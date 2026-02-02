import os
import requests
from config_manager import ConfigManager

config = ConfigManager()
config.load_config()

api_key = config.get_api_key("google_search")
search_id = config.get("api_keys.search_engine_id", "")

print("🔍 DEBUGGING URL CONSTRUCTION")
print("=" * 50)
print(f"API Key: {api_key[:15]}...")
print(f"Search Engine ID: {search_id}")
print(f"Query: 'test search'")

# Method 1: Using params (CORRECT)
url1 = "https://www.googleapis.com/customsearch/v1"
params1 = {
    "key": api_key,
    "cx": search_id,
    "q": "test search",
    "num": 1
}

print(f"\n🧪 Method 1 (Using params):")
print(f"URL: {url1}")
print(f"Params: {params1}")

# Method 2: String concatenation (WRONG but let's check)
url2 = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_id}&q=test%20search&num=1"
print(f"\n🧪 Method 2 (String concat):")
print(f"URL: {url2[:100]}...")

# Test both methods
print(f"\n🔧 Testing Method 1...")
try:
    response1 = requests.get(url1, params=params1, timeout=5)
    print(f"Status: {response1.status_code}")
    if response1.status_code != 200:
        print(f"Error: {response1.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print(f"\n🔧 Testing Method 2...")
try:
    response2 = requests.get(url2, timeout=5)
    print(f"Status: {response2.status_code}")
    if response2.status_code != 200:
        print(f"Error: {response2.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print(f"\n✅ Recommendation: Always use Method 1 (params dict)")
