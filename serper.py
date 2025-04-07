import asyncio
import smithery
import mcp
import json
from mcp.client.websocket import websocket_client
import os
# Create Smithery URL with server endpoint
url = smithery.create_smithery_url("wss://server.smithery.ai/@marcopesani/mcp-server-serper/ws", {
  "serperApiKey": os.getenv("SERPER_API_KEY")
}) + "&api_key=" + os.getenv("SMITHERY_API_KEY")


async def main():
    # Connect to the server using websocket client
    async with websocket_client(url) as streams:
        async with mcp.ClientSession(*streams) as session:
            # List available tools
            tools_result = await session.list_tools()
            print(f"Available tools: {', '.join([t.name for t in tools_result.tools])}")
            
            # Example: Call a tool
            result = await session.call_tool("google_search", {"q": "ai", "gl": "us", "hl": "en"})
            print(json.dumps(json.loads(result.content[0].text), indent=2))
if __name__ == "__main__":
    asyncio.run(main())
