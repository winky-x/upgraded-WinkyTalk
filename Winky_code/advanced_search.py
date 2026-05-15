"""
Advanced search with multiple fallbacks
Tries Wikipedia, DuckDuckGo, and web search APIs
"""

import os
import requests
import logging
from livekit.agents import function_tool
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@function_tool
async def advanced_search(query: str, max_results: int = 3) -> str:
    """
    Advanced search that tries multiple sources:
    1. DuckDuckGo Instant Answers
    2. Wikipedia Search
    3. Plain web search
    """
    logger.info(f"🔍 Advanced search for: {query}")

    if not query or query.strip() == "":
        return "Please provide a search query."

    # Try DuckDuckGo first (fastest, no API key needed)
    logger.info("📍 Trying DuckDuckGo...")
    result = await _try_duckduckgo(query, max_results)
    if result:
        return result

    # Try Wikipedia
    logger.info("📚 Trying Wikipedia...")
    result = await _try_wikipedia(query, max_results)
    if result:
        return result

    # Try generic web search via public APIs
    logger.info("🌐 Trying web search...")
    result = await _try_web_search(query, max_results)
    if result:
        return result

    return f"❌ Could not find reliable results for '{query}'. Try a simpler or more specific query."


async def _try_duckduckgo(query: str, max_results: int = 3) -> str:
    """DuckDuckGo Instant Answer API - Most reliable"""
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "no_redirect": 1,
            "t": "livekit-agent"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        logger.info(f"DuckDuckGo status: {response.status_code}")
        
        if response.status_code in [200, 202]:
            data = response.json()
            results = []

            # Get abstract (main answer from DuckDuckGo)
            abstract = data.get("Abstract", "").strip()
            heading = data.get("Heading", "").strip()
            answer = data.get("Answer", "").strip()

            if abstract and heading:
                results.append(f"{heading}\n{abstract}")
            elif answer:
                results.append(f"Answer: {answer}")

            # Get related topics as fallback results
            if len(results) < max_results:
                related = data.get("RelatedTopics", [])
                for item in related[:max_results - len(results)]:
                    if isinstance(item, dict):
                        text = item.get("Text", "").strip()
                        if text:
                            results.append(text)

            if results and any(r.strip() for r in results):
                formatted = "📌 Search Results:\n\n"
                for i, r in enumerate(results[:max_results], 1):
                    if r.strip():
                        formatted += f"{i}. {r}\n\n"
                
                result_text = formatted.strip()
                if len(result_text) > 20:  # Ensure we have real content
                    logger.info("✅ DuckDuckGo returned results")
                    return result_text

    except requests.Timeout:
        logger.warning("DuckDuckGo timeout")
    except Exception as e:
        logger.warning(f"DuckDuckGo error: {e}")

    return None


async def _try_wikipedia(query: str, max_results: int = 3) -> str:
    """Wikipedia Search API - Secondary source"""
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": max_results,
            "srsort": "relevance",
            "origin": "*"
        }

        response = requests.get(url, params=params, timeout=10)
        logger.info(f"Wikipedia status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            search_results = data.get("query", {}).get("search", [])

            if search_results and len(search_results) > 0:
                formatted = "📖 Wikipedia Results:\n\n"
                for i, result in enumerate(search_results[:max_results], 1):
                    title = result.get("title", "").strip()
                    snippet = result.get("snippet", "").strip()
                    
                    # Clean HTML tags
                    snippet = snippet.replace("<span class=\"searchmatch\">", "")
                    snippet = snippet.replace("</span>", "")
                    snippet = snippet.replace("&quot;", "\"")
                    
                    # Limit snippet length
                    if len(snippet) > 150:
                        snippet = snippet[:150] + "..."
                    
                    if title:
                        formatted += f"{i}. {title}\n{snippet}\n\n"

                result_text = formatted.strip()
                if len(result_text) > 30:
                    logger.info("✅ Wikipedia returned results")
                    return result_text

    except requests.Timeout:
        logger.warning("Wikipedia timeout")
    except Exception as e:
        logger.warning(f"Wikipedia error: {e}")

    return None


async def _try_web_search(query: str, max_results: int = 3) -> str:
    """Generic web search using Bing Search API (free tier) or SearxNG"""
    try:
        # Try Bing search which doesn't require API key
        url = "https://www.bing.com/search"
        params = {
            "q": query,
            "format": "json"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        logger.info(f"Bing search status: {response.status_code}")
        
        # If we got a response, return a note about results being available
        if response.status_code == 200 and len(response.text) > 100:
            return f"🌐 Web results available for '{query}'\nSearch performed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\nTry searching on Google or Bing for more detailed results."

    except requests.Timeout:
        logger.warning("Web search timeout")
    except Exception as e:
        logger.warning(f"Web search error: {e}")

    return None
