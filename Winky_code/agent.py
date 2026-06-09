import sys
import os
import time
import asyncio
import logging

# Fix encoding issue
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore

# Import LiveKit modules
from livekit import agents
from livekit.agents import Agent, JobContext, RoomInputOptions
from livekit.agents.voice import AgentSession
from livekit.agents.llm import ChatContext
from livekit.plugins import google, openai, silero, noise_cancellation
from livekit.plugins.google.tools import GoogleSearch

# Import your custom modules
from Winky_prompts import load_prompts
from memory_loop import MemoryExtractor
from config_manager import ConfigManager
from dotenv import load_dotenv

# PC Operator tools and others are now handled dynamically via MCP server

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
import inspect
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from livekit.agents import function_tool


def create_mcp_tool(mcp_session: ClientSession, tool_info):
    name = tool_info.name.replace("-", "_")
    desc = tool_info.description or ""
    
    raw_schema = {
        "name": name,
        "description": desc,
        "parameters": tool_info.inputSchema
    }
    
    async def dynamic_mcp_tool(raw_arguments: dict) -> str:
        try:
            result = await mcp_session.call_tool(tool_info.name, arguments=raw_arguments)
            logger.info(f"MCP Tool {name} response: isError={result.isError} content={result.content}")
            if result.isError:
                return f"[DEBUG MODE ERROR: MCP Tool Failed] {result.content[0].text}"
            return result.content[0].text
        except Exception as e:
            logger.error(f"MCP Tool {name} failed: {e}")
            return f"[DEBUG MODE ERROR: Exception in Tool Execution] {str(e)}"
            
    dynamic_mcp_tool.__name__ = name
    dynamic_mcp_tool.__doc__ = desc
    
    from livekit.agents.llm import function_tool as ai_tool
    return ai_tool(dynamic_mcp_tool, raw_schema=raw_schema)

class Assistant(Agent):
    def __init__(self, chat_ctx, llm_instance, instructions_text, tools=None) -> None:
        super().__init__(
            instructions=instructions_text,
            chat_ctx=chat_ctx,
            llm=llm_instance,
            tools=tools
        )


async def entrypoint(ctx: JobContext):
    # Connect to the room
    await ctx.connect()

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
    model_name = llm_config.get("model") or "gemini-2.5-flash-native-audio-latest"
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
            # Fallback to non-realtime LLM with tools
            llm_instance = google.LLM(
                model=model_name,
                api_key=google_api_key
            )
            
    elif provider == "openai":
        openai_api_key = config.get_api_key("openai")
        if not openai_api_key:
            logger.error("OpenAI API key not found in config!")
            raise ValueError("OpenAI API key is required when using OpenAI provider")
            
        if hasattr(openai, 'realtime'):
            llm_instance = openai.realtime.RealtimeModel(
                model="gpt-4o-realtime-preview",
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
            
        llm_instance = google.LLM(
            model="gemini-2.5-flash",
            api_key=google_api_key
        )
    
    # Start MCP Server Subprocess
    mcp_server_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "winky_mcp_server.py")
    subprocess_env = os.environ.copy()
    subprocess_env["PYTHONIOENCODING"] = "utf-8"
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[mcp_server_path],
        env=subprocess_env
    )
    
    logger.info("Starting Winky MCP Server Subprocess...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as mcp_session:
            await mcp_session.initialize()
            logger.info("MCP Session Initialized.")
            
            # Fetch tools
            tools_response = await mcp_session.list_tools()
            logger.info(f"Discovered {len(tools_response.tools)} tools from MCP server.")
            
            # We keep GoogleSearch native as requested
            dynamic_tools = [GoogleSearch()]
            for tool in tools_response.tools:
                dynamic_tools.append(create_mcp_tool(mcp_session, tool))
                
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
                instructions_text=instructions_prompt,
                tools=dynamic_tools
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
            
            # Set up Chat handling for text messages manually using data_received
            from livekit import rtc
            @ctx.room.on("data_received")
            def on_data_received(data_packet: rtc.DataPacket, **kwargs):
                if data_packet.topic == "lk.chat":
                    import json
                    try:
                        chat_data = json.loads(data_packet.data.decode("utf-8"))
                        message = chat_data.get("message")
                        if message:
                            logger.info(f"Received text chat message: {message}")
                            # Append user message to the conversation history
                            if hasattr(agent, 'chat_ctx') and agent.chat_ctx is not None:
                                agent.chat_ctx.append(role="user", text=message)
                            elif hasattr(session, 'chat_ctx') and session.chat_ctx is not None:
                                session.chat_ctx.append(role="user", text=message)
                            else:
                                logger.warning("Could not find chat_ctx to append message")
                            
                            # Force the agent to reply
                            asyncio.create_task(session.generate_reply())
                    except Exception as e:
                        logger.error(f"Error parsing chat message: {e}")
            
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

    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint, agent_name="winky"))