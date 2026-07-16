import ollama

print("🧠 Testing Mistral connection...")

try:
    response = ollama.chat(model='mistral', messages=[
        {'role': 'user', 'content': 'Say "I am connected to the ATS bot!"'}
    ])
    print("✅ SUCCESS! Mistral is connected!")
    print(f"Response: {response['message']['content']}")
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("Make sure Ollama is running: ollama serve")
