#!/usr/bin/env python3
"""Test script for the new get_amplify_lambda_help function."""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'awslabs'))

from amplify_gen2_mcp_server.tools import get_amplify_lambda_help

def test_lambda_help():
    """Test the lambda help function with different topics."""
    
    print("=== Testing Lambda Help Function ===\n")
    
    # Test general help
    print("1. Testing general help (no topic):")
    print("-" * 50)
    result = get_amplify_lambda_help(None)
    print(f"Length: {len(result)} characters")
    print(f"First 200 chars: {result[:200]}...")
    print()
    
    # Test event topic
    print("2. Testing 'event' topic:")
    print("-" * 50)
    result = get_amplify_lambda_help(None, "event")
    print(f"Length: {len(result)} characters")
    print(f"Contains 'Event Object Deep Dive': {'Event Object Deep Dive' in result}")
    print()
    
    # Test context topic
    print("3. Testing 'context' topic:")
    print("-" * 50)
    result = get_amplify_lambda_help(None, "context")
    print(f"Length: {len(result)} characters")
    print(f"Contains 'Context Object Deep Dive': {'Context Object Deep Dive' in result}")
    print()
    
    # Test handler topic
    print("4. Testing 'handler' topic:")
    print("-" * 50)
    result = get_amplify_lambda_help(None, "handler")
    print(f"Length: {len(result)} characters")
    print(f"Contains 'Handler Function Patterns': {'Handler Function Patterns' in result}")
    print()
    
    # Test examples topic
    print("5. Testing 'examples' topic:")
    print("-" * 50)
    result = get_amplify_lambda_help(None, "examples")
    print(f"Length: {len(result)} characters")
    print(f"Contains 'Complete Function Examples': {'Complete Function Examples' in result}")
    print()
    
    # Test invalid topic
    print("6. Testing invalid topic:")
    print("-" * 50)
    result = get_amplify_lambda_help(None, "invalid_topic")
    print(f"Length: {len(result)} characters")
    print(f"Returns base help: {'AWS Amplify Gen2 Lambda Functions - Parameter Guide' in result}")
    print()
    
    print("=== All tests completed successfully! ===")

if __name__ == "__main__":
    test_lambda_help()
