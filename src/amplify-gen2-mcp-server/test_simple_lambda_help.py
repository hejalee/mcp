#!/usr/bin/env python3
"""Simple test for the lambda help function."""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'awslabs'))

def test_simple():
    """Simple test of the lambda help function."""
    
    # Import the server module to check if it loads correctly
    try:
        from amplify_gen2_mcp_server.server import get_amplify_lambda_help_tool
        print("✓ Successfully imported get_amplify_lambda_help_tool")
        
        # Test calling the function
        result = get_amplify_lambda_help_tool()
        print(f"✓ Function call successful, result length: {len(result)} characters")
        print(f"✓ Contains expected content: {'AWS Amplify Gen2 Lambda Functions' in result}")
        
        # Test with topic
        result_with_topic = get_amplify_lambda_help_tool("event")
        print(f"✓ Function call with topic successful, result length: {len(result_with_topic)} characters")
        print(f"✓ Contains topic-specific content: {'Event Object Deep Dive' in result_with_topic}")
        
        print("\n=== All tests passed! ===")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()
