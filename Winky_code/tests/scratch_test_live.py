import asyncio
import os
import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

async def test_connect():
    # Load config
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "user_config.json"))
    if not os.path.exists(config_path):
        print(f"Error: Config not found at {config_path}")
        return
        
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    api_key = config.get("api_keys", {}).get("google")
    if not api_key:
        print("Error: No Google API key found in user_config.json")
        return
        
    print(f"Testing API key: {api_key[:8]}...{api_key[-6:] if len(api_key) > 14 else ''}")
    
    from google.genai import Client
    
    client = Client(api_key=api_key)
    
    # 1. Verify API key authentication
    try:
        print("\n[Step 1] Attempting to list models to verify authentication...")
        models_list = list(client.models.list())
        print("✔ Authentication Successful. Found models:")
        # Print a few Gemini models
        for m in models_list:
            if "gemini" in m.name.lower():
                print(f"  - {m.name}")
    except Exception as e:
        print(f"✖ Authentication Failed: {e}")
        print("Please check if your API key is correct and valid.")
        return

    # 2. Test Live Bidirectional connection
    live_models = [
        "gemini-2.5-flash-native-audio-latest"
    ]
    
    for model_name in live_models:
        try:
            print(f"\n[Step 2] Attempting to connect to Live model: {model_name}...")
            async with client.aio.live.connect(model=model_name) as session:
                print(f"✔ Live API Connection Successful for {model_name}!")
                return
        except Exception as e:
            print(f"✖ Live API Connection Failed for {model_name}: {e}")

if __name__ == "__main__":
    asyncio.run(test_connect())
