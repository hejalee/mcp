#!/usr/bin/env python3
"""Test the new template discovery tool."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from awslabs.amplify_gen2_mcp_server.tools import discover_amplify_project_templates

def test_all_templates():
    """Test discovering all templates."""
    print("🚀 Testing All Templates Discovery")
    print("=" * 50)
    
    result = discover_amplify_project_templates(None)
    
    print("Full result:")
    print(result)
    
    return "Amplify Gen2 Project Templates" in result

def test_specific_framework():
    """Test discovering templates for a specific framework."""
    print("\n\n🎯 Testing React Template Discovery")
    print("=" * 50)
    
    result = discover_amplify_project_templates(None, "react")
    
    print("React template result:")
    print(result[:1000] + "..." if len(result) > 1000 else result)
    
    return "REACT Template" in result

def main():
    """Run template discovery tests."""
    print("🔍 Testing Template Discovery Tool\n")
    
    tests = [
        ("All Templates", test_all_templates),
        ("React Template", test_specific_framework)
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
        print("🎉 Template discovery tool working perfectly!")
        return 0
    else:
        print("⚠️ Some issues found")
        return 1

if __name__ == "__main__":
    sys.exit(main())
