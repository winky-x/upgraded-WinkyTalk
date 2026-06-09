from winky_mcp_server import mcp
import asyncio
print("Imported mcp successfully.")
async def run_tool():
    try:
        print("Calling automate_notepad locally...")
        res = await mcp.call_tool("automate_notepad", arguments={"text": "Local test from test_list.py"})
        print(f"Result: {res}")
    except Exception as e:
        print(f"Failed calling tool: {e}")

asyncio.run(run_tool())
