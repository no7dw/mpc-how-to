import asyncio
from mcp.client.websocket import websocket_client
import mcp
from mcp.client.stdio import stdio_client
import os
from datetime import datetime

# Create screenshots directory if it doesn't exist
screenshots_dir = os.path.join(os.getcwd(), "screenshots")
os.makedirs(screenshots_dir, exist_ok=True)

# Create server parameters for stdio connection using the Playwright MCP server configuration
server_params = mcp.StdioServerParameters(
    command="npx",  # Executable
    args=[
        "-y",
        "@smithery/cli",
        "run",
        "@executeautomation/playwright-mcp-server",
        "--config",
        "{}"
    ]
)

async def main():
    try:
        # Connect to the server using stdio client
        async with stdio_client(server_params) as (read, write):
            async with mcp.ClientSession(read, write) as session:
                # List available tools
                tools_list = await session.list_tools()
                print(f"Available tools: {', '.join([t.name for t in tools_list.tools])}")

                try:
                    # Example: Navigate to a website using playwright_navigate
                    target_url = "https://finance.yahoo.com/news/"
                    result = await session.call_tool(
                        "playwright_navigate",
                        arguments={
                            "url": target_url,
                            "browserType": "chromium",
                            "headless": False,
                            "width": 1280,
                            "height": 720,
                            "timeout": 10000,  # 30 seconds timeout
                            "waitUntil": "networkidle"  # Wait until network is idle
                        }
                    )
                    print("Navigation result:", result)
                    domain_name = target_url.split("/")[2]
                    # Generate timestamp for unique filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = os.path.join(screenshots_dir, f"{domain_name}_{timestamp}.png")

                    # Take a screenshot of the page
                    _ = await session.call_tool(
                        "playwright_screenshot",
                        arguments={
                            "name": f"{domain_name}_{timestamp}",
                            "fullPage": True,
                            "savePng": True,
                            "storeBase64": True,
                            "downloadsDir": screenshots_dir
                        }
                    )
                    print(f"Screenshot saved to: {screenshot_path}")

                finally:
                    # Always try to close the browser
                    try:
                        await session.call_tool(
                            "playwright_close",
                            arguments={"random_string": "close"}
                        )
                        print("Browser closed successfully")
                    except Exception as e:
                        print(f"Error closing browser: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
