import ollama

print("🤖 Testing Ollama AI...")

# Try which model you have
models_to_try = ["mistral", "tinyllama", "llama2"]

for model in models_to_try:
    try:
        print(f"Trying model: {model}...")
        response = ollama.chat(model=model, messages=[
            {'role': 'user', 'content': 'What is an ATS resume analyzer? Answer in one sentence.'}
        ])
        print(f"\n✅ Success with {model}!")
        print("🧠 AI Response:")
        print(response['message']['content'])
        break
    except Exception as e:
        print(f"❌ {model} not available: {e}")
