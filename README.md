# Bot Persistence (eyes-socket)

This repository contains tools to add persistent memory (chat history) to local bot models. It provides implementations in Python (`eyes-socket`), C++, and Java, along with a simple HTML frontend mock.

## Overview

The core idea is to maintain a chat history file and feed the recent history as context to the bot model on each interaction. This allows for a continuous conversation.

## `eyes-socket` (Python Implementation)

The most robust and recommended implementation, now available as a Python package.

### Installation

You can install `eyes-socket` from source:

```bash
pip install .
```

(Or, if uploaded to PyPI, simply `pip install eyes-socket`)

### Usage via CLI

Once installed, you can use the `eyes-socket` command globally:

```bash
eyes-socket --model "./path/to/your/model" --history "chat_history.txt"
```

Or you can continue using the wrapper script for backwards compatibility:

```bash
python3 bot_persistence.py --model "./path/to/your/model" --history "chat_history.txt"
```

**Options:**
- `--model`: Command to run the bot model executable (default: `./your-bot-model/chat`).
- `--history`: Path to the chat history file (default: `chat_history.txt`).

### Usage as a Python API

You can also use `eyes-socket` in your own Python scripts:

```python
from eyes_socket import EyesSocket

socket = EyesSocket(model_cmd="python3 mock_bot.py", history_file="my_history.txt")
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
# or
python3 bot_persistence.py --model "python3 mock_bot.py"
```

**To test the C++ implementation:**
```bash
g++ -o bot_persistence bot_persistence.cpp
./bot_persistence "python3 mock_bot.py" "history.txt"
```

**To test the Java implementation:**
```bash
javac ChatBot.java
java ChatBot "python3 mock_bot.py" "history.txt"
```

## License

See `MITLicense.txt`.
