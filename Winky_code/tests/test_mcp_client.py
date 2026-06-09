import sys
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_client():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["winky_mcp_server.py"],
        env=None
    )
    print("Starting client...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Session initialized.")
            
            # List tools
            tools = await session.list_tools()
            print(f"Discovered {len(tools.tools)} tools.")
            
            # Call automate_notepad
            print("Calling automate_notepad...")
            res = await session.call_tool("automate_notepad", arguments={"text": "Hello Yuvraj, MCP is fully working!"})
            print(f"Result isError: {res.isError}")
            print(f"Result Content: {res.content[0].text}")

if __name__ == "__main__":
    asyncio.run(test_client())
