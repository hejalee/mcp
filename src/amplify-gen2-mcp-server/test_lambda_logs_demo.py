#!/usr/bin/env python3
"""Demo script showing the lambda logs function output."""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'awslabs'))

def demo_lambda_logs():
    """Demo the lambda logs function output."""
    
    print("=== Lambda Logs Function Demo ===\n")
    
    try:
        from amplify_gen2_mcp_server.tools import get_amplify_lambda_logs
        
        # Demo 1: Function not found (typical case when testing)
        print("1. Demo: Searching for a function that doesn't exist")
        print("=" * 60)
        result = get_amplify_lambda_logs(None, "demo-function")
        print(result[:500] + "..." if len(result) > 500 else result)
        print("\n")
        
        # Demo 2: With different parameters
        print("2. Demo: Using different parameters")
        print("=" * 60)
        result = get_amplify_lambda_logs(None, "amplify", hours=24, region="us-west-2", profile="dev")
        print(result[:500] + "..." if len(result) > 500 else result)
        print("\n")
        
        # Demo 3: Show the help content when boto3 is not available
        print("3. Demo: What users see when boto3 is not available")
        print("=" * 60)
        # Temporarily simulate boto3 not being available
        import awslabs.amplify_gen2_mcp_server.tools as tools_module
        original_boto3_available = tools_module.BOTO3_AVAILABLE
        tools_module.BOTO3_AVAILABLE = False
        
        result = get_amplify_lambda_logs(None, "test-function")
        print(result)
        
        # Restore original state
        tools_module.BOTO3_AVAILABLE = original_boto3_available
        
        print("\n=== Demo completed! ===")
        
    except Exception as e:
        print(f"Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_lambda_logs()
