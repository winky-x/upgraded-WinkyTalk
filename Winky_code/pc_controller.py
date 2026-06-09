import logging
import asyncio
import pyautogui
import pygetwindow as gw
from livekit.agents import function_tool

logger = logging.getLogger(__name__)

# Set failsafe and pause
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

@function_tool
async def mouse_move(x: int, y: int) -> str:
    """
    Moves the mouse cursor to specific screen coordinates.
    The coordinate (x, y) should be within the user's screen resolution (e.g. 1920x1080).
    """
    try:
        await asyncio.to_thread(pyautogui.moveTo, x, y, duration=0.5)
        return f"Successfully moved mouse to x={x}, y={y}"
    except Exception as e:
        logger.error(f"Error in mouse_move: {e}")
        return f"Error moving mouse: {e}"

@function_tool
async def mouse_click(x: int, y: int, clicks: int = 1) -> str:
    """
    Moves the mouse to specific coordinates and performs a left-click.
    """
    try:
        await asyncio.to_thread(pyautogui.moveTo, x, y, duration=0.5)
        await asyncio.to_thread(pyautogui.click, clicks=clicks)
        return f"Successfully clicked {clicks} time(s) at x={x}, y={y}"
    except Exception as e:
        logger.error(f"Error in mouse_click: {e}")
        return f"Error performing mouse click: {e}"

@function_tool
async def mouse_scroll(direction: str, clicks: int = 3) -> str:
    """
    Scrolls the mouse wheel. direction can be 'up' or 'down'.
    """
    try:
        amount = clicks * 100 if direction.lower() == 'up' else -clicks * 100
        await asyncio.to_thread(pyautogui.scroll, amount)
        return f"Successfully scrolled {direction} by {clicks} clicks"
    except Exception as e:
        logger.error(f"Error in mouse_scroll: {e}")
        return f"Error performing scroll: {e}"

@function_tool
async def keyboard_type(text: str) -> str:
    """
    Types the specified text on the keyboard at the current cursor position.
    """
    try:
        await asyncio.to_thread(pyautogui.write, text, interval=0.05)
        return f"Successfully typed: '{text}'"
    except Exception as e:
        logger.error(f"Error in keyboard_type: {e}")
        return f"Error typing text: {e}"

@function_tool
async def keyboard_press_keys(keys: str) -> str:
    """
    Presses a hotkey or combination of keys separated by plus (+) e.g. 'ctrl+c' or 'ctrl+t' or 'enter'.
    """
    try:
        parts = [k.strip().lower() for k in keys.split('+')]
        await asyncio.to_thread(pyautogui.hotkey, *parts)
        return f"Successfully pressed keys: {keys}"
    except Exception as e:
        logger.error(f"Error in keyboard_press_keys: {e}")
        return f"Error pressing keys: {e}"

@function_tool
async def get_active_window() -> str:
    """
    Gets the details (title, dimensions, position) of the currently active/focused window.
    """
    try:
        win = await asyncio.to_thread(gw.getActiveWindow)
        if win:
            return f"Active Window: Title='{win.title}', Left={win.left}, Top={win.top}, Width={win.width}, Height={win.height}"
        else:
            return "No active window found"
    except Exception as e:
        logger.error(f"Error getting active window: {e}")
        return f"Error getting active window: {e}"

@function_tool
async def ensure_window_focus(app_name: str) -> str:
    """
    Finds a window matching the app name by title or process name, restores it if minimized, and focuses it.
    Use this before sending keys/hotkeys to ensure inputs go to the correct window.
    """
    try:
        import ctypes
        import psutil
        
        def get_proc_name(hwnd):
            try:
                pid = ctypes.c_ulong()
                ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                return psutil.Process(pid.value).name().lower()
            except Exception:
                return ""
                
        windows = await asyncio.to_thread(gw.getWindowsWithTitle, "")
        target_win = None
        app_name_lower = app_name.lower().strip()
        
        # Mapping common names to target executable process names
        process_mapping = {
            "spotify": "spotify.exe",
            "chrome": "chrome.exe",
            "google chrome": "chrome.exe",
            "notepad": "notepad.exe",
            "code": "code.exe",
            "vscode": "code.exe",
            "calculator": "calculatorapp.exe",
            "calc": "calculatorapp.exe"
        }
        target_proc = process_mapping.get(app_name_lower, app_name_lower + ".exe")
        
        for win in windows:
            # Check window title match
            title_match = app_name_lower in win.title.lower()
            
            # Check process name match
            proc_name = await asyncio.to_thread(get_proc_name, win._hWnd)
            proc_match = target_proc in proc_name or app_name_lower in proc_name
            
            if title_match or proc_match:
                target_win = win
                break
                
        if target_win:
            if target_win.isMinimized:
                await asyncio.to_thread(target_win.restore)
            await asyncio.to_thread(target_win.activate)
            await asyncio.sleep(0.5)
            win_proc = await asyncio.to_thread(get_proc_name, target_win._hWnd)
            return f"Successfully focused window: '{target_win.title}' (Process: {win_proc})"
        else:
            return f"Could not find any window matching '{app_name}' to focus."
    except Exception as e:
        logger.error(f"Error in ensure_window_focus: {e}")
        return f"Error focusing window: {e}"

@function_tool
async def smart_type(text: str, press_enter: bool = True) -> str:
    """
    Types text at the current cursor position and optionally presses enter.
    Use this for typing search queries, URL addresses, file names, or text content.
    """
    try:
        await asyncio.to_thread(pyautogui.write, text, interval=0.03)
        if press_enter:
            await asyncio.to_thread(pyautogui.press, 'enter')
            return f"Successfully typed '{text}' and pressed Enter"
        return f"Successfully typed '{text}'"
    except Exception as e:
        logger.error(f"Error in smart_type: {e}")
        return f"Error typing: {e}"

@function_tool
async def launch_app_via_search(app_name: str) -> str:
    """
    Launches any application by searching for it in the Windows Start menu (Win+S).
    Use this as a fallback if launch_app fails or the app is not in the registry.
    """
    try:
        # Press Win+S to open Windows Search
        await asyncio.to_thread(pyautogui.hotkey, 'win', 's')
        await asyncio.sleep(1.0)
        
        # Type the app name
        await asyncio.to_thread(pyautogui.write, app_name, interval=0.03)
        await asyncio.sleep(1.0)
        
        # Press Enter to run the selected app
        await asyncio.to_thread(pyautogui.press, 'enter')
        await asyncio.sleep(1.5)
        
        return f"Sent search query for '{app_name}' via Windows Search and pressed Enter."
    except Exception as e:
        logger.error(f"Error in launch_app_via_search: {e}")
        return f"Error launching app via search: {e}"

@function_tool
async def open_spotify_and_play(query: str) -> str:
    """
    Launches Spotify, searches for the specified song/artist/playlist, and starts playback.
    First checks if Spotify Desktop is already running. If not found, falls back to Spotify Web Player in Chrome.
    This tool handles the FULL flow: launch → search → play.
    """
    try:
        import shutil
        from app_registry import launch_app
        
        # Step 1: Check if Spotify Desktop is already running (window exists)
        focus_res = await ensure_window_focus("spotify")
        is_desktop = "Successfully focused" in focus_res
        
        if not is_desktop:
            # Step 2: Check if Spotify executable is even installed on this system
            spotify_installed = shutil.which("spotify") is not None or shutil.which("spotify.exe") is not None
            
            if spotify_installed:
                # Try launching the desktop app via launch_app_via_search (safer than os.startfile)
                await launch_app_via_search("Spotify")
                await asyncio.sleep(3.0)
                focus_res = await ensure_window_focus("spotify")
                is_desktop = "Successfully focused" in focus_res
                
        if is_desktop:
            # Desktop workflow (search with Ctrl+L which opens Spotify search)
            await asyncio.to_thread(pyautogui.hotkey, 'ctrl', 'l')
            await asyncio.sleep(0.5)
            
            await asyncio.to_thread(pyautogui.write, query, interval=0.03)
            await asyncio.sleep(0.5)
            await asyncio.to_thread(pyautogui.press, 'enter')
            await asyncio.sleep(2.0)
            
            # Press Enter again to play the first result
            await asyncio.to_thread(pyautogui.press, 'enter')
            await asyncio.sleep(0.5)
            
            return f"Spotify Desktop: searched for '{query}' and pressed play on first result."
        else:
            # Web Player workflow
            logger.info("Spotify Desktop not found/installed. Falling back to Spotify Web in Chrome...")
            search_url = "https://open.spotify.com/search/" + query.replace(" ", "%20")
            await launch_app("chrome", search_url)
            await asyncio.sleep(5.0)  # Wait for Spotify web app to load
            await ensure_window_focus("chrome")
            
            # Wait a bit more for content to render, then try to click the first song result
            await asyncio.sleep(2.0)
            
            # Use Tab to navigate to first result and Enter to play
            # Tab through the Spotify web UI to reach first playable result
            for _ in range(5):
                await asyncio.to_thread(pyautogui.press, 'tab')
                await asyncio.sleep(0.2)
            await asyncio.to_thread(pyautogui.press, 'enter')
            await asyncio.sleep(1.0)
            
            return f"Spotify Web Player opened in Chrome with search for '{query}'. Attempted to play the first result. Use take_screenshot_and_analyze to verify if the song is playing."
    except Exception as e:
        logger.error(f"Error in open_spotify_and_play: {e}")
        return f"Error automating Spotify: {e}. Try manually: launch_app('chrome', 'https://open.spotify.com/search/{query}') then use extract_window_dom or take_screenshot_and_analyze to interact."

@function_tool
async def automate_notepad(text: str, filename: str = None) -> str:
    """
    Creates a Notepad document and types the given text.
    Only specify a filename to save the document to the Desktop if the user explicitly requested to save it or provided a filename. By default, leave filename as None.
    """
    try:
        import pyperclip
        from app_registry import launch_app
        launch_res = await launch_app("notepad")
        if "Failed" in launch_res:
            await launch_app_via_search("notepad")
            
        await asyncio.sleep(1.5)
        await ensure_window_focus("notepad")
        
        # Use clipboard paste instead of pyautogui.write() — handles newlines, Unicode, special chars
        await asyncio.to_thread(pyperclip.copy, text)
        await asyncio.sleep(0.2)
        await asyncio.to_thread(pyautogui.hotkey, 'ctrl', 'v')
        await asyncio.sleep(0.5)
        
        if filename:
            # Press Ctrl+S
            await asyncio.to_thread(pyautogui.hotkey, 'ctrl', 's')
            await asyncio.sleep(1.0)
            
            # Construct path on Desktop
            import os
            desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            save_path = os.path.join(desktop_dir, filename)
            
            # Type path and hit enter
            await asyncio.to_thread(pyperclip.copy, save_path)
            await asyncio.sleep(0.2)
            await asyncio.to_thread(pyautogui.hotkey, 'ctrl', 'v')
            await asyncio.sleep(0.5)
            await asyncio.to_thread(pyautogui.press, 'enter')
            await asyncio.sleep(0.5)
            
            return f"Notepad automated: typed text and saved as '{filename}' on Desktop."
            
        return "Notepad automated: typed text successfully."
    except Exception as e:
        logger.error(f"Error in automate_notepad: {e}")
        return f"Error automating Notepad: {e}"


