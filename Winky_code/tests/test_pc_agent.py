import os
import sys
import asyncio

# Ensure parent directory of Winky_code is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Fix encoding issues on Windows
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

async def test_pc_agent():
    print("=== Testing Imports ===")
    try:
        import pyautogui
        import mss
        import pygetwindow as gw
        from PIL import Image
        from google import genai
        print("✅ Core packages imported successfully.")
    except Exception as e:
        print(f"❌ Failed importing core packages: {e}")
        return

    print("\n=== Testing PC Controller ===")
    try:
        import pc_controller
        print("✅ pc_controller.py imported successfully.")
        
        # Test active window details
        active_window_info = await pc_controller.get_active_window()
        print(f"👉 Active window: {active_window_info}")
        
        # Test screen resolution size
        width, height = pyautogui.size()
        print(f"👉 Screen resolution: {width}x{height}")
        
        # Test mouse movement safely (move to center of screen)
        cx, cy = width // 2, height // 2
        print(f"👉 Moving mouse to center: ({cx}, {cy})...")
        await pc_controller.mouse_move(cx, cy)
        print("✅ Mouse moved.")
    except Exception as e:
        print(f"❌ Failed testing PC Controller: {e}")

    print("\n=== Testing Vision Engine ===")
    try:
        import vision_engine
        print("✅ vision_engine.py imported successfully.")
        
        # Take a screenshot using mss
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            print(f"👉 Screenshot captured: Size={img.size}")
            img.thumbnail((1280, 720))
            print(f"👉 Compressed size: {img.size}")
            
        # Try initializing GenAI client
        try:
            client = vision_engine.get_genai_client()
            print("✅ Gemini GenAI Client initialized successfully.")
        except Exception as api_err:
            print(f"⚠️ API Client could not be initialized (probably missing key): {api_err}")
            
    except Exception as e:
        print(f"❌ Failed testing Vision Engine: {e}")

    print("\n=== Testing App Registry ===")
    try:
        import app_registry
        print("✅ app_registry.py imported successfully.")
        print(f"👉 Registered apps (first 10): {list(app_registry.APP_COMMANDS.keys())[:10]}")
        
        # Try launching calculator
        print("👉 Launching calculator...")
        result = await app_registry.launch_app("calculator")
        print(f"👉 Result: {result}")
    except Exception as e:
        print(f"❌ Failed testing App Registry: {e}")

    print("\n=== Testing New Proactive Tools ===")
    try:
        import pc_controller
        print("👉 Checking for new tools on pc_controller...")
        tools = ["ensure_window_focus", "smart_type", "launch_app_via_search", "open_spotify_and_play", "automate_notepad"]
        for tool in tools:
            if hasattr(pc_controller, tool):
                print(f"✅ Tool '{tool}' is successfully implemented.")
            else:
                print(f"❌ Tool '{tool}' is MISSING!")
                
        # Try focusing the Chrome window
        print("👉 Attempting to focus Chrome window...")
        focus_res = await pc_controller.ensure_window_focus("chrome")
        print(f"👉 Focus result: {focus_res}")
    except Exception as e:
        print(f"❌ Failed testing new proactive tools: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(test_pc_agent())
