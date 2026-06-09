import uiautomation as auto
import json
import logging
import asyncio
from livekit.agents import function_tool

logger = logging.getLogger(__name__)


def _walk_tree(control, depth=0, max_depth=8, results=None):
    """Recursively walk the UI Automation tree using GetChildren()."""
    if results is None:
        results = []
    if depth > max_depth:
        return results
    try:
        children = control.GetChildren()
    except Exception:
        return results
    
    INTERACTIVE_TYPES = {
        "ButtonControl", "ListItemControl", "TabItemControl",
        "HyperlinkControl", "EditControl", "CheckBoxControl",
        "TextControl", "MenuItemControl", "TreeItemControl",
        "DocumentControl", "ComboBoxControl", "RadioButtonControl",
        "SliderControl", "ToolBarControl", "MenuBarControl",
    }
    
    for child in children:
        try:
            ct = child.ControlTypeName
            if ct in INTERACTIVE_TYPES:
                rect = child.BoundingRectangle
                if rect:
                    w = rect.width()
                    h = rect.height()
                    if w > 0 and h > 0:
                        name = child.Name or ""
                        # Skip nameless text/button with tiny size (icon glyphs)
                        if name or ct in ("EditControl", "DocumentControl"):
                            results.append({
                                "type": ct.replace("Control", ""),
                                "name": name[:120],
                                "center_x": int(rect.xcenter()),
                                "center_y": int(rect.ycenter()),
                                "width": int(w),
                                "height": int(h),
                            })
        except Exception:
            pass
        # Always recurse into children
        _walk_tree(child, depth + 1, max_depth, results)
    return results


@function_tool
async def extract_window_dom(window_title: str = "") -> str:
    """
    Extracts the UI Automation tree (like a DOM) of a window.
    Returns a JSON list of interactive elements (Buttons, Text fields, Menu items, etc.)
    along with their exact screen pixel coordinates (center_x, center_y).

    Use this BEFORE clicking on anything inside an application. It tells you exactly
    what buttons, text fields, and links exist and where they are on the screen.

    Args:
        window_title: Optional partial window title to target a specific window.
                      If empty, uses the currently active/foreground window.

    Example usage flow:
    1. Call extract_window_dom("Spotify") to see all Spotify UI elements.
    2. Find the element you need (e.g. a Search button at center_x=500, center_y=80).
    3. Call mouse_click(500, 80) to click it.
    """
    try:
        def _extract():
            import pythoncom
            pythoncom.CoInitialize()
            try:
                if window_title:
                    target = auto.WindowControl(
                        searchDepth=1, SubName=window_title
                    )
                    if not target.Exists(3, 1):
                        return {
                            "error": f"Window with title containing '{window_title}' not found.",
                            "suggestion": "Try calling get_active_window() first, or use ensure_window_focus() to bring it to front."
                        }
                else:
                    target = auto.GetForegroundControl()
                    if not target:
                        return {"error": "No active window found."}

                elements = _walk_tree(target, max_depth=6)

                # Cap at 150 elements to avoid overwhelming the LLM
                truncated = len(elements) > 150
                if truncated:
                    elements = elements[:150]

                result = {
                    "window_title": target.Name,
                    "elements_found": len(elements),
                    "truncated": truncated,
                    "elements": elements,
                }
                
                # If very few elements found, suggest using vision fallback
                if len(elements) < 5:
                    result["suggestion"] = (
                        "Very few UI elements found via DOM. This is common for Chrome, Spotify, "
                        "and Electron apps whose content is rendered in a web view. "
                        "Use take_screenshot_and_analyze() to visually read the screen content instead."
                    )
                
                return result
            finally:
                pythoncom.CoUninitialize()

        result = await asyncio.to_thread(_extract)
        return json.dumps(result)
    except Exception as e:
        logger.exception(f"Error extracting window DOM: {e}")
        return json.dumps({"error": f"[DEBUG MODE ERROR: DOM Extraction Failed] {str(e)}"})


@function_tool
async def take_screenshot_and_analyze(question: str) -> str:
    """
    Takes a screenshot of the current screen and uses Gemini Vision to answer a question about it.
    Use this when you need to visually understand what is on the screen but the DOM extraction
    does not provide enough information (e.g. for images, videos, or complex web page layouts
    like Chrome, Spotify, or Electron apps).

    Args:
        question: What you want to know about the screen (e.g. "Is the song playing?",
                  "What page is open in Chrome?", "What error message is shown?",
                  "What interactive elements are visible and where are they?")
    """
    import io
    import os
    import mss
    import pyautogui
    from PIL import Image

    try:
        from google import genai
        from google.genai import types
        from config_manager import ConfigManager

        config = ConfigManager()
        google_api_key = config.get_api_key("google") or os.environ.get("GOOGLE_API_KEY")
        if not google_api_key:
            return json.dumps({"error": "Google API key not configured."})

        client = genai.Client(api_key=google_api_key)

        # Get screen dimensions for context
        screen_width, screen_height = pyautogui.size()

        # Capture screen
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

        # Compress
        img.thumbnail((1280, 720))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=70)
        buffer.seek(0)
        compressed_img = Image.open(buffer)

        prompt = f"""You are analyzing a screenshot of a user's PC screen.
The screen resolution is {screen_width}x{screen_height} pixels.

Answer this question: {question}

IMPORTANT INSTRUCTIONS:
- Be specific and detailed about what you see.
- If you see interactive elements (buttons, search bars, links, text fields), describe them AND estimate their approximate pixel position as (x, y) based on the {screen_width}x{screen_height} resolution.
- If there are error messages, quote them exactly.
- If asked about positions, give approximate pixel coordinates like "The search bar is at approximately (500, 85)".
- Focus on ACTIONABLE information that would help someone interact with the screen programmatically.
- Return your answer as plain text."""

        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=[compressed_img, prompt]
        )

        return response.text.strip()
    except Exception as e:
        logger.exception(f"Error in screenshot analysis: {e}")
        return json.dumps({"error": f"[DEBUG MODE ERROR: Screenshot API Failed] {str(e)}", "suggestion": "Try using extract_window_dom() instead, or try locate_element_on_screen() for a specific element. You MUST tell the user about this exact error!"})

