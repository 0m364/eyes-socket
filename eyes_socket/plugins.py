import os
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
            data = json.dumps({"prompt": prompt}).encode('utf-8')
            req = urllib.request.Request(self.uri, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=30) as response:
                result = response.read().decode('utf-8')
                try:
                    json_res = json.loads(result)
                    if "response" in json_res:
                        return json_res["response"]
                    elif "text" in json_res:
                        return json_res["text"]
                    elif "message" in json_res:
                         return json_res["message"]
                    return result
                except json.JSONDecodeError:
                    return result.strip()
        except Exception as e:
            print(f"Error calling API model '{self.uri}': {e}")
            return None

class BrowserZeroAuthModel(BaseModel):
    def call(self, prompt: str) -> str:
        print(f"Simulating Browser/0-Auth call to: {self.uri}")
        print(f"Prompt sent: {prompt}")
        return f"[Browser Model {self.uri} Response]: Simulated response to '{prompt[:20]}...'"

class OpenAIModel(BaseModel):
    def __init__(self, uri: str):
        super().__init__(uri)
        self.model_name = uri[len("openai:"):] if uri.startswith("openai:") else uri
        if not self.model_name:
            self.model_name = "gpt-3.5-turbo"

    def call(self, prompt: str) -> str:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return "Error: OPENAI_API_KEY environment variable not set."

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"Error calling OpenAI API '{self.uri}': {e}"

class AnthropicModel(BaseModel):
    def __init__(self, uri: str):
        super().__init__(uri)
        self.model_name = uri[len("anthropic:"):] if uri.startswith("anthropic:") else uri
        if not self.model_name:
            self.model_name = "claude-3-haiku-20240307"

    def call(self, prompt: str) -> str:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return "Error: ANTHROPIC_API_KEY environment variable not set."

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
        data = {
            "model": self.model_name,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['content'][0]['text'].strip()
        except Exception as e:
            return f"Error calling Anthropic API '{self.uri}': {e}"

class OllamaModel(BaseModel):
    def __init__(self, uri: str):
        super().__init__(uri)
        self.model_name = uri[len("ollama:"):] if uri.startswith("ollama:") else uri
        if not self.model_name:
            self.model_name = "llama2"

    def call(self, prompt: str) -> str:
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        url = f"{host}/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('response', '').strip()
        except Exception as e:
            return f"Error calling Ollama API '{self.uri}': {e}"

def create_model(model_uri: str) -> BaseModel:
    if model_uri.startswith("openai:"):
        return OpenAIModel(model_uri)
    elif model_uri.startswith("anthropic:"):
        return AnthropicModel(model_uri)
    elif model_uri.startswith("ollama:"):
        return OllamaModel(model_uri)
    elif model_uri.startswith("http://") or model_uri.startswith("https://"):
        return APIModel(model_uri)
    elif model_uri.startswith("browser:"):
        return BrowserZeroAuthModel(model_uri[len("browser:"):])
    else:
        return LocalModel(model_uri)
