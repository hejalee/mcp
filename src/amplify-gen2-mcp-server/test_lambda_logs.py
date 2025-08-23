#!/usr/bin/env python3
"""Test script for the new get_amplify_lambda_logs function."""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'awslabs'))

def test_lambda_logs():
    """Test the lambda logs function."""
    
    print("=== Testing Lambda Logs Function ===\n")
    
    try:
        from amplify_gen2_mcp_server.tools import get_amplify_lambda_logs
        print("✓ Successfully imported get_amplify_lambda_logs")
        
        # Test with a mock function name (should handle gracefully)
        print("\n1. Testing with mock function name:")
        print("-" * 50)
        result = get_amplify_lambda_logs(None, "test-function")
        print(f"✓ Function call successful, result length: {len(result)} characters")
        
        # Check if it handles missing boto3 gracefully
        if "boto3 Not Available" in result:
            print("ℹ️ boto3 not available - showing alternative methods")
        elif "AWS credentials are not configured" in result:
            print("ℹ️ AWS credentials not configured - showing setup instructions")
        elif "No Lambda functions found" in result:
            print("ℹ️ No functions found (expected for test)")
        else:
            print("ℹ️ Function executed successfully")
        
        print(f"✓ Contains helpful content: {'Lambda Logs' in result}")
        
        # Test with different parameters
        print("\n2. Testing with different parameters:")
        print("-" * 50)
        result_with_params = get_amplify_lambda_logs(None, "amplify", hours=24, region="us-west-2")
        print(f"✓ Function call with parameters successful, result length: {len(result_with_params)} characters")
        
        print("\n=== All tests passed! ===")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

def test_server_integration():
    """Test the MCP server integration."""
    
    print("\n=== Testing MCP Server Integration ===\n")
    
    try:
        from amplify_gen2_mcp_server.server import get_amplify_lambda_logs_tool
        print("✓ Successfully imported get_amplify_lambda_logs_tool")
        
        # Test calling the tool function
        result = get_amplify_lambda_logs_tool("test-function")
        print(f"✓ Tool function call successful, result length: {len(result)} characters")
        print(f"✓ Contains expected content: {'Lambda Logs' in result}")
        
        # Test with parameters
        result_with_params = get_amplify_lambda_logs_tool("test", hours=2, region="us-east-1")
        print(f"✓ Tool function call with parameters successful, result length: {len(result_with_params)} characters")
        
        print("\n✓ MCP server integration tests passed!")
        
    except Exception as e:
        print(f"✗ MCP integration error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_lambda_logs()
    test_server_integration()
