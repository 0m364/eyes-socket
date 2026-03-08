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
            description="Send a message to the bot model with persistent history. Can specify multiple models and rounds for chaining.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_input": {
                        "type": "string",
                        "description": "The message to send to the bot."
                    },
                    "model_cmds": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Commands to run the bot model executables, API URLs, or browser: URLs. Default: ['python3 mock_bot.py']"
                    },
                    "model_cmd": {
                        "type": "string",
                        "description": "Fallback command to run the bot model executable (for backwards compatibility).",
                    },
                    "rounds": {
                        "type": "integer",
                        "description": "Number of conversational rounds if chaining multiple models.",
                        "default": 1
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

    # Handle single string fallback for model_cmds parameter if requested via old spec (or mcp default)
    if "model_cmds" in arguments:
        model_cmds = arguments["model_cmds"]
    elif "model_cmd" in arguments:
        model_cmds = [arguments["model_cmd"]]
    else:
        model_cmds = ["python3 mock_bot.py"]

    if isinstance(model_cmds, str):
        model_cmds = [model_cmds]

    rounds = arguments.get("rounds", 1)
    history_file = arguments.get("history_file", "chat_history.txt")

    try:
        socket = EyesSocket(model_cmds=model_cmds, history_file=history_file)
        ai_responses = socket.chat(user_input, rounds=rounds)

        output_text = ""
        if isinstance(ai_responses, list):
             for model_name, response in ai_responses:
                 output_text += f"{model_name}: {response}\n"
             if not output_text:
                 output_text = "Bot: [No response or error]"
        elif ai_responses:
             output_text = f"Bot: {ai_responses}"
        else:
             output_text = "Bot: [No response or error]"

        return [types.TextContent(type="text", text=output_text.strip())]

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
