# Bot Persistence (eyes-socket)

This repository contains tools to add persistent memory (chat history) to local bot models, AI APIs, and conversational endpoints. It provides implementations in Python (`eyes-socket`), C++, and Java, along with a simple HTML frontend mock.

`eyes-socket` aims to be the go-to fast, secure, and modular persistency module for all AI frameworks, capable of connecting to any LLM or API.

## Overview

The core idea is to maintain a chat history file and feed the recent history as context to the bot model on each interaction. This allows for continuous, stateful conversations across any framework.

## `eyes-socket` (Python Implementation)

The most robust and recommended implementation, now available as a Python package.

### Features
*   **Modular Architecture:** Support for Local models, API endpoints, OpenAI, Anthropic, and Ollama out-of-the-box.
*   **Zero Dependencies:** Uses the Python standard library for network requests ensuring speed and eliminating dependency bloat.
*   **Secure:** API keys are read securely from environment variables, never hardcoded.

### Installation

You can install `eyes-socket` from source:

```bash
pip install .
```

### Usage via CLI

Once installed, you can use the `eyes-socket` command globally:

**Local Model:**
```bash
eyes-socket --model "./path/to/your/model" --history "chat_history.txt"
```

**OpenAI (Requires `OPENAI_API_KEY` environment variable):**
```bash
export OPENAI_API_KEY="your-key-here"
eyes-socket --model "openai:gpt-4o" --history "chat_history.txt"
```

**Anthropic (Requires `ANTHROPIC_API_KEY` environment variable):**
```bash
export ANTHROPIC_API_KEY="your-key-here"
eyes-socket --model "anthropic:claude-3-opus-20240229" --history "chat_history.txt"
```

**Ollama (Optionally respects `OLLAMA_HOST`):**
```bash
eyes-socket --model "ollama:llama3" --history "chat_history.txt"
```

**Generic API:**
```bash
eyes-socket --model "https://my-custom-api.com/chat" --history "chat_history.txt"
```

**Options:**
- `--model`: Command to run the bot model executable or the API URI (default: `./your-bot-model/chat`).
- `--history`: Path to the chat history file (default: `chat_history.txt`).

### Usage as a Python API

You can also use `eyes-socket` in your own Python scripts to easily add state to any LLM wrapper:

```python
import os
from eyes_socket import EyesSocket

os.environ["OPENAI_API_KEY"] = "sk-..."

socket = EyesSocket(model_cmds="openai:gpt-3.5-turbo", history_file="my_history.txt")
response = socket.chat("Hello!")
print(response)
```

## Other Implementations

### C++ (`bot_persistence.cpp`)

A compiled implementation for performance or integration into C++ projects.

**Compilation:**
```bash
g++ -o bot_persistence bot_persistence.cpp
```

**Usage:**
```bash
./bot_persistence "./path/to/your/model" "chat_history.txt"
```

### Java (`ChatBot.java`)

A Java implementation.

**Compilation:**
```bash
javac ChatBot.java
```

**Usage:**
```bash
java ChatBot "./path/to/your/model" "chat_history.txt"
```

### HTML (`bot_memory.html`)

A simple web interface. Note that this is a frontend mock and requires a backend server (not included) to actually communicate with a bot model.

## Testing with Mock Bot

A `mock_bot.py` script is included for testing purposes. It simply echoes back the input it receives.

**To test the Python implementation:**
```bash
eyes-socket --model "python3 mock_bot.py"
```

### Usage as an MCP Server

`eyes-socket` can now be used as an MCP (Model Context Protocol) server to integrate with agentic frameworks.

1. Install with MCP dependencies:
   ```bash
   pip install ".[mcp]"
   ```

2. Run the MCP server:
   ```bash
   eyes-socket-mcp
   ```

   The server provides the `chat_with_bot` tool which takes:
   - `user_input` (required): The message to send to the bot.
   - `model_cmds` (optional): Array of commands/URIs to run the bot models (e.g. `["openai:gpt-4", "ollama:llama3"]`).
   - `rounds` (optional): Number of conversational rounds for chained models.
   - `history_file` (optional): Path to the chat history file (default: `chat_history.txt`).

## License

See `MITLicense.txt`.
