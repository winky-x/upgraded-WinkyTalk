import os
import sys
import asyncio
import json
import logging
import time

# Ensure parent directory of Winky_code is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your modules
import pc_controller
import vision_engine
import app_registry
from config_manager import ConfigManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def stress_test():
    print("🚀 STARTING GLOBAL STRESS TEST FOR WINKY-OS AGENT")
    print("--------------------------------------------------")
    
    # 1. App Launch Test
    print("\n[1/4] Testing App Launch (Calculator)...")
    launch_res = await app_registry.launch_app("calculator")
    print(f"Result: {launch_res}")
    if "Error" in launch_res:
        print("❌ App launch failed. Aborting stress test.")
        return
    
    print("Waiting 3 seconds for app to render...")
    await asyncio.sleep(3)
    
    # 2. Vision Grounding Test
    print("\n[2/4] Testing Vision Grounding (Locating '7' button on Calculator)...")
    start_time = time.time()
    vision_res_json = await vision_engine.locate_element_on_screen("calculator button 7")
    vision_res = json.loads(vision_res_json)
    latency = time.time() - start_time
    
    print(f"Latency: {latency:.2f}s")
    if vision_res.get("success"):
        px, py = vision_res["pixel_coordinates"]
        conf = vision_res["confidence"]
        print(f"✅ Found '7' button at: ({px}, {py}) with confidence {conf}")
        
        # 3. Hardware Control Test
        print(f"\n[3/4] Testing Hardware Control (Clicking '7')...")
        print(f"👉 Moving mouse to ({px}, {py})...")
        await pc_controller.mouse_move(px, py)
        await asyncio.sleep(0.5)
        print("👉 Clicking...")
        await pc_controller.mouse_click(px, py)
        print("✅ Click executed.")
    else:
        print(f"❌ Vision Grounding failed: {vision_res.get('message', 'Unknown error')}")

    # 4. Search Grounding / Latency Test
    print("\n[4/4] Testing Search Grounding Latency...")
    print("👉 Search Grounding is now handled natively by Gemini. Testing availability...")
    try:
        from livekit.plugins import google
        if hasattr(google, 'google_search'):
            print("✅ Native Google Search tool is available in plugins.")
        else:
            print("⚠️ Native Google Search tool NOT found in current livekit plugins version.")
    except Exception as e:
        print(f"❌ Search Grounding check failed: {e}")

    print("\n--------------------------------------------------")
    print("🏁 STRESS TEST COMPLETE")
    
    # Cleanup: Try to close Calculator
    print("\nCleaning up: Attempting to close Calculator...")
    close_res = await vision_engine.locate_element_on_screen("calculator close button")
    close_data = json.loads(close_res)
    if close_data.get("success"):
        cx, cy = close_data["pixel_coordinates"]
        await pc_controller.mouse_click(cx, cy)
        print("✅ Calculator closed.")
    else:
        print("⚠️ Could not locate close button for cleanup.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Ensure GOOGLE_API_KEY is set for the script
    config = ConfigManager()
    os.environ["GOOGLE_API_KEY"] = config.get_api_key("google")
    
    asyncio.run(stress_test())
