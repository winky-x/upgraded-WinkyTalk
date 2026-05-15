import os
import requests
import logging
from dotenv import load_dotenv
from livekit.agents import function_tool  # ✅ Correct decorator
from datetime import datetime
from livekit import agents
from config_manager import ConfigManager

config = ConfigManager()

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import os
import requests
import logging
from livekit.agents import function_tool


logger = logging.getLogger(__name__)

@function_tool
async def google_search(query: str) -> str:
    """
    Perform a web search using DuckDuckGo API for instant answers.
    Returns relevant search results.
    """

    logger.info(f"Query प्राप्त हुई: {query}")

    if not query or query.strip() == "":
        return "Please provide a search query."

    try:
        # Use DuckDuckGo Instant Answer API with User-Agent header
        logger.info("Searching DuckDuckGo for: " + query)
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, params=params, headers=headers, timeout=10)
        logger.info(f"DuckDuckGo response status: {response.status_code}")
        
        if response.status_code in [200, 202]:  # Both OK and Accepted are valid
            data = response.json()
            
            results = []
            
            # Get abstract (main answer)
            if data.get("Abstract"):
                heading = data.get("Heading", "Result")
                abstract = data.get("Abstract", "")
                results.append(f"**{heading}**\n{abstract}")
            
            # Get direct answer
            if data.get("Answer") and not data.get("Abstract"):
                results.append(f"Answer: {data.get('Answer')}")
            
            # Get related topics
            related = data.get("RelatedTopics", [])
            for item in related[:2]:
                if isinstance(item, dict) and item.get("Text"):
                    results.append(item.get("Text"))
            
            if results:
                formatted = "Here are the search results:\n\n"
                for i, result in enumerate(results[:3], 1):
                    formatted += f"{i}. {result}\n\n"
                logger.info(f"Returning {len(results)} results")
                return formatted.strip()
                
    except Exception as e:
        logger.error(f"DuckDuckGo search failed: {e}")

    return f"Could not find results for '{query}'. Please try a different search term."


async def get_current_datetime() -> str:
    """
    Returns the current date and time in a human-readable format.

    Use this tool when the user asks for the current time, date, or wants to know what day it is.
    Example prompts:
    - "अब क्या time हो रहा है?"
    - "आज की तारीख क्या है?"
    - "What’s the time right now?"
    """

    now = datetime.now()
    formatted = now.strftime("%d %B %Y, %I:%M %p")  # Example: 31 July 2025, 04:22 PM
    return formatted;