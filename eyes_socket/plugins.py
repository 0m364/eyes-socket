import shlex
import subprocess
import urllib.request
import urllib.parse
import json

class BaseModel:
    def __init__(self, uri: str):
        self.uri = uri

    def call(self, prompt: str) -> str:
        raise NotImplementedError("Subclasses must implement call()")

    def get_name(self) -> str:
        return self.uri

class LocalModel(BaseModel):
    def call(self, prompt: str) -> str:
        try:
            if " " in self.uri:
                command = shlex.split(self.uri)
            else:
                command = [self.uri]

            command.append(prompt)

            response = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return response.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error calling local model '{self.uri}': {e}")
            print(f"Stderr: {e.stderr}")
            return None
        except FileNotFoundError:
            print(f"Error: Executable not found in command '{self.uri}'")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

class APIModel(BaseModel):
    def call(self, prompt: str) -> str:
        try:
            # Basic POST request, assumes a specific JSON format for the prompt
            # Can be customized further based on specific API needs
            data = json.dumps({"prompt": prompt}).encode('utf-8')
            req = urllib.request.Request(self.uri, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as response:
                result = response.read().decode('utf-8')
                # Attempt to parse as JSON if possible
                try:
                    json_res = json.loads(result)
                    if "response" in json_res:
                        return json_res["response"]
                    elif "text" in json_res:
                        return json_res["text"]
                    elif "message" in json_res:
                         return json_res["message"]
                    return result # Return raw string if we can't find a standard key
                except json.JSONDecodeError:
                    return result.strip()
        except Exception as e:
            print(f"Error calling API model '{self.uri}': {e}")
            return None

class BrowserZeroAuthModel(BaseModel):
    def call(self, prompt: str) -> str:
        # Placeholder for browser automation/0-auth logic.
        # This would typically use selenium, playwright, etc.
        # For now, it returns a simulated response.
        print(f"Simulating Browser/0-Auth call to: {self.uri}")
        print(f"Prompt sent: {prompt}")
        return f"[Browser Model {self.uri} Response]: Simulated response to '{prompt[:20]}...'"

def create_model(model_uri: str) -> BaseModel:
    if model_uri.startswith("http://") or model_uri.startswith("https://"):
        return APIModel(model_uri)
    elif model_uri.startswith("browser:"):
        return BrowserZeroAuthModel(model_uri[len("browser:"):])
    else:
        return LocalModel(model_uri)
