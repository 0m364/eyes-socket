import os
from .plugins import create_model

class EyesSocket:
    def __init__(self, model_cmds, history_file="chat_history.txt"):
        # Support both single string (for backwards compatibility) and lists
        if isinstance(model_cmds, str):
            model_cmds = [model_cmds]

        self.models = [create_model(cmd) for cmd in model_cmds]
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

    def add_bot_response(self, text, model_name="Bot"):
        self.chat_history.append(f"{model_name}: {text}")

    def get_context(self, max_lines=1000):
        return "\n".join(self.chat_history[-max_lines:])

    def chat(self, user_input, rounds=1):
        if not user_input.strip():
            return None

        self.add_user_input(user_input)
        responses = []

        for _ in range(rounds):
            for model in self.models:
                prompt = self.get_context()
                ai_response = model.call(prompt)

                if ai_response:
                    model_name = "Bot" if len(self.models) == 1 else f"Bot ({model.uri})"
                    self.add_bot_response(ai_response, model_name=model_name)
                    responses.append((model_name, ai_response))
                else:
                    responses.append((model.uri, "[No response or error]"))

        self.save_chat_history()

        if len(self.models) == 1 and rounds == 1:
             # Backward compatibility: return single string
             return responses[0][1] if responses else None
        else:
             # New behavior: return list of (model_name, response) tuples
             return responses
