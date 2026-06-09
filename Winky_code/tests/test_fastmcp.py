from fastmcp import FastMCP
from pc_controller import mouse_move

mcp = FastMCP("test")
try:
    mcp.add_tool(mouse_move)
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
