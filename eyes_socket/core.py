import os
import shlex
import subprocess

class EyesSocket:
    def __init__(self, model_cmd, history_file="chat_history.txt"):
        self.model_cmd = model_cmd
        self.history_file = history_file
        self.chat_history = self.load_chat_history()

    def load_chat_history(self):
        """Loads chat history from the specified file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return f.read().splitlines()
            except IOError as e:
                print(f"Error loading history: {e}")
                return []
        return []

    def save_chat_history(self):
        """Saves chat history to the specified file."""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                f.write("\n".join(self.chat_history))
        except IOError as e:
            print(f"Error saving history: {e}")

    def add_user_input(self, text):
        self.chat_history.append("You: " + text)

    def add_bot_response(self, text):
        self.chat_history.append("Bot: " + text)

    def call_bot_model(self, prompt):
        """Calls the bot model executable with the prompt."""
        try:
            # Split command into a list properly handling quoted arguments
            if " " in self.model_cmd:
                command = shlex.split(self.model_cmd)
            else:
                command = [self.model_cmd]

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
            print(f"Error: Executable not found in command '{self.model_cmd}'")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def get_context(self, max_lines=1000):
        return "\n".join(self.chat_history[-max_lines:])

    def chat(self, user_input):
        if not user_input.strip():
            return None

        self.add_user_input(user_input)
        prompt = self.get_context()
        ai_response = self.call_bot_model(prompt)

        if ai_response:
            self.add_bot_response(ai_response)
            self.save_chat_history()
            return ai_response
        else:
            return None
