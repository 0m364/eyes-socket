#!/usr/bin/env python3
"""
Bot Persistence - A simple CLI for persistent chat with a local bot model.
"""

import os
import subprocess
import argparse
import sys
import shlex

def load_chat_history(filepath):
    """Loads chat history from the specified file."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read().splitlines()
        except IOError as e:
            print(f"Error loading history: {e}")
            return []
    return []

def save_chat_history(filepath, chat_history):
    """Saves chat history to the specified file."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(chat_history))
    except IOError as e:
        print(f"Error saving history: {e}")

def call_bot_model(executable_cmd, prompt):
    """Calls the bot model executable with the prompt."""
    try:
        # Split command into a list properly handling quoted arguments
        if " " in executable_cmd:
            command = shlex.split(executable_cmd)
        else:
            command = [executable_cmd]

        command.append(prompt)

        response = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return response.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error calling bot model: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"Error: Executable not found in command '{executable_cmd}'")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Chat with a local bot model with persistent history.")
    parser.add_argument("--model", type=str, default="./your-bot-model/chat", help="Command to run the bot model executable.")
    parser.add_argument("--history", type=str, default="chat_history.txt", help="Path to the chat history file.")
    args = parser.parse_args()

    chat_history = load_chat_history(args.history)
    print(f"Loaded {len(chat_history)} lines of history from '{args.history}'.")
    print("Type 'quit' or 'exit' to end the session.")

    try:
        while True:
            try:
                user_input = input("You: ")
            except EOFError:
                break

            if user_input.lower() in ("quit", "exit"):
                break

            if not user_input.strip():
                continue

            chat_history.append("You: " + user_input)

            # Limit context to last 1000 lines to prevent overflow
            context = chat_history[-1000:]
            prompt = "\n".join(context)

            ai_response = call_bot_model(args.model, prompt)

            if ai_response:
                print(f"Bot: {ai_response}")
                chat_history.append("Bot: " + ai_response)
                save_chat_history(args.history, chat_history)
            else:
                print("Bot: [No response or error]")

    except KeyboardInterrupt:
        print("\nExiting...")

    print("Goodbye!")

if __name__ == "__main__":
    main()
