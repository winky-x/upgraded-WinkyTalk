import os
import io
import json
import logging
import asyncio
import mss
import pyautogui
from PIL import Image
from google import genai
from google.genai import types
from livekit.agents import function_tool
from config_manager import ConfigManager

logger = logging.getLogger(__name__)

# Initialize ConfigManager
config = ConfigManager()

def get_genai_client():
    google_api_key = config.get_api_key("google") or os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("Google API key is missing from config and environment.")
    return genai.Client(api_key=google_api_key)

@function_tool
async def locate_element_on_screen(element_description: str) -> str:
    """
    Takes a screenshot of the user's screen and uses Gemini Vision to locate the described element.
    Returns the X and Y coordinates (normalized 0 to 1000, and converted to screen pixels).
    Use this BEFORE trying to click or move to any button, app icon, text field, or menu item.
    
    Example prompts:
    - "Chrome window को locate करो"
    - "Search bar कहाँ पर है?"
    - "Find the close button"
    """
    logger.info(f"Visual grounding: Locating '{element_description}' on screen...")
    
    try:
        # Get screen dimensions
        screen_width, screen_height = pyautogui.size()
        
        # Take screenshot using mss
        with mss.mss() as sct:
            # Capture the primary monitor
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            
            # Convert mss screenshot to PIL Image
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            
        # Compress / downscale image to 720p / low quality JPEG
        img.thumbnail((1280, 720))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=70)
        buffer.seek(0)
        compressed_img = Image.open(buffer)
        
        # Call Gemini GenAI SDK
        client = get_genai_client()
        
        prompt = f"""
You are the visual coordinate locator for a Local PC Agent.
Your task is to analyze the screenshot and locate the following element: "{element_description}"

Return a JSON object with:
- "x": Center X coordinate of the element on a scale of 0 to 1000 (0 = left edge, 1000 = right edge).
- "y": Center Y coordinate of the element on a scale of 0 to 1000 (0 = top edge, 1000 = bottom edge).
- "confidence": Float between 0.0 and 1.0 representing your confidence.
- "message": A brief status description.

Example output:
{{
  "x": 450,
  "y": 880,
  "confidence": 0.92,
  "message": "Found Chrome icon in the taskbar"
}}

IMPORTANT: Return ONLY raw JSON. Do not wrap in markdown or any other format.
"""
        # Run API call in asyncio to_thread to keep LiveKit responsive
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=[compressed_img, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        result_text = response.text.strip()
        logger.info(f"Gemini grounding response: {result_text}")
        
        # Parse JSON
        data = json.loads(result_text)
        x_norm = data.get("x")
        y_norm = data.get("y")
        confidence = data.get("confidence", 0.0)
        msg = data.get("message", "")
        
        if x_norm is None or y_norm is None:
            return f"Error: Could not locate '{element_description}' on the screen. Gemini did not return valid coordinates."
            
        # Convert to screen pixels
        pixel_x = int((x_norm / 1000) * screen_width)
        pixel_y = int((y_norm / 1000) * screen_height)
        
        result_dict = {
            "success": True,
            "element": element_description,
            "normalized_coordinates": [x_norm, y_norm],
            "pixel_coordinates": [pixel_x, pixel_y],
            "screen_resolution": [screen_width, screen_height],
            "confidence": confidence,
            "message": msg
        }
        
        return json.dumps(result_dict)
        
    except Exception as e:
        logger.exception(f"Exception in locate_element_on_screen: {e}")
        return json.dumps({
            "success": False,
            "error": f"[DEBUG MODE ERROR: Rate Limit or API Failure] {str(e)}",
            "message": f"Failed to locate element due to error. You MUST report this to the user: {str(e)}"
        })
