import ollama

print("=" * 50)
print("🧠 ATS Bot Connection Test")
print("=" * 50)

# Test 1: Check if Ollama is accessible
print("\n📡 Test 1: Checking Ollama connection...")
try:
    response = ollama.list()
    print("✅ Ollama is running!")
    print(f"📦 Available models: {response}")
except Exception as e:
    print(f"❌ Ollama not accessible: {e}")
    exit(1)

# Test 2: Check if Mistral is available
print("\n📡 Test 2: Checking Mistral model...")
try:
    models = ollama.list()
    model_names = [m['name'] for m in models.get('models', [])]
    if any('mistral' in name for name in model_names):
        print("✅ Mistral model is available!")
    else:
        print("⚠️ Mistral not found. Available models:", model_names)
except Exception as e:
    print(f"❌ Error checking models: {e}")

# Test 3: Test Mistral response
print("\n📡 Test 3: Testing Mistral response...")
try:
    response = ollama.chat(model='mistral', messages=[
        {'role': 'user', 'content': 'Say "ATS bot is connected to Mistral!"'}
    ])
    print("✅ Mistral responded successfully!")
    print(f"💬 Response: {response['message']['content']}")
except Exception as e:
    print(f"❌ Mistral test failed: {e}")

print("\n" + "=" * 50)
print("✅ Connection test complete!")
print("=" * 50)
