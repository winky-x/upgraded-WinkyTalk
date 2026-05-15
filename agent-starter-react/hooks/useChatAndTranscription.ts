import { useMemo } from 'react';
import {
  type ReceivedChatMessage,
  type TextStreamData,
  useChat,
  useRoomContext,
  useTranscriptions,
} from '@livekit/components-react';
import { transcriptionToChatMessage } from '@/lib/utils';

export default function useChatAndTranscription() {
  const transcriptions: TextStreamData[] = useTranscriptions();
  const chat = useChat();
  const room = useRoomContext();

  const mergedTranscriptions = useMemo(() => {
    const merged: Array<ReceivedChatMessage> = [
      ...transcriptions.map((transcription) => transcriptionToChatMessage(transcription, room)),
      ...chat.chatMessages,
    ];

    // Smart sorting that handles edge cases:
    // 1. Primary sort: by timestamp ascending (oldest first)
    // 2. Secondary sort: by message origin (local/user before remote/AI)
    // This prevents timing edge cases where AI response appears before user message
    return merged.sort((a, b) => {
      const timeDiff = a.timestamp - b.timestamp;
      
      // If timestamps differ by more than 50ms, use timestamp order
      if (Math.abs(timeDiff) > 50) {
        return timeDiff;
      }
      
      // For messages received within 50ms (timing edge cases):
      // Local (user messages from isLocal=true) should appear before remote (AI)
      const aIsLocal = a.from?.isLocal ?? false;
      const bIsLocal = b.from?.isLocal ?? false;
      
      if (aIsLocal && !bIsLocal) return -1; // A is user, comes first
      if (!aIsLocal && bIsLocal) return 1;  // B is user, comes first
      
      // Fallback to timestamp for same-type messages
      return timeDiff;
    });
  }, [transcriptions, chat.chatMessages, room]);

  return { messages: mergedTranscriptions, send: chat.send };
}
