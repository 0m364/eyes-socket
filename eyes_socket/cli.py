import argparse
import sys
from .core import EyesSocket

def main():
    parser = argparse.ArgumentParser(description="Chat with local bot models with persistent history.")
    parser.add_argument("--model", type=str, action="append", help="Command to run the bot model executable or API URL or browser: URL. Can be specified multiple times to chain models.")
    parser.add_argument("--rounds", type=int, default=1, help="Number of conversational rounds if chaining multiple models.")
    parser.add_argument("--history", type=str, default="chat_history.txt", help="Path to the chat history file.")
    args = parser.parse_args()

    # Default to mock_bot.py if no models specified
    models = args.model if args.model else ["./your-bot-model/chat"]

    socket = EyesSocket(model_cmds=models, history_file=args.history)
    print(f"Loaded {len(socket.chat_history)} lines of history from '{args.history}'.")
    print(f"Loaded {len(models)} models.")
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

            # Support both backwards compatibility (single response string) and multi-model (list of tuples)
            ai_responses = socket.chat(user_input, rounds=args.rounds)

            if isinstance(ai_responses, list):
                for model_name, response in ai_responses:
                    print(f"{model_name}: {response}")
            elif ai_responses:
                print(f"Bot: {ai_responses}")
            else:
                print("Bot: [No response or error]")

    except KeyboardInterrupt:
        print("\nExiting...")

    print("Goodbye!")

if __name__ == "__main__":
    main()
