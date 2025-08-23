#!/usr/bin/env python3
"""
Test script to verify the custom functions documentation fix.
"""

import sys
import os

# Add the current directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from custom_functions_enhancement import get_custom_functions_documentation, enhanced_get_amplify_documentation

def test_custom_functions_documentation():
    """Test the custom functions documentation retrieval."""
    print("Testing custom functions documentation retrieval...")
    
    # Test direct custom functions documentation
    print("\n1. Testing direct custom functions documentation:")
    result = get_custom_functions_documentation("nextjs")
    print(f"Result length: {len(result)} characters")
    print("First 500 characters:")
    print(result[:500])
    print("...")
    
    # Test enhanced documentation function with custom functions topic
    print("\n2. Testing enhanced documentation with 'custom functions' topic:")
    result = enhanced_get_amplify_documentation("custom functions", "nextjs")
    print(f"Result length: {len(result)} characters")
    print("First 500 characters:")
    print(result[:500])
    print("...")
    
    # Test enhanced documentation function with general functions topic
    print("\n3. Testing enhanced documentation with 'functions' topic:")
    result = enhanced_get_amplify_documentation("functions", "nextjs")
    print(f"Result length: {len(result)} characters")
    print("First 500 characters:")
    print(result[:500])
    print("...")

if __name__ == "__main__":
    test_custom_functions_documentation()
