import sys
import logging
from fastmcp import FastMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




# Import all tool functions
from pc_controller import (
    mouse_move, mouse_click, mouse_scroll, keyboard_type, keyboard_press_keys, get_active_window,
    ensure_window_focus, smart_type, launch_app_via_search, open_spotify_and_play, automate_notepad
)
from jarvis_get_whether import get_weather
from vision_engine import locate_element_on_screen
from app_registry import launch_app
from comprehensive_mcp_tools import COMPREHENSIVE_TOOLS
from dom_vision_engine import extract_window_dom, take_screenshot_and_analyze

logger.info("Initializing Winky MCP Server...")

def unwrap_function(func):
    """
    LiveKit's @function_tool decorator wraps the function in a FunctionTool class instance.
    We need to extract the underlying original coroutine function so FastMCP knows it is
    an async function and awaits it correctly.
    Newer LiveKit versions use .fnc, older use ._func.
    """
    if hasattr(func, 'fnc'):
        return func.fnc
    return getattr(func, '_func', func)

# Create the MCP server
mcp = FastMCP("Winky_MCP_Server")

# Add standard tools. FastMCP seamlessly inspects the function signatures, 
# even if they are decorated with LiveKit's @function_tool.
mcp.add_tool(unwrap_function(mouse_move))
mcp.add_tool(unwrap_function(mouse_click))
mcp.add_tool(unwrap_function(mouse_scroll))
mcp.add_tool(unwrap_function(keyboard_type))
mcp.add_tool(unwrap_function(keyboard_press_keys))
mcp.add_tool(unwrap_function(get_active_window))
mcp.add_tool(unwrap_function(ensure_window_focus))
mcp.add_tool(unwrap_function(smart_type))
mcp.add_tool(unwrap_function(launch_app_via_search))
mcp.add_tool(unwrap_function(open_spotify_and_play))
mcp.add_tool(unwrap_function(automate_notepad))
mcp.add_tool(unwrap_function(launch_app))
mcp.add_tool(unwrap_function(get_weather))
mcp.add_tool(unwrap_function(locate_element_on_screen))
mcp.add_tool(unwrap_function(extract_window_dom))
mcp.add_tool(unwrap_function(take_screenshot_and_analyze))

logger.info("Registered standard PC Controller and Vision tools.")

# Add comprehensive tools from the dictionary
for name, func in COMPREHENSIVE_TOOLS.items():
    # fastmcp uses the function's name by default, we can rename it.
    mcp.add_tool(unwrap_function(func), name=name)

logger.info(f"Registered {len(COMPREHENSIVE_TOOLS)} comprehensive tools.")

if __name__ == "__main__":
    logger.info("Starting Winky MCP Server via stdio...")
    # FastMCP run() method uses stdio by default or can be explicitly configured.
    # We use stdio for inter-process communication.
    mcp.run(transport='stdio')
