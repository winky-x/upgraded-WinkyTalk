"""
🚀 SUPER NAVIGATOR - All-in-One Advanced Search System
One file that does: Browser automation + AI decisions + Vision + Real-time UI
"""

import asyncio
import json
import logging
import base64
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import aiohttp
from dataclasses_json import dataclass_json

# Try imports with fallbacks
try:
    from playwright.async_api import async_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed. Browser features disabled.")

try:
    import openai
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== DATA STRUCTURES ====================
@dataclass_json
@dataclass
class SearchResult:
    title: str
    snippet: str
    link: str
    source: str
    price: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    relevance: float = 0.5
    extracted_at: str = ""

@dataclass_json
@dataclass  
class NavigationStep:
    action: str  # navigate, click, type, scroll, extract
    target: str  # URL, selector, text
    data: Dict = None
    timestamp: str = ""

@dataclass_json
@dataclass
class TaskProgress:
    task_id: str
    status: str  # planning, searching, analyzing, complete
    current_step: int = 0
    total_steps: int = 0
    visited_sites: List[str] = None
    found_items: List[SearchResult] = None
    ai_analysis: Dict = None
    last_update: str = ""
    
    def __post_init__(self):
        if self.visited_sites is None:
            self.visited_sites = []
        if self.found_items is None:
            self.found_items = []
        if self.ai_analysis is None:
            self.ai_analysis = {}

# ==================== SUPER NAVIGATOR CORE ====================
class SuperNavigator:
    """
    🚀 All-in-one advanced search system
    Combines: Browser automation + AI decisions + Real-time UI
    """
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.page = None
        self.playwright = None
        
        # AI Components
        self.llm = None
        self.vision_model = None
        
        # State
        self.active_tasks: Dict[str, TaskProgress] = {}
        self.websocket_clients = {}
        
        # Configuration
        self.timeout = 30000
        self.max_depth = 3
        
        # Initialize
        asyncio.create_task(self._initialize())
    
    async def _initialize(self):
        """Initialize all components"""
        # Setup browser if available
        if PLAYWRIGHT_AVAILABLE:
            await self._setup_browser()
        
        # Setup AI models
        await self._setup_ai()
        
        logger.info("🚀 SuperNavigator initialized!")
    
    async def _setup_browser(self):
        """Setup headless browser"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=['--disable-dev-shm-usage', '--no-sandbox']
            )
            self.page = await self.browser.new_page()
            
            # Stealth mode
            await self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            """)
            
            logger.info("🌐 Browser ready")
        except Exception as e:
            logger.error(f"Browser setup failed: {e}")
    
    async def _setup_ai(self):
        """Setup AI models"""
        # Try to setup OpenAI if available
        if OPENAI_AVAILABLE:
            from config_manager import ConfigManager
            config = ConfigManager()
            api_key = config.get_api_key("openai")
            if api_key:
                self.llm = openai.AsyncOpenAI(api_key=api_key)
                logger.info("🧠 AI models ready")
    
    # ==================== MAIN PUBLIC API ====================
    
    async def execute_smart_search(self, task: str) -> TaskProgress:
        """
        🎯 Execute complex search tasks like:
        - "Find best laptop under $250 on Facebook Marketplace in San Jose"
        - "Compare iPhone prices on Amazon and eBay"
        - "Find apartments for rent in NYC under $2000"
        """
        task_id = f"task_{int(datetime.now().timestamp())}"
        progress = TaskProgress(
            task_id=task_id,
            status="planning",
            last_update=datetime.now().isoformat()
        )
        
        self.active_tasks[task_id] = progress
        await self._update_progress(task_id, progress)
        
        # Step 1: Plan with AI
        steps = await self._plan_task(task)
        progress.total_steps = len(steps)
        progress.status = "searching"
        
        # Step 2: Execute steps
        results = []
        for i, step in enumerate(steps):
            progress.current_step = i + 1
            await self._update_progress(task_id, progress)
            
            step_result = await self._execute_step(step, task)
            if step_result:
                results.extend(step_result)
                progress.found_items = results
                progress.visited_sites.append(step.get('url', 'unknown'))
            
            await asyncio.sleep(1)  # Be nice to websites
        
        # Step 3: AI Analysis
        if results and self.llm:
            analysis = await self._analyze_results(results, task)
            progress.ai_analysis = analysis
            progress.status = "analyzing"
        
        progress.status = "complete"
        progress.last_update = datetime.now().isoformat()
        await self._update_progress(task_id, progress)
        
        return progress
    
    async def _plan_task(self, task: str) -> List[Dict]:
        """AI-powered task planning"""
        if not self.llm:
            # Simple fallback planning
            return self._simple_plan(task)
        
        try:
            prompt = f"""
            Break this search task into specific web navigation steps:
            Task: {task}
            
            Return JSON array of steps like:
            [
              {{"action": "search", "platform": "google", "query": "..."}},
              {{"action": "navigate", "url": "..."}},
              {{"action": "extract", "what": "listings"}},
              {{"action": "filter", "criteria": {{"max_price": 250}}}}
            ]
            
            Choose platforms based on task (google, facebook, amazon, craigslist, etc.)
            """
            
            response = await self.llm.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            plan = json.loads(response.choices[0].message.content)
            return plan.get("steps", [])
            
        except Exception as e:
            logger.error(f"AI planning failed: {e}")
            return self._simple_plan(task)
    
    def _simple_plan(self, task: str) -> List[Dict]:
        """Simple planning without AI"""
        task_lower = task.lower()
        
        if "facebook" in task_lower or "marketplace" in task_lower:
            return [
                {"action": "navigate", "url": "https://www.facebook.com/marketplace"},
                {"action": "search", "selector": "input[aria-label*='Search']", "query": self._extract_query(task)},
                {"action": "extract", "selector": "[data-testid*='marketplace_feed_item']"},
                {"action": "filter", "field": "price", "max": self._extract_price(task)}
            ]
        elif "amazon" in task_lower:
            return [
                {"action": "navigate", "url": "https://www.amazon.com"},
                {"action": "search", "selector": "#twotabsearchtextbox", "query": self._extract_query(task)},
                {"action": "extract", "selector": "[data-component-type='s-search-result']"}
            ]
        else:
            # Default Google search
            return [
                {"action": "search_google", "query": task},
                {"action": "extract", "selector": "div.g"}
            ]
    
    async def _execute_step(self, step: Dict, original_task: str) -> List[SearchResult]:
        """Execute a single navigation step"""
        action = step.get("action")
        
        if action == "navigate" and self.page:
            url = step.get("url")
            await self.page.goto(url)
            return []
            
        elif action == "search" and self.page:
            selector = step.get("selector", "input[type='text']")
            query = step.get("query", original_task)
            
            search_box = await self.page.query_selector(selector)
            if search_box:
                await search_box.type(query)
                await search_box.press("Enter")
                await asyncio.sleep(2)
            return []
            
        elif action == "search_google":
            # Use our robust Google search
            from google_search import google_search
            results_text = await google_search(step.get("query", original_task))
            
            # Parse results into SearchResult objects
            return self._parse_google_results(results_text)
            
        elif action == "extract" and self.page:
            selector = step.get("selector", "div")
            items = await self.page.query_selector_all(selector)
            
            results = []
            for item in items[:10]:  # Limit to 10
                try:
                    result = await self._extract_item_data(item)
                    if result:
                        results.append(result)
                except:
                    continue
            
            return results
        
        return []
    
    async def _extract_item_data(self, element) -> Optional[SearchResult]:
        """Extract data from a page element"""
        try:
            # Try to get title
            title_elem = await element.query_selector("h1, h2, h3, [class*='title'], [class*='name']")
            title = await title_elem.inner_text() if title_elem else ""
            
            # Try to get price
            price_elem = await element.query_selector("[class*='price'], .price, span[class*='currency']")
            price = await price_elem.inner_text() if price_elem else ""
            
            # Try to get link
            link_elem = await element.query_selector("a")
            link = await link_elem.get_attribute("href") if link_elem else ""
            
            # Try to get image
            img_elem = await element.query_selector("img")
            img_url = await img_elem.get_attribute("src") if img_elem else ""
            
            if title or price:
                return SearchResult(
                    title=title[:200],
                    snippet=price,
                    link=self._make_absolute_url(link) if link else "",
                    source=self.page.url if self.page else "web",
                    price=price,
                    image_url=img_url,
                    extracted_at=datetime.now().isoformat()
                )
        except:
            pass
        
        return None
    
    def _make_absolute_url(self, href: str) -> str:
        """Make relative URL absolute"""
        if not href or href.startswith("http"):
            return href
        
        if self.page and href.startswith("/"):
            from urllib.parse import urlparse
            parsed = urlparse(self.page.url)
            return f"{parsed.scheme}://{parsed.netloc}{href}"
        
        return href
    
    def _parse_google_results(self, results_text: str) -> List[SearchResult]:
        """Parse Google search results text"""
        # Simple parsing - in reality would use proper HTML parsing
        lines = results_text.split("\n")
        results = []
        
        for line in lines:
            if line.strip() and not line.startswith("🔍") and not line.startswith("I found"):
                # Very basic parsing - you'd want to improve this
                results.append(SearchResult(
                    title=line[:100],
                    snippet=line[:200],
                    link="",
                    source="google",
                    extracted_at=datetime.now().isoformat()
                ))
        
        return results[:5]  # Limit to 5
    
    async def _analyze_results(self, results: List[SearchResult], task: str) -> Dict:
        """AI analysis of results"""
        if not self.llm or not results:
            return {}
        
        try:
            # Convert results to text for AI
            results_text = "\n".join([
                f"{i+1}. {r.title} - {r.price} - {r.location or ''}"
                for i, r in enumerate(results[:10])
            ])
            
            prompt = f"""
            Analyze these search results and provide recommendations:
            
            Original Task: {task}
            
            Results Found:
            {results_text}
            
            Provide analysis in this JSON format:
            {{
                "best_option": {{
                    "index": 1,
                    "reason": "why it's the best"
                }},
                "price_range": {{"min": 0, "max": 0}},
                "recommendations": ["rec1", "rec2"],
                "summary": "brief summary"
            }}
            """
            
            response = await self.llm.chat.completions.create(
                model="gpt-3.5-turbo",  # Cheaper for analysis
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return {}
    
    def _extract_query(self, task: str) -> str:
        """Extract search query from task"""
        # Remove common phrases
        phrases_to_remove = [
            "find", "search for", "look for", "get me", 
            "on facebook", "on amazon", "on marketplace",
            "under $", "less than $", "cheap", "best"
        ]
        
        query = task.lower()
        for phrase in phrases_to_remove:
            query = query.replace(phrase, "")
        
        return query.strip()
    
    def _extract_price(self, task: str) -> Optional[float]:
        """Extract price from task"""
        import re
        matches = re.findall(r'\$(\d+)', task)
        if matches:
            return float(matches[0])
        return None
    
    async def _update_progress(self, task_id: str, progress: TaskProgress):
        """Update progress and notify WebSocket clients"""
        # Update internal state
        self.active_tasks[task_id] = progress
        
        # Notify WebSocket clients if any
        if task_id in self.websocket_clients:
            for ws in self.websocket_clients[task_id]:
                try:
                    await ws.send_json(progress.to_dict())
                except:
                    pass
    
    # ==================== WEBSOCKET API ====================
    
    async def websocket_handler(self, websocket, task_id: str):
        """Handle WebSocket connections for real-time updates"""
        if task_id not in self.websocket_clients:
            self.websocket_clients[task_id] = []
        
        self.websocket_clients[task_id].append(websocket)
        
        try:
            # Send current progress
            if task_id in self.active_tasks:
                await websocket.send_json(self.active_tasks[task_id].to_dict())
            
            # Keep connection alive
            async for _ in websocket:
                pass
                
        finally:
            self.websocket_clients[task_id].remove(websocket)
            if not self.websocket_clients[task_id]:
                del self.websocket_clients[task_id]
    
    # ==================== SIMPLE API ====================
    
    async def quick_search(self, query: str) -> List[SearchResult]:
        """Simple search without complex navigation"""
        from google_search import google_search
        
        try:
            results_text = await google_search(query)
            return self._parse_google_results(results_text)
        except:
            return []
    
    async def close(self):
        """Cleanup resources"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        
        logger.info("SuperNavigator shutdown complete")

# ==================== GLOBAL INSTANCE ====================
super_nav = SuperNavigator()

# ==================== FASTAPI INTEGRATION (Optional) ====================
"""
# If you want to add a web API, add this in a separate file:

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.post("/search")
async def start_search(task: str):
    progress = await super_nav.execute_smart_search(task)
    return {"task_id": progress.task_id, "status": progress.status}

@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()
    await super_nav.websocket_handler(websocket, task_id)
"""
