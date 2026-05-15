# How to Replicate Winky AI Voice Agent Assistant Using Gemini

## GitHub Repository
**Source Code:** [https://github.com/winky-x/upgraded-WinkyTalk](https://github.com/winky-x/upgraded-WinkyTalk)

## Professional System Prompt for Advanced AI Code Generation

**SYSTEM PROMPT FOR HIGHLY CAPABLE AI CODE GENERATOR:**

```
You are Grok, an advanced AI coding assistant built by xAI, with exceptional capabilities in full-stack software development, system architecture, and complex project implementation. You have deep expertise in Python, TypeScript, React, Next.js, real-time systems, AI integration, and production-grade application development.

Your mission is to create a complete, production-ready voice AI assistant application based on the detailed specifications provided. You must demonstrate mastery in:

**CORE COMPETENCIES:**
- Full-stack application development (Python backend + TypeScript/React frontend)
- Real-time communication systems (WebRTC, WebSockets, LiveKit)
- AI/ML integration (Google Gemini, API orchestration)
- System architecture and scalability
- Security best practices and performance optimization
- Error handling and logging
- Testing and deployment strategies

**DEVELOPMENT PRINCIPLES:**
1. **Production-Ready Code**: All code must be production-quality with proper error handling, logging, and documentation
2. **Security First**: Implement secure API key management, input validation, and authentication
3. **Performance Optimized**: Use efficient algorithms, caching, and resource management
4. **Scalable Architecture**: Design for horizontal scaling and microservices principles
5. **Comprehensive Testing**: Include unit tests, integration tests, and end-to-end testing
6. **Documentation**: Provide detailed code comments, API documentation, and deployment guides
7. **Best Practices**: Follow industry standards for code organization, naming conventions, and patterns

**TECHNICAL REQUIREMENTS:**
- Python 3.11+ with asyncio for concurrent operations
- TypeScript 5.0+ with strict type checking
- React 19 with modern hooks and patterns
- Next.js 15 with App Router
- LiveKit for real-time communication
- Google Gemini for AI processing
- RESTful API design
- Database integration (if needed)
- Docker containerization
- CI/CD pipeline setup

**IMPLEMENTATION APPROACH:**
1. **Analyze Requirements**: Thoroughly understand all specifications before coding
2. **Design Architecture**: Create detailed system diagrams and component relationships
3. **Implement Core Systems**: Build foundational components first (config, logging, error handling)
4. **Develop Backend**: Create Python services with proper async patterns
5. **Build Frontend**: Develop React components with TypeScript
6. **Integrate Systems**: Connect frontend and backend with real-time communication
7. **Add AI Features**: Implement Gemini integration with tool calling
8. **Testing & Validation**: Comprehensive testing at each stage
9. **Documentation**: Complete setup and deployment guides
10. **Optimization**: Performance tuning and security hardening

**QUALITY STANDARDS:**
- Code must compile and run without errors
- All dependencies properly managed
- Environment variables and configuration handled securely
- Logging implemented at appropriate levels
- Error messages user-friendly and informative
- Code follows PEP 8 (Python) and ESLint (TypeScript) standards
- Comprehensive error handling for all edge cases
- Input validation and sanitization
- Rate limiting and abuse prevention
- GDPR/CCPA compliance considerations

**DELIVERABLES:**
1. Complete source code with all components
2. Detailed setup and installation instructions
3. API documentation and usage examples
4. Testing procedures and test cases
5. Deployment configurations (Docker, cloud)
6. Performance benchmarks and optimization notes
7. Security audit checklist and implementation
8. Troubleshooting guide and common issues
9. Future enhancement roadmap
10. Maintenance and monitoring guidelines

**SPECIAL INSTRUCTIONS:**
- When generating code, include detailed comments explaining complex logic
- Use type hints in Python and TypeScript for better code quality
- Implement proper async/await patterns throughout
- Handle all API rate limits and error responses gracefully
- Create modular, reusable components
- Follow the single responsibility principle
- Implement proper separation of concerns
- Use environment variables for all sensitive data
- Include health checks and monitoring endpoints
- Design for easy configuration and customization

Remember: You are not just writing code; you are architecting a complete, professional-grade AI voice assistant system that must be immediately deployable and maintainable in production environments.
```

## Overview
Winky AI is a conversational voice agent assistant built with a modern web frontend and Python backend. This guide explains how to create an exact or very similar AI agent using Google's Gemini AI to code the entire project from backend to frontend.

The project consists of:
- A Next.js 15 frontend with React 19 for the user interface
- A Python backend using LiveKit Agents framework
- Google Gemini integration for conversational AI
- Real-time voice and video communication
- Tool integrations (web search, weather, memory)
- Configuration management system
- Memory extraction and context management

## Project Architecture

### Frontend (Next.js + React)
- **Framework:** Next.js 15 with React 19
- **Real-time Communication:** LiveKit Client SDK
- **UI Components:** Radix UI, Tailwind CSS
- **Features:** Video/audio tiles, chat interface, device selection, agent controls
- **State Management:** React hooks and context
- **Styling:** Tailwind CSS with custom components
- **Routing:** Next.js App Router

### Backend (Python)
- **Framework:** LiveKit Agents
- **LLM Integration:** Google Gemini (Realtime API)
- **Tools:** Web search, weather, memory system, advanced search
- **Configuration:** JSON-based config management
- **Async Processing:** Python asyncio for concurrent operations
- **API Integrations:** Multiple external service integrations

### Key Technologies
- **LiveKit:** Real-time voice/video communication platform
- **Google Gemini:** AI model for conversational responses
- **Python AsyncIO:** Backend processing and concurrency
- **WebRTC:** Real-time media streaming protocol
- **WebSockets:** Real-time bidirectional communication
- **REST APIs:** External service integrations

## Prerequisites

### System Requirements
- Python 3.11 or 3.12 (recommended for stability)
- Node.js v20.19.6 or later
- MSVC Build Tools (for Windows C++ compilation)
- Git for version control
- At least 8GB RAM recommended
- Stable internet connection for API calls

### API Keys Required
- Google Gemini API Key (from Google AI Studio)
- LiveKit Cloud API Credentials (URL, Key, Secret)
- Google Custom Search API (for web search functionality)
- OpenWeatherMap API (for weather information)
- Optional: Mem0 API for advanced memory management

### Development Environment Setup
1. Install Python 3.11/3.12
2. Install Node.js v20+
3. Install Git
4. Set up virtual environment for Python
5. Install package managers (pip, pnpm/npm)

## Step-by-Step Replication Guide

### 1. Project Setup with Gemini

**Detailed Prompt for Gemini:**

```
Create a complete AI voice assistant project structure with the following specifications:

PROJECT REQUIREMENTS:
- Name: WinkyAI-Replica
- Architecture: Full-stack with separate frontend/backend
- Frontend: Next.js 15, React 19, TypeScript, Tailwind CSS
- Backend: Python 3.11+, LiveKit Agents, AsyncIO
- AI: Google Gemini Realtime API integration
- Communication: LiveKit for real-time voice/video
- Tools: Web search, weather API, memory system
- Configuration: JSON-based with environment variables
- Deployment: Local development with production considerations

FOLDER STRUCTURE:
WinkyAI-Replica/
├── frontend/                    # Next.js application
│   ├── app/                     # Next.js app router
│   ├── components/              # React components
│   ├── lib/                     # Utilities and configurations
│   ├── public/                  # Static assets
│   └── styles/                  # Global styles
├── backend/                     # Python LiveKit agent
│   ├── agent.py                 # Main agent file
│   ├── config_manager.py        # Configuration handling
│   ├── tools/                   # Custom tools directory
│   │   ├── web_search.py        # Google search integration
│   │   ├── weather.py           # Weather API integration
│   │   └── memory.py            # Memory management
│   ├── prompts/                 # Dynamic prompt templates
│   └── requirements.txt         # Python dependencies
├── config/                      # Configuration files
│   ├── user_config.json         # User settings template
│   └── environment.example      # Environment variables
├── docs/                        # Documentation
└── scripts/                     # Utility scripts

INCLUDE:
- Package.json files with all dependencies
- TypeScript configurations
- ESLint and Prettier configs
- Python virtual environment setup
- Docker files for containerization
- README with setup instructions
```

### 2. Backend Development

**Have Gemini generate the Python backend with detailed specifications:**

```python
# backend/agent.py - Main agent implementation
import sys
import os
import asyncio
import logging
from typing import Optional, Dict, Any
from datetime import datetime

# Fix encoding issues
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# LiveKit imports
from livekit import agents
from livekit.agents import Agent, JobContext, RoomInputOptions
from livekit.agents.voice import AgentSession
from livekit.agents.llm import ChatContext
from livekit.plugins import google, openai, silero, noise_cancellation

# Custom imports
from config_manager import ConfigManager
from tools.web_search import perform_web_search
from tools.weather import get_weather_info
from tools.memory import MemoryExtractor
from prompts.loader import load_prompts

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VoiceAssistantAgent(Agent):
    """
    Main voice assistant agent class that handles conversational AI interactions.
    
    This agent integrates with Google Gemini for natural language processing,
    provides tool-based functionalities, and manages conversation memory.
    """
    
    def __init__(
        self, 
        chat_ctx: ChatContext, 
        llm_instance, 
        instructions_text: str, 
        tools: Optional[list] = None,
        config: ConfigManager = None
    ):
        """
        Initialize the voice assistant agent.
        
        Args:
            chat_ctx: LiveKit chat context for conversation history
            llm_instance: Configured LLM instance (Gemini/OpenAI)
            instructions_text: System prompt for the agent
            tools: List of available tools (search, weather, etc.)
            config: Configuration manager instance
        """
        super().__init__(
            instructions=instructions_text,
            chat_ctx=chat_ctx,
            llm=llm_instance,
            tools=tools or []
        )
        
        self.config = config or ConfigManager()
        self.memory_extractor = MemoryExtractor()
        self.start_time = datetime.now()
        
        logger.info("Voice Assistant Agent initialized successfully")

async def initialize_llm(config: ConfigManager) -> Any:
    """
    Initialize the appropriate LLM based on configuration.
    
    Args:
        config: Configuration manager instance
        
    Returns:
        Configured LLM instance
        
    Raises:
        ValueError: If required API keys are missing
        ImportError: If required modules are not available
    """
    llm_config = config.get_llm_config()
    provider = llm_config.get("provider", "google")
    model_name = llm_config.get("model", "gemini-2.5-flash-native-audio-preview-09-2025")
    voice_name = llm_config.get("voice", "Puck")

    logger.info(f"Initializing LLM: {provider}/{model_name} with voice: {voice_name}")

    if provider == "google":
        google_api_key = config.get_api_key("google")
        if not google_api_key:
            raise ValueError("Google API key required for Google provider")

        # Try different Google module versions
        try:
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
        except Exception as e:
            logger.error(f"Failed to initialize Google LLM: {e}")
            raise

    elif provider == "openai":
        openai_api_key = config.get_api_key("openai")
        if not openai_api_key:
            raise ValueError("OpenAI API key required for OpenAI provider")

        if hasattr(openai, 'realtime'):
            llm_instance = openai.realtime.RealtimeModel(
                model=model_name,
                api_key=openai_api_key,
                voice=voice_name
            )
        else:
            raise ImportError("OpenAI realtime module not found")
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    return llm_instance

async def setup_memory_system(config: ConfigManager) -> str:
    """
    Set up the memory system and return initial memory context.
    
    Args:
        config: Configuration manager instance
        
    Returns:
        Initial memory context string
    """
    user_id = config.get_user_id()
    full_name = config.get_full_name()
    mem0_key = config.get_mem0_key()

    memory_str = ""
    
    try:
        if mem0_key:
            # Initialize memory client if available
            memory_str = f"\n(Memory system active for user: {full_name})"
            logger.info(f"Memory system initialized for user_id: {user_id}")
        else:
            memory_str = "\n(Memory system disabled - Stateless Mode)"
            logger.warning("Mem0 key not found - memory system disabled")
    except Exception as e:
        logger.error(f"Error initializing memory system: {e}")
        memory_str = "\n(Memory system unavailable)"

    return memory_str

async def entrypoint(ctx: JobContext):
    """
    Main entry point for the LiveKit agent.
    
    This function initializes all components, sets up the agent session,
    and starts the conversation loop.
    
    Args:
        ctx: LiveKit job context
    """
    logger.info("Starting agent entrypoint")
    
    # Initialize configuration
    config = ConfigManager()
    config.load_config()
    
    # Load dynamic prompts
    try:
        instructions_prompt, reply_prompt = await load_prompts()
        logger.info("Prompts loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load prompts: {e}")
        # Fallback prompts
        instructions_prompt = "You are a helpful voice assistant."
        reply_prompt = "Hello! How can I help you today?"

    # Set up memory system
    memory_context = await setup_memory_system(config)
    
    # Initialize LLM
    try:
        llm_instance = await initialize_llm(config)
        logger.info("LLM initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        raise

    # Get user information
    user_id = config.get_user_id()
    full_name = config.get_full_name()
    
    logger.info(f"Initializing agent for user: {full_name} (ID: {user_id})")

    # Create agent session with noise cancellation
    session = AgentSession(
        preemptive_generation=True,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        )
    )

    # Get current chat context
    current_ctx = session.history.items

    # Initialize chat context with user information
    initial_ctx = ChatContext()
    initial_ctx.add_message(
        role="assistant", 
        content=f'''You are Winky AI, a helpful voice assistant for {full_name}. 
        User internal ID: {user_id}.{memory_context}
        
        Current capabilities:
        - Web search using Google
        - Weather information
        - Memory of previous conversations
        - Real-time voice responses
        
        Always be helpful, accurate, and engaging in your responses.'''
    )

    # Define available tools
    available_tools = [
        perform_web_search,
        get_weather_info
    ]

    # Create the agent instance
    agent = VoiceAssistantAgent(
        chat_ctx=initial_ctx,
        llm_instance=llm_instance,
        instructions_text=instructions_prompt,
        tools=available_tools,
        config=config
    )

    # Start the agent session
    try:
        await session.start(
            room=ctx.room,
            agent=agent
        )
        logger.info("Agent session started successfully")
    except Exception as e:
        logger.error(f"Failed to start agent session: {e}")
        raise

    # Generate initial greeting
    try:
        await session.generate_reply(
            instructions=reply_prompt
        )
        logger.info("Initial reply generated")
    except Exception as e:
        logger.error(f"Failed to generate initial reply: {e}")

    # Start memory extraction loop
    try:
        memory_task = asyncio.create_task(
            MemoryExtractor().run(current_ctx)
        )
        logger.info("Memory extraction loop started")
    except Exception as e:
        logger.error(f"Failed to start memory extraction: {e}")

    # Keep the session alive
    try:
        await session.wait()
    except Exception as e:
        logger.error(f"Session error: {e}")
    finally:
        # Cleanup
        if 'memory_task' in locals():
            memory_task.cancel()
        logger.info("Agent session ended")

if __name__ == "__main__":
    # Windows-specific fix for asyncio
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    logger.info("Agent starting... checking configuration")
    
    # Wait for valid configuration
    config = ConfigManager()
    while True:
        config.load_config()
        
        # Check for required credentials
        lk_url = config.get_api_key("livekit_url")
        lk_key = config.get_api_key("livekit_key")
        lk_secret = config.get_api_key("livekit_secret")

        if lk_url and lk_key and lk_secret:
            active_user_id = config.get_user_id()
            active_full_name = config.get_full_name()
            
            logger.info(f"Configuration found! Connecting to LiveKit at {lk_url}")
            logger.info(f"Active user profile: ID=[{active_user_id}] NAME=[{active_full_name}]")
            
            # Set environment variables
            os.environ["LIVEKIT_URL"] = lk_url
            os.environ["LIVEKIT_API_KEY"] = lk_key
            os.environ["LIVEKIT_API_SECRET"] = lk_secret
            
            # Set API keys
            google_key = config.get_api_key("google")
            openai_key = config.get_api_key("openai")
            mem0_key = config.get_mem0_key()
            
            if google_key:
                os.environ["GOOGLE_API_KEY"] = google_key
            if openai_key:
                os.environ["OPENAI_API_KEY"] = openai_key
            if mem0_key:
                os.environ["MEM0_API_KEY"] = mem0_key
            else:
                logger.warning("Mem0 key not found - memory system disabled")
                
            break
        else:
            logger.info("Waiting for configuration setup... (checking again in 2s)")
            time.sleep(2)
    
    # Start the LiveKit agent
    try:
        agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
    except KeyboardInterrupt:
        logger.info("Agent shutdown requested by user")
    except Exception as e:
        logger.error(f"Critical error starting agent: {e}")
        raise
```

**Key Backend Components to Implement:**

#### Configuration Manager (`config_manager.py`)
```python
import json
import os
import logging
from typing import Dict, Any, Optional

class ConfigManager:
    """
    Centralized configuration management for the voice assistant.
    
    Handles loading, saving, and accessing configuration settings
    from JSON files and environment variables.
    """
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def load_config(self) -> None:
        """Load configuration from user_config.json"""
        config_path = self._get_config_path()
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                logging.info(f"Configuration loaded from {config_path}")
            except Exception as e:
                logging.error(f"Failed to load config: {e}")
                self._config = {}
        else:
            logging.warning(f"Config file not found: {config_path}")
            self._config = {}
    
    def save_config(self) -> None:
        """Save current configuration to file"""
        config_path = self._get_config_path()
        
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2)
            logging.info(f"Configuration saved to {config_path}")
        except Exception as e:
            logging.error(f"Failed to save config: {e}")
    
    def _get_config_path(self) -> str:
        """Get the absolute path to the config file"""
        return os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "config", "user_config.json"
        ))
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service"""
        return self.get(f"api_keys.{service}")
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration"""
        return self.get("llm", {
            "provider": "google",
            "model": "gemini-2.5-flash-native-audio-preview-09-2025",
            "voice": "Puck"
        })
    
    def get_user_id(self) -> str:
        """Get user ID"""
        return self.get("user.id", "default_user")
    
    def get_full_name(self) -> str:
        """Get user's full name"""
        return self.get("user.full_name", "User")
    
    def get_mem0_key(self) -> Optional[str]:
        """Get Mem0 API key"""
        return self.get_api_key("mem0")
```

#### Memory Extraction System (`tools/memory.py`)
```python
import asyncio
import logging
from typing import List, Dict, Any
from livekit.agents.llm import ChatMessage

logger = logging.getLogger(__name__)

class MemoryExtractor:
    """
    Extracts and manages conversation memory for long-term context.
    
    This class monitors chat history and extracts important information
    to maintain conversation context across sessions.
    """
    
    def __init__(self):
        self.memory_items: List[Dict[str, Any]] = []
        self.extraction_interval = 30  # seconds
        self.max_memory_items = 100
    
    async def run(self, chat_history: List[ChatMessage]) -> None:
        """
        Main memory extraction loop.
        
        Args:
            chat_history: LiveKit chat message history
        """
        logger.info("Starting memory extraction loop")
        
        while True:
            try:
                await self._extract_memory(chat_history)
                await asyncio.sleep(self.extraction_interval)
            except asyncio.CancelledError:
                logger.info("Memory extraction cancelled")
                break
            except Exception as e:
                logger.error(f"Memory extraction error: {e}")
                await asyncio.sleep(self.extraction_interval)
    
    async def _extract_memory(self, chat_history: List[ChatMessage]) -> None:
        """
        Extract memory items from recent chat history.
        
        Args:
            chat_history: Current chat message history
        """
        if not chat_history:
            return
        
        # Get recent messages (last 10)
        recent_messages = chat_history[-10:]
        
        for message in recent_messages:
            if self._is_memory_worthy(message):
                memory_item = self._create_memory_item(message)
                self._add_memory_item(memory_item)
    
    def _is_memory_worthy(self, message: ChatMessage) -> bool:
        """
        Determine if a message contains memory-worthy information.
        
        Args:
            message: Chat message to evaluate
            
        Returns:
            True if message should be remembered
        """
        content = message.content.lower()
        
        # Keywords that indicate important information
        memory_keywords = [
            'remember', 'important', 'note', 'save',
            'my name is', 'i am', 'i live in', 'i work',
            'birthday', 'anniversary', 'phone', 'email',
            'address', 'schedule', 'meeting', 'appointment'
        ]
        
        return any(keyword in content for keyword in memory_keywords)
    
    def _create_memory_item(self, message: ChatMessage) -> Dict[str, Any]:
        """
        Create a memory item from a chat message.
        
        Args:
            message: Source chat message
            
        Returns:
            Memory item dictionary
        """
        return {
            'timestamp': message.timestamp,
            'role': message.role,
            'content': message.content,
            'importance': self._calculate_importance(message),
            'tags': self._extract_tags(message)
        }
    
    def _calculate_importance(self, message: ChatMessage) -> float:
        """
        Calculate importance score for a message.
        
        Args:
            message: Chat message
            
        Returns:
            Importance score (0.0 to 1.0)
        """
        content = message.content.lower()
        score = 0.0
        
        # Length factor
        if len(content) > 50:
            score += 0.2
        
        # Question factor
        if '?' in content:
            score += 0.1
        
        # Personal information keywords
        personal_keywords = ['i ', 'my ', 'me ', 'mine']
        if any(kw in content for kw in personal_keywords):
            score += 0.3
        
        # Memory keywords
        memory_keywords = ['remember', 'important', 'note']
        if any(kw in content for kw in memory_keywords):
            score += 0.4
        
        return min(score, 1.0)
    
    def _extract_tags(self, message: ChatMessage) -> List[str]:
        """
        Extract tags from a message for categorization.
        
        Args:
            message: Chat message
            
        Returns:
            List of tags
        """
        content = message.content.lower()
        tags = []
        
        tag_mappings = {
            'personal': ['name', 'age', 'birthday', 'address', 'phone', 'email'],
            'work': ['work', 'job', 'office', 'meeting', 'schedule'],
            'location': ['live', 'address', 'city', 'country'],
            'preferences': ['like', 'prefer', 'favorite', 'hate']
        }
        
        for tag, keywords in tag_mappings.items():
            if any(kw in content for kw in keywords):
                tags.append(tag)
        
        return tags
    
    def _add_memory_item(self, item: Dict[str, Any]) -> None:
        """
        Add a memory item to the collection.
        
        Args:
            item: Memory item to add
        """
        self.memory_items.append(item)
        
        # Maintain maximum memory items
        if len(self.memory_items) > self.max_memory_items:
            # Remove oldest items
            self.memory_items = self.memory_items[-self.max_memory_items:]
        
        logger.debug(f"Added memory item: {item['content'][:50]}...")
    
    def get_relevant_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant memories based on a query.
        
        Args:
            query: Search query
            limit: Maximum number of memories to return
            
        Returns:
            List of relevant memory items
        """
        query_lower = query.lower()
        
        # Simple relevance scoring
        scored_memories = []
        for memory in self.memory_items:
            score = 0.0
            content = memory['content'].lower()
            
            # Exact word matches
            query_words = query_lower.split()
            for word in query_words:
                if word in content:
                    score += 1.0
            
            # Tag matches
            for tag in memory.get('tags', []):
                if tag in query_lower:
                    score += 0.5
            
            if score > 0:
                scored_memories.append((score, memory))
        
        # Sort by score and return top results
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [memory for score, memory in scored_memories[:limit]]
    
    def get_memory_summary(self) -> str:
        """
        Generate a summary of stored memories.
        
        Returns:
            Formatted memory summary
        """
        if not self.memory_items:
            return "No memories stored yet."
        
        summary = f"Total memories: {len(self.memory_items)}\n\n"
        
        # Group by tags
        tag_groups = {}
        for memory in self.memory_items:
            for tag in memory.get('tags', ['untagged']):
                if tag not in tag_groups:
                    tag_groups[tag] = []
                tag_groups[tag].append(memory)
        
        for tag, memories in tag_groups.items():
            summary += f"{tag.title()}: {len(memories)} items\n"
        
        return summary
```

#### Web Search Tool (`tools/web_search.py`)
```python
import requests
import logging
from typing import Optional
from config_manager import ConfigManager

logger = logging.getLogger(__name__)

def perform_web_search(query: str) -> str:
    """
    Perform web search using Google Custom Search API.
    
    Args:
        query: Search query string
        
    Returns:
        Formatted search results or error message
    """
    config = ConfigManager()
    config.load_config()
    
    # Get API credentials
    api_key = config.get_api_key("google_search")
    search_engine_id = config.get("api_keys.search_engine_id")
    
    if not api_key:
        return "❌ Search not configured: Missing Google Search API key"
    
    if not search_engine_id:
        return "❌ Search not configured: Missing Search Engine ID"
    
    logger.info(f"Performing web search for: {query}")
    
    try:
        # Google Custom Search API parameters
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": query,
            "num": 5,  # Number of results
            "dateRestrict": "m1",  # Last month only
            "safe": "active"  # Safe search
        }
        
        logger.debug(f"Making request to Google Search API")
        
        # Make API request
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract search information
        search_info = data.get("searchInformation", {})
        total_results = search_info.get("totalResults", "0")
        
        logger.info(f"Search returned {total_results} total results")
        
        items = data.get("items", [])
        
        if not items:
            return f"🔍 No recent results found for '{query}'. Try different keywords."
        
        # Format results
        results = []
        for i, item in enumerate(items[:5], 1):
            title = item.get("title", "No title")
            link = item.get("link", "No link")
            snippet = item.get("snippet", "No description")
            display_link = item.get("displayLink", link)
            
            result = f"""{i}. **{title}**
   📍 {display_link}
   📝 {snippet}
"""
            results.append(result)
        
        header = f"🔍 **Search Results for '{query}'**\nFound {total_results} results (showing top 5)\n\n"
        return header + "\n".join(results) + "\n📅 *Limited to last month*"
        
    except requests.exceptions.Timeout:
        logger.error("Search request timed out")
        return "⏰ Search timeout: Request took too long"
        
    except requests.exceptions.ConnectionError:
        logger.error("Connection error during search")
        return "🔌 Connection error: Cannot connect to search service"
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error during search: {e}")
        if e.response.status_code == 403:
            return "❌ Search API Error (403): Check API key and billing"
        elif e.response.status_code == 400:
            return "❌ Search API Error (400): Invalid request parameters"
        else:
            return f"❌ Search failed with HTTP {e.response.status_code}"
            
    except Exception as e:
        logger.error(f"Unexpected error during search: {e}")
        return f"❌ Search error: {str(e)}"

def search_with_filters(query: str, filters: Optional[dict] = None) -> str:
    """
    Perform advanced web search with additional filters.
    
    Args:
        query: Search query
        filters: Optional filters (date, site, etc.)
        
    Returns:
        Formatted search results
    """
    if not filters:
        return perform_web_search(query)
    
    config = ConfigManager()
    api_key = config.get_api_key("google_search")
    search_engine_id = config.get("api_keys.search_engine_id")
    
    if not api_key or not search_engine_id:
        return "❌ Search configuration incomplete"
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": query,
            "num": 5
        }
        
        # Apply filters
        if 'date_restrict' in filters:
            params['dateRestrict'] = filters['date_restrict']
        if 'site' in filters:
            params['q'] += f" site:{filters['site']}"
        if 'file_type' in filters:
            params['fileType'] = filters['file_type']
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        items = data.get("items", [])
        
        if not items:
            return f"🔍 No results found for '{query}' with applied filters"
        
        results = []
        for i, item in enumerate(items[:5], 1):
            title = item.get("title", "No title")
            link = item.get("link", "No link")
            snippet = item.get("snippet", "No description")
            
            result = f"""{i}. **{title}**
   🔗 {link}
   📝 {snippet}
"""
            results.append(result)
        
        filter_desc = ", ".join([f"{k}: {v}" for k, v in filters.items()])
        header = f"🔍 **Filtered Search Results for '{query}'**\nFilters: {filter_desc}\n\n"
        return header + "\n".join(results)
        
    except Exception as e:
        logger.error(f"Filtered search error: {e}")
        return f"❌ Filtered search failed: {str(e)}"
```

#### Weather Tool (`tools/weather.py`)
```python
import requests
import logging
from typing import Optional, Dict, Any
from config_manager import ConfigManager

logger = logging.getLogger(__name__)

def get_weather_info(location: str) -> str:
    """
    Get weather information for a location using OpenWeatherMap API.
    
    Args:
        location: City name or location string
        
    Returns:
        Formatted weather information or error message
    """
    config = ConfigManager()
    config.load_config()
    
    api_key = config.get_api_key("weather")
    
    if not api_key:
        return "❌ Weather service not configured: Missing OpenWeatherMap API key"
    
    logger.info(f"Getting weather for: {location}")
    
    try:
        # OpenWeatherMap API call
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"  # Celsius
        }
        
        logger.debug("Making request to OpenWeatherMap API")
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract weather data
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        
        weather_main = data.get("weather", [{}])[0].get("main", "Unknown")
        weather_desc = data.get("weather", [{}])[0].get("description", "No description")
        
        temp = data.get("main", {}).get("temp")
        feels_like = data.get("main", {}).get("feels_like")
        humidity = data.get("main", {}).get("humidity")
        pressure = data.get("main", {}).get("pressure")
        
        wind_speed = data.get("wind", {}).get("speed")
        wind_deg = data.get("wind", {}).get("deg")
        
        visibility = data.get("visibility")
        
        # Format response
        weather_report = f"""🌤️ **Weather in {city_name}, {country}**

**Current Conditions:**
- Weather: {weather_main} ({weather_desc.title()})
- Temperature: {temp}°C (Feels like {feels_like}°C)
- Humidity: {humidity}%
- Pressure: {pressure} hPa
- Wind: {wind_speed} m/s"""

        if wind_deg is not None:
            directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                         'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
            wind_dir = directions[round(wind_deg / 22.5) % 16]
            weather_report += f" {wind_dir}"
        
        if visibility:
            visibility_km = visibility / 1000
            weather_report += f"\n- Visibility: {visibility_km} km"
        
        return weather_report
        
    except requests.exceptions.Timeout:
        logger.error("Weather request timed out")
        return "⏰ Weather request timeout"
        
    except requests.exceptions.ConnectionError:
        logger.error("Connection error for weather service")
        return "🔌 Cannot connect to weather service"
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error for weather: {e}")
        if e.response.status_code == 401:
            return "❌ Weather API Error: Invalid API key"
        elif e.response.status_code == 404:
            return f"❌ Location not found: {location}"
        else:
            return f"❌ Weather service error: HTTP {e.response.status_code}"
            
    except Exception as e:
        logger.error(f"Unexpected weather error: {e}")
        return f"❌ Weather error: {str(e)}"

def get_forecast(location: str, days: int = 3) -> str:
    """
    Get weather forecast for multiple days.
    
    Args:
        location: Location string
        days: Number of days for forecast (max 5)
        
    Returns:
        Formatted forecast information
    """
    config = ConfigManager()
    api_key = config.get_api_key("weather")
    
    if not api_key:
        return "❌ Weather forecast not configured"
    
    try:
        url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        city_name = data.get("name", "Unknown")
        forecast_list = data.get("list", [])
        
        if not forecast_list:
            return f"❌ No forecast data available for {location}"
        
        # Group by day
        daily_forecasts = {}
        for item in forecast_list[:days * 8]:  # 8 entries per day (3-hour intervals)
            dt = item.get("dt_txt", "").split(" ")[0]  # Get date part
            if dt not in daily_forecasts:
                daily_forecasts[dt] = []
            daily_forecasts[dt].append(item)
        
        forecast_report = f"🌤️ **{days}-Day Weather Forecast for {city_name}**\n\n"
        
        for date, entries in list(daily_forecasts.items())[:days]:
            # Get daily averages
            temps = [entry["main"]["temp"] for entry in entries]
            avg_temp = sum(temps) / len(temps)
            
            weather_conditions = [entry["weather"][0]["main"] for entry in entries]
            main_condition = max(set(weather_conditions), key=weather_conditions.count)
            
            forecast_report += f"**{date}:**\n"
            forecast_report += f"- Average Temperature: {avg_temp:.1f}°C\n"
            forecast_report += f"- Conditions: {main_condition}\n\n"
        
        return forecast_report
        
    except Exception as e:
        logger.error(f"Forecast error: {e}")
        return f"❌ Forecast error: {str(e)}"
```

#### Prompt Loader (`prompts/loader.py`)
```python
import os
import json
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

async def load_prompts() -> Tuple[str, str]:
    """
    Load dynamic prompts from JSON files.
    
    Returns:
        Tuple of (instructions_prompt, reply_prompt)
    """
    prompts_dir = os.path.dirname(__file__)
    
    # Default prompts
    default_instructions = """You are Winky AI, a helpful and intelligent voice assistant.
You have access to various tools including web search and weather information.
Always be polite, accurate, and engaging in your responses.
Use the available tools when appropriate to provide the best assistance."""

    default_reply = "Hello! I'm Winky AI, your voice assistant. How can I help you today?"
    
    try:
        # Load instructions prompt
        instructions_file = os.path.join(prompts_dir, "instructions.json")
        if os.path.exists(instructions_file):
            with open(instructions_file, 'r', encoding='utf-8') as f:
                instructions_data = json.load(f)
                instructions_prompt = instructions_data.get("prompt", default_instructions)
        else:
            instructions_prompt = default_instructions
            logger.warning("Instructions prompt file not found, using default")
        
        # Load reply prompt
        reply_file = os.path.join(prompts_dir, "reply.json")
        if os.path.exists(reply_file):
            with open(reply_file, 'r', encoding='utf-8') as f:
                reply_data = json.load(f)
                reply_prompt = reply_data.get("prompt", default_reply)
        else:
            reply_prompt = default_reply
            logger.warning("Reply prompt file not found, using default")
            
    except Exception as e:
        logger.error(f"Error loading prompts: {e}")
        instructions_prompt = default_instructions
        reply_prompt = default_reply
    
    return instructions_prompt, reply_prompt

def save_prompt(prompt_type: str, prompt_text: str) -> bool:
    """
    Save a prompt to file.
    
    Args:
        prompt_type: "instructions" or "reply"
        prompt_text: The prompt text to save
        
    Returns:
        True if saved successfully, False otherwise
    """
    prompts_dir = os.path.dirname(__file__)
    
    try:
        if prompt_type not in ["instructions", "reply"]:
            logger.error(f"Invalid prompt type: {prompt_type}")
            return False
        
        filename = f"{prompt_type}.json"
        filepath = os.path.join(prompts_dir, filename)
        
        data = {"prompt": prompt_text}
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Prompt saved: {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving prompt: {e}")
        return False

def get_available_prompts() -> dict:
    """
    Get information about available prompts.
    
    Returns:
        Dictionary with prompt information
    """
    prompts_dir = os.path.dirname(__file__)
    prompts_info = {}
    
    for filename in os.listdir(prompts_dir):
        if filename.endswith('.json'):
            prompt_type = filename.replace('.json', '')
            filepath = os.path.join(prompts_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    prompt_text = data.get("prompt", "")
                    
                prompts_info[prompt_type] = {
                    "file": filename,
                    "length": len(prompt_text),
                    "preview": prompt_text[:100] + "..." if len(prompt_text) > 100 else prompt_text
                }
            except Exception as e:
                logger.error(f"Error reading prompt {filename}: {e}")
    
    return prompts_info
```

### 3. Frontend Development

**Have Gemini create the Next.js frontend with detailed specifications:**

**Project Structure:**
```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Main page
│   ├── globals.css         # Global styles
│   ├── setup/
│   │   └── page.tsx        # Setup/configuration page
│   ├── dashboard/
│   │   └── page.tsx        # Dashboard page
│   └── api/
│       ├── config/
│       │   └── route.ts    # Configuration API
│       └── connection-details/
│           └── route.ts    # Connection details API
├── components/
│   ├── layout.tsx          # Main layout component
│   ├── page.tsx            # Page wrapper
│   ├── Container.tsx       # Container component
│   ├── Tabs.tsx            # Tab navigation
│   ├── ui/                 # UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── label.tsx
│   │   ├── select.tsx
│   │   ├── card.tsx
│   │   └── alert.tsx
│   ├── livekit/            # LiveKit components
│   │   ├── agent-tile.tsx
│   │   ├── avatar-tile.tsx
│   │   ├── media-tiles.tsx
│   │   ├── video-tile.tsx
│   │   ├── device-select.tsx
│   │   ├── track-toggle.tsx
│   │   ├── chat/           # Chat components
│   │   │   ├── chat-entry.tsx
│   │   │   ├── chat-input.tsx
│   │   │   └── chat-message-view.tsx
│   │   └── agent-control-bar/
│   │       ├── agent-control-bar.tsx
│   │       ├── hooks/
│   │       │   ├── use-agent-control-bar.ts
│   │       │   └── use-publish-permissions.ts
│   ├── SuperSearchDashboard.tsx
│   ├── theme-toggle.tsx
│   ├── welcome.tsx
│   └── alert-toast.tsx
├── lib/
│   ├── types.ts            # TypeScript types
│   └── utils.ts            # Utility functions
├── hooks/
│   └── useChatAndTranscription.ts
├── public/                 # Static assets
└── package.json
```

**Main Application Layout (`app/layout.tsx`):**
```tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { ThemeProvider } from '@/components/theme-provider'
import { Toaster } from '@/components/ui/sonner'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Winky AI Voice Assistant',
  description: 'Conversational AI voice assistant with real-time communication',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  )
}
```

**Main Page (`app/page.tsx`):**
```tsx
'use client'

import { useState, useEffect } from 'react'
import { Container } from '@/components/Container'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/Tabs'
import { Welcome } from '@/components/welcome'
import { SuperSearchDashboard } from '@/components/SuperSearchDashboard'
import { SetupPage } from './setup/page'
import { DashboardPage } from './dashboard/page'

export default function Home() {
  const [activeTab, setActiveTab] = useState('welcome')
  const [isConfigured, setIsConfigured] = useState(false)

  useEffect(() => {
    // Check if the app is configured
    checkConfiguration()
  }, [])

  const checkConfiguration = async () => {
    try {
      const response = await fetch('/api/config')
      const config = await response.json()
      setIsConfigured(config.isConfigured)
    } catch (error) {
      console.error('Failed to check configuration:', error)
    }
  }

  if (!isConfigured) {
    return <SetupPage onConfigured={() => setIsConfigured(true)} />
  }

  return (
    <Container>
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="welcome">Welcome</TabsTrigger>
          <TabsTrigger value="voice">Voice Assistant</TabsTrigger>
          <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
        </TabsList>

        <TabsContent value="welcome">
          <Welcome onGetStarted={() => setActiveTab('voice')} />
        </TabsContent>

        <TabsContent value="voice">
          <VoiceAssistantInterface />
        </TabsContent>

        <TabsContent value="dashboard">
          <DashboardPage />
        </TabsContent>
      </Tabs>
    </Container>
  )
}
```

**Voice Assistant Interface Component:**
```tsx
'use client'

import { useState, useEffect, useRef } from 'react'
import { Room, RoomEvent, Track } from 'livekit-client'
import { LiveKitRoom, VideoConference } from '@livekit/components-react'
import '@livekit/components-styles'
import { useChatAndTranscription } from '@/hooks/useChatAndTranscription'
import { AgentControlBar } from '@/components/livekit/agent-control-bar/agent-control-bar'
import { ChatMessageView } from '@/components/livekit/chat/chat-message-view'
import { DeviceSelect } from '@/components/livekit/device-select'
import { MediaTiles } from '@/components/livekit/media-tiles'

interface VoiceAssistantInterfaceProps {
  onConnectionStateChange?: (connected: boolean) => void
}

export function VoiceAssistantInterface({ onConnectionStateChange }: VoiceAssistantInterfaceProps) {
  const [room, setRoom] = useState<Room | null>(null)
  const [connectionDetails, setConnectionDetails] = useState<any>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const {
    messages,
    isTranscribing,
    sendMessage,
    clearMessages
  } = useChatAndTranscription(room)

  useEffect(() => {
    fetchConnectionDetails()
  }, [])

  const fetchConnectionDetails = async () => {
    try {
      const response = await fetch('/api/connection-details')
      if (!response.ok) {
        throw new Error('Failed to fetch connection details')
      }
      const details = await response.json()
      setConnectionDetails(details)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to connect')
    }
  }

  const handleConnect = async () => {
    if (!connectionDetails) return

    try {
      const newRoom = new Room()
      
      // Set up event listeners
      newRoom.on(RoomEvent.Connected, () => {
        setIsConnected(true)
        onConnectionStateChange?.(true)
      })
      
      newRoom.on(RoomEvent.Disconnected, () => {
        setIsConnected(false)
        onConnectionStateChange?.(false)
      })
      
      newRoom.on(RoomEvent.ConnectionStateChanged, (state) => {
        console.log('Connection state:', state)
      })

      // Connect to room
      await newRoom.connect(connectionDetails.serverUrl, connectionDetails.token)
      setRoom(newRoom)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Connection failed')
    }
  }

  const handleDisconnect = () => {
    if (room) {
      room.disconnect()
      setRoom(null)
      setIsConnected(false)
      onConnectionStateChange?.(false)
    }
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] space-y-4">
        <div className="text-red-500 text-center">
          <h3 className="text-lg font-semibold">Connection Error</h3>
          <p>{error}</p>
        </div>
        <button
          onClick={fetchConnectionDetails}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Retry
        </button>
      </div>
    )
  }

  if (!connectionDetails) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-2">Loading connection details...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* Connection Controls */}
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center space-x-4">
          <DeviceSelect />
          {!isConnected ? (
            <button
              onClick={handleConnect}
              className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
            >
              Connect
            </button>
          ) : (
            <button
              onClick={handleDisconnect}
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Disconnect
            </button>
          )}
        </div>
        
        <div className="text-sm text-gray-600">
          Status: {isConnected ? 'Connected' : 'Disconnected'}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Video/Media Area */}
        <div className="flex-1 p-4">
          {isConnected && room ? (
            <LiveKitRoom room={room} connect={false}>
              <MediaTiles />
              <AgentControlBar />
            </LiveKitRoom>
          ) : (
            <div className="flex items-center justify-center h-full bg-gray-100 rounded-lg">
              <p className="text-gray-500">Connect to start voice interaction</p>
            </div>
          )}
        </div>

        {/* Chat Sidebar */}
        <div className="w-80 border-l flex flex-col">
          <div className="p-4 border-b">
            <h3 className="font-semibold">Chat</h3>
            {isTranscribing && (
              <p className="text-sm text-blue-500 mt-1">Transcribing...</p>
            )}
          </div>
          
          <div className="flex-1 overflow-y-auto">
            <ChatMessageView messages={messages} />
          </div>
          
          <div className="p-4 border-t">
            <ChatInput onSendMessage={sendMessage} disabled={!isConnected} />
          </div>
        </div>
      </div>
    </div>
  )
}
```

**Configuration API (`app/api/config/route.ts`):**
```typescript
import { NextRequest, NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

const CONFIG_PATH = path.join(process.cwd(), '..', 'config', 'user_config.json')

export async function GET() {
  try {
    if (!fs.existsSync(CONFIG_PATH)) {
      return NextResponse.json({
        isConfigured: false,
        message: 'Configuration not found'
      })
    }

    const configData = fs.readFileSync(CONFIG_PATH, 'utf-8')
    const config = JSON.parse(configData)

    // Check if essential configuration exists
    const isConfigured = !!(
      config.api_keys?.livekit_url &&
      config.api_keys?.livekit_key &&
      config.api_keys?.livekit_secret &&
      config.api_keys?.google
    )

    return NextResponse.json({
      isConfigured,
      config: isConfigured ? config : null
    })
  } catch (error) {
    console.error('Config API error:', error)
    return NextResponse.json(
      { error: 'Failed to read configuration' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const config = await request.json()

    // Ensure config directory exists
    const configDir = path.dirname(CONFIG_PATH)
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true })
    }

    // Write configuration
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2))

    return NextResponse.json({
      success: true,
      message: 'Configuration saved successfully'
    })
  } catch (error) {
    console.error('Config save error:', error)
    return NextResponse.json(
      { error: 'Failed to save configuration' },
      { status: 500 }
    )
  }
}
```

**Connection Details API (`app/api/connection-details/route.ts`):**
```typescript
import { NextRequest, NextResponse } from 'next/server'
import { AccessToken } from 'livekit-server-sdk'
import fs from 'fs'
import path from 'path'

const CONFIG_PATH = path.join(process.cwd(), '..', 'config', 'user_config.json')

export async function GET() {
  try {
    if (!fs.existsSync(CONFIG_PATH)) {
      return NextResponse.json(
        { error: 'Configuration not found' },
        { status: 404 }
      )
    }

    const configData = fs.readFileSync(CONFIG_PATH, 'utf-8')
    const config = JSON.parse(configData)

    const livekitUrl = config.api_keys?.livekit_url
    const apiKey = config.api_keys?.livekit_key
    const apiSecret = config.api_keys?.livekit_secret

    if (!livekitUrl || !apiKey || !apiSecret) {
      return NextResponse.json(
        { error: 'LiveKit credentials not configured' },
        { status: 400 }
      )
    }

    // Create access token
    const at = new AccessToken(apiKey, apiSecret, {
      identity: `user_${Date.now()}`,
      name: config.user?.full_name || 'User'
    })

    at.addGrant({
      roomJoin: true,
      room: 'voice-assistant-room',
      canPublish: true,
      canSubscribe: true
    })

    const token = at.toJwt()

    return NextResponse.json({
      serverUrl: livekitUrl,
      token: token,
      roomName: 'voice-assistant-room'
    })
  } catch (error) {
    console.error('Connection details API error:', error)
    return NextResponse.json(
      { error: 'Failed to generate connection details' },
      { status: 500 }
    )
  }
}
```

### 4. Configuration System

**JSON Configuration Structure:**
```json
{
  "api_keys": {
    "google": "your_gemini_api_key_here",
    "livekit_url": "https://your-project.livekit.cloud",
    "livekit_key": "your_livekit_api_key",
    "livekit_secret": "your_livekit_api_secret",
    "google_search": "your_google_custom_search_api_key",
    "search_engine_id": "your_custom_search_engine_id",
    "weather": "your_openweathermap_api_key",
    "mem0": "your_mem0_api_key_optional"
  },
  "llm": {
    "provider": "google",
    "model": "gemini-2.5-flash-native-audio-preview-09-2025",
    "voice": "Puck",
    "temperature": 0.7,
    "max_tokens": 1000
  },
  "user": {
    "id": "unique_user_id_123",
    "full_name": "John Doe",
    "preferences": {
      "theme": "dark",
      "language": "en",
      "timezone": "America/New_York"
    }
  },
  "features": {
    "memory_enabled": true,
    "web_search_enabled": true,
    "weather_enabled": true,
    "voice_enabled": true,
    "transcription_enabled": true
  },
  "performance": {
    "max_memory_items": 100,
    "search_results_limit": 5,
    "audio_sample_rate": 16000,
    "video_quality": "720p"
  },
  "logging": {
    "level": "INFO",
    "file_logging": true,
    "console_logging": true,
    "log_retention_days": 30
  }
}
```

### 5. Tools and Features

**Advanced Search Integration:**
```python
# tools/advanced_search.py
import asyncio
import logging
from typing import List, Dict, Any, Optional
from .web_search import perform_web_search, search_with_filters
from .memory import MemoryExtractor

logger = logging.getLogger(__name__)

class AdvancedSearch:
    """
    Advanced search functionality combining multiple sources
    and intelligent result processing.
    """
    
    def __init__(self):
        self.memory_extractor = MemoryExtractor()
        self.search_history: List[Dict[str, Any]] = []
    
    async def comprehensive_search(self, query: str, context: Optional[Dict[str, str]] = None) -> str:
        """
        Perform comprehensive search with context awareness.
        
        Args:
            query: Search query
            context: Additional context (user preferences, location, etc.)
            
        Returns:
            Formatted comprehensive search results
        """
        logger.info(f"Performing comprehensive search for: {query}")
        
        # Check memory for relevant information first
        memory_results = self.memory_extractor.get_relevant_memories(query, limit=3)
        
        # Perform web search
        web_results = perform_web_search(query)
        
        # Apply context filters if available
        if context:
            web_results = self._apply_context_filters(web_results, context)
        
        # Combine and rank results
        combined_results = self._combine_results(memory_results, web_results, query)
        
        # Store search in history
        self._store_search_history(query, combined_results)
        
        return combined_results
    
    def _apply_context_filters(self, results: str, context: Dict[str, str]) -> str:
        """
        Apply context-based filters to search results.
        
        Args:
            results: Raw search results
            context: Context filters
            
        Returns:
            Filtered results
        """
        # Implementation for context filtering
        # (location, time, user preferences, etc.)
        return results
    
    def _combine_results(self, memory_results: List[Dict], web_results: str, query: str) -> str:
        """
        Combine memory and web results intelligently.
        
        Args:
            memory_results: Results from memory
            web_results: Results from web search
            query: Original query
            
        Returns:
            Combined formatted results
        """
        combined = f"🔍 **Comprehensive Search Results for '{query}'**\n\n"
        
        # Add memory results if available
        if memory_results:
            combined += "**From Memory:**\n"
            for i, memory in enumerate(memory_results, 1):
                content = memory.get('content', '')[:200]
                combined += f"{i}. {content}...\n"
            combined += "\n"
        
        # Add web results
        combined += "**From Web:**\n"
        combined += web_results
        
        return combined
    
    def _store_search_history(self, query: str, results: str) -> None:
        """
        Store search in history for analytics and improvement.
        
        Args:
            query: Search query
            results: Search results
        """
        search_entry = {
            'timestamp': asyncio.get_event_loop().time(),
            'query': query,
            'results_count': results.count('\n') if results else 0,
            'success': bool(results and '❌' not in results)
        }
        
        self.search_history.append(search_entry)
        
        # Keep only last 100 searches
        if len(self.search_history) > 100:
            self.search_history = self.search_history[-100:]

def advanced_search(query: str) -> str:
    """
    Main advanced search function for the voice assistant.
    
    Args:
        query: Search query from user
        
    Returns:
        Formatted search results
    """
    search_engine = AdvancedSearch()
    
    try:
        # Run in new event loop if needed
        if asyncio.iscoroutinefunction(search_engine.comprehensive_search):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(search_engine.comprehensive_search(query))
            loop.close()
        else:
            result = search_engine.comprehensive_search(query)
        
        return result
    except Exception as e:
        logger.error(f"Advanced search error: {e}")
        # Fallback to basic search
        return perform_web_search(query)
```

### 6. Deployment and Testing

**Local Development Setup:**
```bash
# Backend setup
cd WinkyAI-Replica/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy configuration template
cp ../config/user_config.json.example ../config/user_config.json
# Edit user_config.json with your API keys

# Start backend
python agent.py dev

# Frontend setup (new terminal)
cd ../frontend
npm install
npm run dev
```

**Environment Variables (.env.local):**
```bash
# Frontend environment variables
NEXT_PUBLIC_LIVEKIT_URL=your_livekit_url
NEXT_PUBLIC_DEFAULT_ROOM=voice-assistant-room

# Optional: Analytics and monitoring
NEXT_PUBLIC_ANALYTICS_ID=your_analytics_id
NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn
```

**Docker Configuration:**
```dockerfile
# Dockerfile for backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port (if needed for health checks)
EXPOSE 8080

# Run the agent
CMD ["python", "agent.py"]
```

**Docker Compose for Full Stack:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    environment:
      - LIVEKIT_URL=${LIVEKIT_URL}
      - LIVEKIT_API_KEY=${LIVEKIT_API_KEY}
      - LIVEKIT_API_SECRET=${LIVEKIT_API_SECRET}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_LIVEKIT_URL=${LIVEKIT_URL}
    depends_on:
      - backend
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

### 7. Advanced Features

**Real-time Transcription:**
```typescript
// hooks/useTranscription.ts
import { useState, useEffect, useRef } from 'react'
import { Room, RoomEvent, Track } from 'livekit-client'

export function useTranscription(room: Room | null) {
  const [transcription, setTranscription] = useState('')
  const [isTranscribing, setIsTranscribing] = useState(false)
  const transcriptionRef = useRef('')

  useEffect(() => {
    if (!room) return

    const handleTranscription = (data: any) => {
      const text = data.transcription || ''
      transcriptionRef.current += text + ' '
      setTranscription(transcriptionRef.current)
    }

    room.on(RoomEvent.TranscriptionReceived, handleTranscription)

    return () => {
      room.off(RoomEvent.TranscriptionReceived, handleTranscription)
    }
  }, [room])

  const clearTranscription = () => {
    transcriptionRef.current = ''
    setTranscription('')
  }

  return {
    transcription,
    isTranscribing,
    clearTranscription
  }
}
```

**Voice Activity Detection:**
```python
# tools/voice_activity.py
import numpy as np
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class VoiceActivityDetector:
    """
    Voice Activity Detection using energy-based methods.
    """
    
    def __init__(self, sample_rate: int = 16000, frame_duration: float = 0.025):
        self.sample_rate = sample_rate
        self.frame_length = int(sample_rate * frame_duration)
        self.energy_threshold = 0.01  # Adjust based on environment
        self.silence_frames = 0
        self.voice_frames = 0
        
    def is_voice_active(self, audio_data: np.ndarray) -> bool:
        """
        Determine if voice activity is present in audio frame.
        
        Args:
            audio_data: Audio frame data
            
        Returns:
            True if voice activity detected
        """
        # Calculate RMS energy
        energy = np.sqrt(np.mean(audio_data ** 2))
        
        # Simple energy-based VAD
        is_active = energy > self.energy_threshold
        
        # Update counters
        if is_active:
            self.voice_frames += 1
            self.silence_frames = 0
        else:
            self.silence_frames += 1
            self.voice_frames = 0
        
        return is_active
    
    def reset(self):
        """Reset VAD state"""
        self.silence_frames = 0
        self.voice_frames = 0
    
    def adjust_threshold(self, audio_sample: np.ndarray):
        """
        Dynamically adjust energy threshold based on background noise.
        
        Args:
            audio_sample: Background audio sample
        """
        background_energy = np.sqrt(np.mean(audio_sample ** 2))
        self.energy_threshold = background_energy * 1.5  # 1.5x background noise
        logger.info(f"Adjusted VAD threshold to: {self.energy_threshold}")
```

**Custom UI Themes:**
```typescript
// components/theme-provider.tsx
'use client'

import * as React from 'react'
import { ThemeProvider as NextThemesProvider } from 'next-themes'
import { type ThemeProviderProps } from 'next-themes/dist/types'

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>
}

// themes.ts
export const themes = {
  light: {
    background: '#ffffff',
    foreground: '#000000',
    primary: '#3b82f6',
    secondary: '#64748b',
    accent: '#f1f5f9'
  },
  dark: {
    background: '#0f172a',
    foreground: '#f8fafc',
    primary: '#60a5fa',
    secondary: '#94a3b8',
    accent: '#1e293b'
  },
  neon: {
    background: '#000000',
    foreground: '#00ff41',
    primary: '#00ff41',
    secondary: '#008f11',
    accent: '#003300'
  }
}
```

## Gemini Prompting Strategies

### Effective Prompts for Replication:

1. **Architecture Planning:**
```
Design a voice AI assistant architecture using LiveKit and Gemini with the following components: [list components]
```

2. **Code Generation:**
```
Generate Python code for a LiveKit agent that uses Gemini realtime API with voice capabilities and tool integration
```

3. **Frontend Components:**
```
Create React components for a LiveKit voice chat interface with video tiles, chat messages, and device controls
```

4. **Integration:**
```
Write code to integrate Google Custom Search API as a tool in a LiveKit agent
```

## Troubleshooting Common Issues

### Backend Issues:
- Ensure Python version compatibility
- Check API key configurations
- Verify LiveKit credentials

### Frontend Issues:
- Confirm LiveKit client version matches server
- Check WebRTC permissions
- Verify token server configuration

### Audio/Video Issues:
- Test microphone/camera permissions
- Check network connectivity
- Verify codec support

## Customization Options

### Voice Configuration:
- Choose different Gemini voices
- Adjust speech parameters
- Add voice cloning capabilities

### UI Themes:
- Dark/light mode toggle
- Custom color schemes
- Responsive design adjustments

### Feature Extensions:
- Add file upload capabilities
- Integrate calendar functions
- Implement task management

## Security Considerations

- Store API keys securely (environment variables)
- Implement token-based authentication
- Use HTTPS in production
- Regular security audits

## Performance Optimization

- Implement connection pooling
- Optimize audio/video encoding
- Cache frequent API responses
- Monitor resource usage

## Future Enhancements

- Multi-modal inputs (text, voice, image)
- Advanced conversation memory
- Integration with external services
- Mobile app development
- Cloud deployment options

---

**Note:** This guide provides a comprehensive overview for replicating the Winky AI project. Use Gemini AI to generate specific code implementations based on your requirements and the architecture outlined above.</content>
<parameter name="filePath">/workspaces/upgraded-WinkyTalk/ReplicationGuide/HowToReplicateWithGemini.md</content>
<parameter name="filePath">/workspaces/upgraded-WinkyTalk/ReplicationGuide/HowToReplicateWithGemini.md