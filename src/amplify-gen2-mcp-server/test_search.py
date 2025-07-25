#!/usr/bin/env python3
"""Test script for the Amplify Gen2 MCP server document search functionality."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from awslabs.amplify_gen2_mcp_server.tools import (
    search_amplify_documentation,
    search_amplify_gen2_documentation,
    fetch_github_content,
    fetch_raw_content
)

def test_basic_search():
    """Test basic documentation search functionality."""
    print("🔍 Testing basic documentation search...")
    
    # Test search for authentication
    results = search_amplify_documentation("authentication", limit=3)
    
    print(f"Found {len(results)} results for 'authentication':")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Path: {result['path']}")
        print(f"   Score: {result['relevance_score']:.1f}")
        print()
    
    return len(results) > 0

def test_content_fetch():
    """Test fetching content from GitHub."""
    print("📄 Testing content fetching...")
    
    # Test fetching a specific file that we know exists from our search results
    content = fetch_github_content("aws-amplify/docs", "public/images/gen2/q-developer/authentication.md")
    
    if content:
        print(f"Successfully fetched content ({len(content)} characters)")
        print("First 200 characters:")
        print(content[:200] + "..." if len(content) > 200 else content)
        return True
    else:
        print("Failed to fetch content")
        return False

def test_full_search_tool():
    """Test the complete search tool."""
    print("🛠️ Testing full search tool...")
    
    # Test the main search function
    result = search_amplify_gen2_documentation(None, "authentication", limit=3)
    
    print("Search tool result:")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    return "Amplify Gen2 Documentation Search Results" in result

def main():
    """Run all tests."""
    print("🚀 Starting Amplify Gen2 MCP Server Tests\n")
    
    tests = [
        ("Basic Search", test_basic_search),
        ("Content Fetch", test_content_fetch),
        ("Full Search Tool", test_full_search_tool)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED\n")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED\n")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}\n")
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
