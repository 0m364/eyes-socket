######################
# bot-persistence_0.1             #
#                👀                            #
#####################

import os
import subprocess

CHAT_HISTORY_FILE = "your-bot-model_chat_history.txt"

def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as f:
            return f.read().splitlines()
    return []

def save_chat_history(chat_history):
    with open(CHAT_HISTORY_FILE, "w") as f:
        f.write("\n".join(chat_history))

def call_your_bot_model(prompt):
    your_bot_model_executable = "./your-bot-model/chat"
    response = subprocess.run([your_bot_model_executable, prompt], capture_output=True, text=True)
    return response.stdout.strip()

def main():
    chat_history = load_chat_history()

    while True:
        user_input = input("You: ")  # Prompting the user for input
        if user_input.lower() == "quit":
            break

        chat_history.append("You: " + user_input)  # Adding user input to chat history

        prompt = " ".join(chat_history[-1000:])  # Creating a prompt from the last 1000 lines of chat history
        ai_response = call_your_bot_model(prompt)  # Calling your bot model with the prompt
        print("Your bot model: " + ai_response)  # Printing the bot's response

        chat_history.append("Your bot model: " + ai_response)  # Adding bot's response to chat history
        save_chat_history(chat_history)  # Saving the updated chat history

if __name__ == "__main__":
    main()