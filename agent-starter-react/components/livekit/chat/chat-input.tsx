'use client';

import React, { useState, useRef, useEffect } from 'react';
import { 
  Files, 
  Orbit, 
  Trash2, 
  RefreshCw, 
  Search, 
  Mic, 
  MicOff, 
  Sparkles, 
  BookOpen, 
  Clock, 
  Coins, 
  Loader, 
  Blocks, 
  Globe, 
  Calculator, 
  CloudSun, 
  Zap, 
  ArrowUp, 
  Square, 
  Wrench,
  Paperclip,
  Activity
} from 'lucide-react';
import { toast } from 'sonner';
import { motion, AnimatePresence } from 'motion/react';
import clsx from 'clsx';
import { TrackToggle } from '../track-toggle';
import { Track } from 'livekit-client';

export interface Attachment {
  mimeType: string;
  data: string;
  url: string;
}

interface ChatInputProps {
  onSend: (text: string, attachments?: Attachment[]) => void;
  disabled?: boolean;
  className?: string;
  // We can pass LiveKit mic toggle props
  isMicMuted?: boolean;
  onToggleMic?: () => void;
}

function LiquidGlassContainer({ className, children, roundedClass = "rounded-[2rem] sm:rounded-[2.5rem]" }: { className?: string, children: React.ReactNode, roundedClass?: string }) {
  return (
    <div className={clsx("relative liquid-glass-exact", roundedClass, className)}>
      <div className="relative z-10 w-full h-full">
        {children}
      </div>
    </div>
  );
}

function GlassFilter() {
  return (
    <svg className="hidden">
      <defs>
        <filter id="container-glass" x="0%" y="0%" width="100%" height="100%" colorInterpolationFilters="sRGB">
          <feTurbulence type="fractalNoise" baseFrequency="0.05 0.05" numOctaves={1} seed={1} result="turbulence" />
          <feGaussianBlur in="turbulence" stdDeviation="2" result="blurredNoise" />
          <feDisplacementMap in="SourceGraphic" in2="blurredNoise" scale={70} xChannelSelector="R" yChannelSelector="B" result="displaced" />
          <feGaussianBlur in="displaced" stdDeviation="4" result="finalBlur" />
          <feComposite in="finalBlur" in2="finalBlur" operator="over" />
        </filter>
      </defs>
    </svg>
  );
}

export function ChatInput({ onSend, disabled, className, isMicMuted, onToggleMic }: ChatInputProps) {
  const [value, setValue] = useState('');
  const [attachments, setAttachments] = useState<Attachment[]>([]);
  const [showTools, setShowTools] = useState(false);
  const [selectedTool, setSelectedTool] = useState<string | undefined>();

  const fileInputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const toolsButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        showTools &&
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        toolsButtonRef.current &&
        !toolsButtonRef.current.contains(event.target as Node)
      ) {
        setShowTools(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showTools]);
  
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const availableTools = [
    { id: '', label: 'Autonomous Intelligence', icon: <Sparkles className="w-3.5 h-3.5" />, color: 'text-violet-500' },
    { id: 'detailed_google_search', label: 'Detailed Web Search', icon: <Search className="w-3.5 h-3.5" />, color: 'text-blue-500' },
    { id: 'fast_google_search', label: 'Fast Web Search', icon: <Zap className="w-3.5 h-3.5" />, color: 'text-amber-500' },
    { id: 'get_accurate_weather', label: 'Weather Forecast', icon: <CloudSun className="w-3.5 h-3.5" />, color: 'text-sky-400' },
    { id: 'read_webpage_content', label: 'Read Webpage', icon: <BookOpen className="w-3.5 h-3.5" />, color: 'text-emerald-500' },
    { id: 'evaluate_math_expression', label: 'Math Calculator', icon: <Calculator className="w-3.5 h-3.5" />, color: 'text-rose-500' },
    { id: 'get_current_time_and_date', label: 'Time & Date', icon: <Clock className="w-3.5 h-3.5" />, color: 'text-zinc-500' },
    { id: 'get_crypto_price', label: 'Crypto Price', icon: <Coins className="w-3.5 h-3.5" />, color: 'text-yellow-500' },
  ];

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  }, [value]);

  const handleSend = () => {
    if (disabled) return;
    if (value.trim() || attachments.length > 0) {
      // In WinkyTalk, tools are handled autonomously, but if a tool was selected, we could prefix it.
      let finalMessage = value;
      if (selectedTool) {
        finalMessage = `[Tool: ${selectedTool}] ${value}`;
      }
      
      onSend(finalMessage, attachments);
      setValue('');
      setAttachments([]);
      setShowTools(false);
      setSelectedTool(undefined);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;
    const newAttachments: Attachment[] = [];
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const data = await new Promise<string>((resolve) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve((reader.result as string).split(',')[1]);
        reader.readAsDataURL(file);
      });
      newAttachments.push({ mimeType: file.type, data, url: URL.createObjectURL(file) });
    }
    setAttachments((prev) => [...prev, ...newAttachments]);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const removeAttachment = (index: number) => {
    setAttachments((prev) => {
      const newAtt = [...prev];
      URL.revokeObjectURL(newAtt[index].url);
      newAtt.splice(index, 1);
      return newAtt;
    });
  };

  return (
    <div className={clsx("relative w-full mx-auto pb-1 sm:pb-2", className)}>
      {/* TOOL POPUP OVERLAY */}
      <AnimatePresence>
        {showTools && (
          <motion.div 
            ref={dropdownRef}
            initial={{ opacity: 0, y: 10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.95 }}
            className="absolute bottom-[calc(100%+16px)] left-2 sm:left-4 w-[calc(100vw-16px)] sm:w-72 max-w-[288px] z-50 p-2"
          >
            <LiquidGlassContainer roundedClass="rounded-[2rem]">
              <div className="p-3">
                <div className="px-3 py-2 text-[10px] font-black text-white/50 uppercase tracking-[0.2em] border-b border-white/10 mb-2 flex items-center gap-2">
                  <Activity size={12} className="text-violet-400" /> Cognitive Directives
                </div>
                <div className="space-y-1">
                  {availableTools.map((tool) => (
                    <button
                      key={tool.id}
                      onClick={() => {
                        setSelectedTool(tool.id);
                        setShowTools(false);
                      }}
                      className={clsx(
                        "w-full flex items-center gap-3 px-3 py-2.5 rounded-[1.25rem] text-[13px] font-semibold transition-all duration-300 group/item",
                        selectedTool === tool.id
                          ? "bg-white/20 text-white shadow-[0_0_15px_rgba(255,255,255,0.1)]"
                          : "text-white/80 hover:bg-white/10 hover:text-white"
                      )}
                    >
                      <div className={clsx(
                        "p-1.5 rounded-xl transition-colors",
                        selectedTool === tool.id ? "bg-white/20 text-white" : "bg-white/10 group-hover/item:bg-white/20",
                        tool.color && selectedTool !== tool.id ? tool.color : ""
                      )}>
                        {tool.icon}
                      </div>
                      <span className="flex-1 text-left">{tool.label}</span>
                    </button>
                  ))}
                </div>
              </div>
            </LiquidGlassContainer>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ATTACHMENTS BAR */}
      <AnimatePresence>
        {attachments.length > 0 && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="flex flex-wrap gap-2 mb-3 px-2 overflow-hidden"
          >
            {attachments.map((att, idx) => (
              <motion.div 
                key={idx} 
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                className="relative group p-1"
              >
                <LiquidGlassContainer roundedClass="rounded-2xl">
                  <div className="p-1 relative">
                    {att.mimeType.startsWith('image/') ? (
                      <img src={att.url} className="h-16 w-16 object-cover rounded-xl" />
                    ) : (
                      <div className="h-16 w-16 flex items-center justify-center bg-violet-100 rounded-xl text-violet-600">
                        <Files className="w-6 h-6" />
                      </div>
                    )}
                    <button
                      onClick={() => removeAttachment(idx)}
                      className="absolute -top-1 -right-1 bg-white text-rose-500 rounded-full p-1 shadow-md opacity-0 group-hover:opacity-100 transition-opacity z-20"
                    >
                      <Trash2 size={10} />
                    </button>
                  </div>
                </LiquidGlassContainer>
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* MAIN INPUT CONTAINER (Refined with liquid-glass logic) */}
      <LiquidGlassContainer
        className={clsx(
          "flex flex-col gap-1 sm:gap-2 p-1.5 sm:p-2.5 transition-all duration-500",
          disabled ? "opacity-60 grayscale" : "focus-within:ring-1 focus-within:ring-white/10"
        )}
      >
        <div className="flex items-end gap-1.5 sm:gap-2.5 pr-1 sm:pr-2">
          {/* LEFT ACTIONS */}
          <div className="flex items-center gap-1 pl-1 sm:pl-2 mb-1">
            <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" multiple accept="image/*,video/*,audio/*" />
            <button
              onClick={() => fileInputRef.current?.click()}
              className="p-2 sm:p-3 text-white/70 hover:text-white hover:bg-white/10 rounded-full transition-all active:scale-90"
              disabled={disabled}
            >
              <Paperclip size={22} />
            </button>

            <button
              ref={toolsButtonRef}
              onClick={() => setShowTools(!showTools)}
              className={clsx(
                "p-2 sm:p-3 rounded-full transition-all active:scale-90",
                showTools || selectedTool ? "text-white bg-white/20 shadow-inner" : "text-white/70 hover:text-white hover:bg-white/10"
              )}
              disabled={disabled}
            >
              <Blocks size={22} />
            </button>
          </div>

          {/* TEXT AREA */}
          <div className="flex-1 min-w-0 min-h-[44px] sm:min-h-[52px] flex items-center py-1">
            <textarea
              ref={textareaRef}
              value={value}
              onChange={(e) => setValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask Winky..."
              className="w-full max-h-40 min-h-[38px] sm:min-h-[44px] px-1 sm:px-2 py-1.5 sm:py-2.5 bg-transparent resize-none focus:outline-none text-white placeholder:text-white/70 font-sans leading-normal text-[16px] sm:text-[18px] selection:bg-white/20"
              rows={1}
              disabled={disabled}
            />
          </div>

          {/* RIGHT ACTIONS */}
          <div className="flex items-center gap-1.5 sm:gap-2.5 mb-1">
            {/* LiveKit Mic Toggle instead of manual recording */}
            <button
              onClick={onToggleMic}
              className={clsx(
                "p-2 sm:p-3 rounded-full transition-all duration-500 shadow-md",
                isMicMuted 
                  ? "bg-zinc-800 text-zinc-400 hover:bg-zinc-700" 
                  : "bg-emerald-500/20 text-emerald-200 hover:bg-emerald-500/30 ring-2 ring-emerald-400/30 animate-pulse"
              )}
              disabled={disabled}
            >
              {isMicMuted ? <MicOff size={22} /> : <Mic size={22} />}
            </button>

            <button
              onClick={handleSend}
              disabled={disabled || (!value.trim() && attachments.length === 0)}
              className={clsx(
                "flex items-center justify-center rounded-full transition-all duration-300 w-10 h-10 sm:w-11 sm:h-11 shrink-0 ml-1",
                (!value.trim() && attachments.length === 0) 
                  ? "bg-white/10 text-white/30 cursor-not-allowed shadow-inner" 
                  : "bg-white text-black shadow-[0_0_15px_rgba(255,255,255,0.4)] cursor-pointer hover:scale-105 active:scale-95",
                disabled && "opacity-50 grayscale cursor-not-allowed"
              )}
            >
              {disabled ? <Loader className="w-5 h-5 animate-spin" /> : <ArrowUp strokeWidth={2.5} className="w-5 h-5 sm:w-6 sm:h-6" />}
            </button>
          </div>
        </div>
      </LiquidGlassContainer>
      
      <GlassFilter />
    </div>
  );
}
