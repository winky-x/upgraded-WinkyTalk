# Goal: Add DOM and Vision Navigation Capabilities

The current system relies on basic mouse/keyboard control and Gemini Vision for finding element coordinates on the screen. However, this is limited because the AI doesn't have structured knowledge of the active window's elements (like a DOM tree) to interact reliably with applications like Spotify or Chrome. 

This plan introduces a reliable way for the AI to "see" and "read" the exact structured elements on the screen, just like reading a web page's DOM, but for any desktop application.

## User Review Required

> [!IMPORTANT]
> **Library Choice:** I propose using the `uiautomation` Python library. It hooks into Microsoft's UI Automation framework to extract the "Accessibility Tree" (which acts exactly like a DOM) for ANY open application, including Chrome, Spotify, and Notepad. This means the AI won't need to launch a new automated browser—it can just read what's currently on your screen! Do you approve of installing this library?

> [!WARNING]
> Web browsers like Chrome must have "Accessibility" enabled for the DOM to be fully readable by Windows. Usually, this happens automatically when a UI Automation script queries it, but in some edge cases, certain web elements might be opaque unless you run Chrome with `--force-renderer-accessibility`. I will add fallback mechanisms to use Gemini Vision if the DOM extraction fails.

## Proposed Changes

---

### Virtual Environment
#### [MODIFY] Requirements
- Run `pip install uiautomation` to add the Microsoft UI Automation python wrapper to our virtual environment.

---

### Winky Codebase

#### [NEW] [dom_vision_engine.py](file:///c:/Users/login/Desktop/upgraded-WinkyTalk/Winky_code/dom_vision_engine.py)
Create a new engine that provides tools to extract the screen's DOM:
- `extract_window_dom()`: A tool that finds the currently active window, walks its UI Automation tree, and returns a structured JSON list of all interactive elements (Buttons, Text controls, Hyperlinks, etc.) along with their exact screen coordinates (x, y) so the AI can use `mouse_click` on them.

#### [MODIFY] [winky_mcp_server.py](file:///c:/Users/login/Desktop/upgraded-WinkyTalk/Winky_code/winky_mcp_server.py)
- Register the new `extract_window_dom` tool with the FastMCP server so Winky can access it dynamically.

#### [MODIFY] [pc_controller.py](file:///c:/Users/login/Desktop/upgraded-WinkyTalk/Winky_code/pc_controller.py)
- Optional: Enhance `open_spotify_and_play` to utilize the DOM extraction to verify if Spotify is playing or if the search bar was successfully found, instead of blindly typing.

## Verification Plan

### Automated Tests
- Run `python dom_vision_engine.py` directly to print the extracted DOM tree of the active terminal window to verify the library works correctly on your system.

### Manual Verification
- Start the MCP server and voice agent.
- Ask Winky to "Open Spotify and read out the buttons on the screen" or "Play a specific song on Spotify using the UI."
- Check if Winky uses the `extract_window_dom` tool, correctly identifies the coordinates, and clicks the right elements without relying solely on guessing coordinates.
