import sys
import os
import time
import asyncio
import logging

# Fix encoding issue
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Import LiveKit modules
from livekit import agents
from livekit.agents import Agent, JobContext, RoomInputOptions
from livekit.agents.voice import AgentSession
from livekit.agents.llm import ChatContext
from livekit.plugins import google, openai, silero, noise_cancellation

# Import your custom modules
from Jarvis_prompts import load_prompts
from memory_loop import MemoryExtractor
from config_manager import ConfigManager
from dotenv import load_dotenv

# Disable mem0 for now
# from mem0 import AsyncMemoryClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize config
config = ConfigManager()
load_dotenv()

# Add at the top with other imports
import requests
import json

# Add this function in agent.py (after imports, before the Assistant class)
def perform_web_search(query: str) -> str:
    """Perform web search using Google Custom Search API"""
    from config_manager import ConfigManager
    
    config = ConfigManager()
    config.load_config()
    
    # Get API keys from config
    api_key = config.get_api_key("google_search")
    search_engine_id = config.get("api_keys.search_engine_id", "")
    
    if not api_key:
        return "❌ Search not configured: Missing Google Search API key"
    
    if not search_engine_id:
        return "❌ Search not configured: Missing Search Engine ID"
    
    print(f"🔍 Attempting search for: {query}")
    print(f"🔑 API Key present: {'Yes' if api_key else 'No'}")
    print(f"🆔 Search Engine ID present: {'Yes' if search_engine_id else 'No'}")
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": query,
            "num": 3,  # Get 3 results
            "dateRestrict": "m1"  # Last month only
        }
        
        print(f"🌐 Making request to: {url}")
        print(f"📋 Parameters: { {k: '***' if 'key' in k else v for k, v in params.items()} }")
        
        response = requests.get(url, params=params, timeout=15)
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            search_info = data.get("searchInformation", {})
            total_results = search_info.get("totalResults", "0")
            
            print(f"📈 Total results found: {total_results}")
            
            items = data.get("items", [])
            
            if not items:
                return "🔍 No recent results found. Try a different search query."
            
            results = []
            for i, item in enumerate(items[:3], 1):  # Limit to 3 results
                title = item.get("title", "No title")
                link = item.get("link", "No link")
                snippet = item.get("snippet", "No description")
                
                # Try to get display link
                display_link = item.get("displayLink", link)
                
                results.append(
                    f"{i}. **{title}**\n"
                    f"   📍 {display_link}\n"
                    f"   📝 {snippet}\n"
                )
            
            return (
                f"🔍 **Search Results for '{query}'** (Found {total_results} results)\n\n" +
                "\n".join(results) +
                f"\n📅 *Results limited to last month*"
            )
        
        elif response.status_code == 403:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Unknown error")
            return f"❌ Search API Error (403): {error_msg}\n\nThis usually means:\n1. API key is invalid\n2. Billing is not enabled\n3. Search Engine ID is wrong"
        
        elif response.status_code == 400:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Unknown error")
            return f"❌ Search API Error (400): {error_msg}"
        
        else:
            return f"❌ Search failed with status {response.status_code}: {response.text[:200]}"
            
    except requests.exceptions.Timeout:
        return "⏰ Search timeout: The request took too long"
    except requests.exceptions.ConnectionError:
        return "🔌 Connection error: Cannot connect to search API"
    except Exception as e:
        return f"❌ Search error: {str(e)}"
    
class Assistant(Agent):
    def __init__(self, chat_ctx, llm_instance, instructions_text) -> None:
        super().__init__(
            instructions=instructions_text,
            chat_ctx=chat_ctx,
            llm=llm_instance
        )


async def entrypoint(ctx: JobContext):
    # RELOAD CONFIGURATION
    config.load_config()
    
    # Load Dynamic Prompts
    instructions_prompt, reply_prompt = await load_prompts()

    # Get user name and mem0 key from config
    user_id = config.get_user_id()
    full_name = config.get_full_name()
    mem0_key = config.get_mem0_key()
    
    logger.info(f"Fetching initial memories for user_id: {user_id} (Spoken Name: {full_name})")
    
    # STARTUP MEMORY: Fetch existing memories before the agent starts
    memory_str = ""
    try:
        if mem0_key:
            memory_str = "\n(Memory system temporarily disabled)"
        else:
            logger.warning("Mem0 key not found. Skipping startup memory fetch.")
            memory_str = "\n(Memory system disabled - Stateless Mode)"
            
    except Exception as e:
        logger.error(f"Error fetching initial memories: {e}")
        logger.exception("Full traceback:")
        memory_str = "\n(Memory system unavailable)"

    # Get LLM Configuration from config
    llm_config = config.get_llm_config()
    provider = llm_config.get("provider", "google")
    model_name = llm_config.get("model", "gemini-2.5-flash-native-audio-preview-09-2025")
    # Default fallback voices per provider
    default_voice = "Puck" if provider == "google" else "alloy"
    voice_name = llm_config.get("voice", default_voice)

    logger.info(f"Using LLM Provider: {provider}, Model: {model_name}, Voice: {voice_name}")

    # Create LLM instance based on provider
    llm_instance = None
    if provider == "google":
        google_api_key = config.get_api_key("google")
        if not google_api_key:
            logger.error("Google API key not found in config!")
            raise ValueError("Google API key is required when using Google provider")
        
        # Check which Google module to use
        if hasattr(google, 'beta') and hasattr(google.beta, 'realtime'):
            llm_instance = google.beta.realtime.RealtimeModel(
                model=model_name,
                api_key=google_api_key,
                voice=voice_name
            )
        elif hasattr(google, 'realtime'):
            llm_instance = google.realtime.RealtimeModel(
                model=model_name,
                api_key=google_api_key,
                voice=voice_name
            )
        else:
            raise ImportError("Google realtime module not found")
            
    elif provider == "openai":
        openai_api_key = config.get_api_key("openai")
        if not openai_api_key:
            logger.error("OpenAI API key not found in config!")
            raise ValueError("OpenAI API key is required when using OpenAI provider")
            
        if hasattr(openai, 'realtime'):
            llm_instance = openai.realtime.RealtimeModel(
                model=model_name,
                api_key=openai_api_key,
                voice=voice_name
            )
        else:
            raise ImportError("OpenAI realtime module not found")
    else:
        # Fallback to Google
        logger.error(f"Unsupported LLM provider: {provider}. Falling back to Google.")
        google_api_key = config.get_api_key("google")
        if not google_api_key:
            raise ValueError("Google API key is required for fallback")
            
        if hasattr(google, 'realtime'):
            llm_instance = google.realtime.RealtimeModel(
                model="gemini-2.5-flash-native-audio-preview-09-2025",
                api_key=google_api_key,
                voice="Puck"
            )
        else:
            raise ImportError("Google realtime module not found")
    
    # Configure the Session
    session = AgentSession(
        preemptive_generation=True
    )

    # Get the current chat history reference
    current_ctx = session.history.items

    # Inject the startup memory into the context
    initial_ctx = ChatContext()
    initial_ctx.add_message(
        role="assistant", 
        content=f'''The user's spoken name is {full_name}. Internal memory ID is {user_id}.{memory_str}'''
    )
    
    # Create the Agent instance
    agent = Assistant(
        chat_ctx=initial_ctx, 
        llm_instance=llm_instance, 
        instructions_text=instructions_prompt
    )
    
    # Try different start() signatures based on your LiveKit version
    # OPTION 1: Most common - no input_options parameter
    try:
        await session.start(
            room=ctx.room,
            agent=agent
        )
    except TypeError as e:
        # OPTION 2: Try with room_input_options (deprecated but might work)
        logger.warning(f"Option 1 failed: {e}. Trying alternative...")
        try:
            await session.start(
                room=ctx.room,
                agent=agent,
                room_input_options=RoomInputOptions(
                    noise_cancellation=noise_cancellation.BVC()
                )
            )
        except TypeError as e2:
            # OPTION 3: Simplest - no options at all
            logger.warning(f"Option 2 failed: {e2}. Trying simplest option...")
            await session.start(
                room=ctx.room,
                agent=agent
            )
    
    # Generate Initial Reply
    await session.generate_reply(
        instructions=reply_prompt
    )
    
    # Start the memory extraction loop
    conv_ctx = MemoryExtractor()
    await conv_ctx.run(current_ctx)


if __name__ == "__main__":
    # --- Windows Specific Fix ---
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # --- Wait for Valid Config Loop ---
    print("Agent starting... checking for configuration...")
    while True:
        config.load_config()
        lk_url = config.get_api_key("livekit_url")
        lk_key = config.get_api_key("livekit_key")
        lk_secret = config.get_api_key("livekit_secret")

        if lk_url and lk_key and lk_secret:
            active_user_id = config.get_user_id()
            active_full_name = config.get_full_name()
            print(f"Configuration found! Connecting to {lk_url}...")
            print(f"ACTIVE USER PROFILE: ID=[{active_user_id}] NAME=[{active_full_name}]")
            
            # Inject LiveKit credentials
            os.environ["LIVEKIT_URL"] = lk_url
            os.environ["LIVEKIT_API_KEY"] = lk_key
            os.environ["LIVEKIT_API_SECRET"] = lk_secret
            
            # Inject LLM API keys
            google_key = config.get_api_key("google")
            openai_key = config.get_api_key("openai")
            
            if google_key:
                os.environ["GOOGLE_API_KEY"] = google_key
            if openai_key:
                os.environ["OPENAI_API_KEY"] = openai_key
            
            # Inject Mem0 Key
            mem0_key = config.get_mem0_key()
            if mem0_key:
                os.environ["MEM0_API_KEY"] = mem0_key
            else:
                print("⚠️  WARNING: Mem0 key not found - Memory system will be disabled")
                
            break
        else:
            print("Waiting for Setup to be completed in browser... (checking again in 2s)")
            time.sleep(2)
    # ------------------------------------------

    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))