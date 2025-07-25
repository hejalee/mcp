#!/usr/bin/env python3
"""Test script for the MCP tools directly."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from awslabs.amplify_gen2_mcp_server.tools import (
    search_amplify_gen2_documentation,
    get_amplify_gen2_guidance,
    troubleshoot_amplify_gen2,
    read_amplify_documentation
)

def test_search_tool():
    """Test the search tool."""
    print("🔍 Testing search_amplify_gen2_documentation tool...")
    
    result = search_amplify_gen2_documentation(None, "authentication", 3)
    
    print("Result preview:")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    return "Amplify Gen2 Documentation Search Results" in result

def test_guidance_tool():
    """Test the guidance tool."""
    print("💡 Testing get_amplify_gen2_guidance tool...")
    
    try:
        result = get_amplify_gen2_guidance(None, "authentication")
        
        print("Result preview:")
        print(result[:500] + "..." if len(result) > 500 else result)
        
        return len(result) > 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_troubleshoot_tool():
    """Test the troubleshoot tool."""
    print("🔧 Testing troubleshoot_amplify_gen2 tool...")
    
    try:
        result = troubleshoot_amplify_gen2(None, "deployment fails")
        
        print("Result preview:")
        print(result[:500] + "..." if len(result) > 500 else result)
        
        return len(result) > 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_read_documentation_tool():
    """Test the read documentation tool."""
    print("📖 Testing read_amplify_documentation tool...")
    
    try:
        # Use a URL from our search results
        url = "https://github.com/aws-amplify/docs/blob/main/public/images/gen2/q-developer/authentication.md"
        result = read_amplify_documentation(None, url, 1000)
        
        print("Result preview:")
        print(result[:500] + "..." if len(result) > 500 else result)
        
        return "Amplify Documentation Content" in result
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all MCP tool tests."""
    print("🚀 Starting MCP Tools Tests\n")
    
    tests = [
        ("Search Tool", test_search_tool),
        ("Guidance Tool", test_guidance_tool),
        ("Troubleshoot Tool", test_troubleshoot_tool),
        ("Read Documentation Tool", test_read_documentation_tool)
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
        print("🎉 All MCP tools working!")
        return 0
    else:
        print("⚠️ Some MCP tools failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
