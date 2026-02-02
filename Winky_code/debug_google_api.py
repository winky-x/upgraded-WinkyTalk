import requests
import json
import os
from config_manager import ConfigManager

print("=" * 70)
print("🔧 GOOGLE CUSTOM SEARCH API DEBUGGER")
print("=" * 70)

config = ConfigManager()
config.load_config()

api_key = config.get_api_key("google_search")
search_engine_id = config.get("api_keys.search_engine_id", "")

print(f"\n📊 CONFIGURATION:")
print(f"   API Key: {api_key[:10]}...{api_key[-4:] if api_key else 'Missing'}")
print(f"   Search Engine ID: {search_engine_id}")

if not api_key or not search_engine_id:
    print("\n❌ MISSING CONFIGURATION")
    exit()

print(f"\n🧪 TEST 1: Verify API Key (without Search Engine)")
url1 = "https://www.googleapis.com/customsearch/v1"
params1 = {
    "key": api_key,
    "cx": "test",  # Wrong ID to test API key
    "q": "test"
}

try:
    response1 = requests.get(url1, params=params1, timeout=10)
    print(f"   API Key Test Status: {response1.status_code}")
    
    if response1.status_code == 403:
        error_data = response1.json()
        error_msg = error_data.get("error", {}).get("message", "")
        print(f"   Error Message: {error_msg}")
        
        if "billing" in error_msg.lower():
            print("\n   💡 DIAGNOSIS: BILLING NOT ENABLED")
            print("   Solution: Enable billing at https://console.cloud.google.com/billing")
        elif "access" in error_msg.lower():
            print("\n   💡 DIAGNOSIS: API NOT ENABLED")
            print("   Solution: Enable Custom Search API at https://console.cloud.google.com/apis/library/customsearch.googleapis.com")
        elif "invalid" in error_msg.lower():
            print("\n   💡 DIAGNOSIS: INVALID API KEY")
            print("   Solution: Create new API key at https://console.cloud.google.com/apis/credentials")
    else:
        print(f"   Response: {response1.text[:200]}")
        
except Exception as e:
    print(f"   Test 1 Error: {e}")

print(f"\n🧪 TEST 2: Check API Services Enabled")
# Check what services are enabled for this API key
url2 = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={api_key}"
try:
    response2 = requests.get(url2, timeout=10)
    print(f"   API Services Check: {response2.status_code}")
    if response2.status_code == 200:
        print("   ✓ API key is valid format")
except:
    print("   ⚠️ Could not verify API key format")

print(f"\n🔗 QUICK FIX LINKS:")
print("   1. Enable Billing: https://console.cloud.google.com/billing")
print("   2. Enable Custom Search API: https://console.cloud.google.com/apis/library/customsearch.googleapis.com")
print("   3. Create New API Key: https://console.cloud.google.com/apis/credentials")
print("   4. Programmable Search Engine: https://programmablesearchengine.google.com/")

print("\n" + "=" * 70)
