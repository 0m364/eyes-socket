import argparse
import sys
from .core import EyesSocket

def main():
    parser = argparse.ArgumentParser(description="Chat with a local bot model with persistent history.")
    parser.add_argument("--model", type=str, default="./your-bot-model/chat", help="Command to run the bot model executable.")
    parser.add_argument("--history", type=str, default="chat_history.txt", help="Path to the chat history file.")
    args = parser.parse_args()

    socket = EyesSocket(model_cmd=args.model, history_file=args.history)
    print(f"Loaded {len(socket.chat_history)} lines of history from '{args.history}'.")
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

            ai_response = socket.chat(user_input)

            if ai_response:
                print(f"Bot: {ai_response}")
            else:
                print("Bot: [No response or error]")

    except KeyboardInterrupt:
        print("\nExiting...")

    print("Goodbye!")

if __name__ == "__main__":
    main()
