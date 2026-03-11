from eyes_socket.plugins import create_model, OpenAIModel, AnthropicModel, OllamaModel, LocalModel

print("Testing Model Factory Integration")
m1 = create_model("openai:gpt-4o")
print(f"openai: prefix created: {type(m1).__name__} (expected OpenAIModel)")

m2 = create_model("anthropic:claude-3-opus-20240229")
print(f"anthropic: prefix created: {type(m2).__name__} (expected AnthropicModel)")

m3 = create_model("ollama:llama3")
print(f"ollama: prefix created: {type(m3).__name__} (expected OllamaModel)")

m4 = create_model("python3 mock_bot.py")
print(f"local command created: {type(m4).__name__} (expected LocalModel)")

print("\nTesting Model Invocation Missing Key handling")
print(f"OpenAI Call Missing Key: {m1.call('hello')}")
print(f"Anthropic Call Missing Key: {m2.call('hello')}")

print("\nSuccess!")
