import asyncio
import os
import sys

# To support mcp server tools
try:
    from mcp.server.models import InitializationOptions
    import mcp.types as types
    from mcp.server import NotificationOptions, Server
    from mcp.server.stdio import stdio_server
except ImportError:
    print("The mcp package is required to run the MCP server.")
    print("Please install it using: pip install mcp")
    sys.exit(1)

from eyes_socket.core import EyesSocket

server = Server("eyes-socket")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="chat_with_bot",
            description="Send a message to the bot model with persistent history.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_input": {
                        "type": "string",
                        "description": "The message to send to the bot."
                    },
                    "model_cmd": {
                        "type": "string",
                        "description": "Command to run the bot model executable (default: 'python3 mock_bot.py')",
                    },
                    "history_file": {
                        "type": "string",
                        "description": "Path to the chat history file (default: 'chat_history.txt')"
                    }
                },
                "required": ["user_input"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    if name != "chat_with_bot":
        raise ValueError(f"Unknown tool: {name}")

    if not arguments or "user_input" not in arguments:
        raise ValueError("Missing required argument 'user_input'")

    user_input = arguments["user_input"]
    model_cmd = arguments.get("model_cmd", "python3 mock_bot.py")
    history_file = arguments.get("history_file", "chat_history.txt")

    try:
        socket = EyesSocket(model_cmd=model_cmd, history_file=history_file)
        ai_response = socket.chat(user_input)

        if ai_response:
            return [types.TextContent(type="text", text=ai_response)]
        else:
            return [types.TextContent(type="text", text="Bot: [No response or error]")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def run_server():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="eyes-socket",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

def main():
    asyncio.run(run_server())

if __name__ == "__main__":
    main()
