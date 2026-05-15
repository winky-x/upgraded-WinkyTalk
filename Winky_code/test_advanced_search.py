#!/usr/bin/env python3
"""
Test advanced search functionality before integrating into agent
"""

import asyncio
import sys

async def test_search():
    # Import the advanced search
    from advanced_search import advanced_search
    
    test_queries = [
        "python programming",
        "artificial intelligence",
        "weather climate",
        "machine learning",
        "quantum computing"
    ]
    
    print("\n" + "="*70)
    print("TESTING ADVANCED SEARCH")
    print("="*70)
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 70)
        try:
            result = await advanced_search(query)
            if result:
                # Print first 300 chars of result
                preview = result[:300] if len(result) > 300 else result
                print(f"✅ SUCCESS\n{preview}...")
            else:
                print("❌ FAILED - No result returned")
        except Exception as e:
            print(f"❌ ERROR: {e}")

    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(test_search())
