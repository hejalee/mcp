#!/usr/bin/env python3
"""
Amplify Gen2 MCP Server Test Runner

This script specifically tests the Amplify Gen2 MCP server by temporarily
enabling it in the configuration and running comprehensive tests.
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path


def create_test_config(original_config_path: str) -> str:
    """Create a temporary config with Amplify Gen2 server enabled."""
    
    # Read original config
    with open(original_config_path, 'r') as f:
        config = json.load(f)
    
    # Enable the Amplify Gen2 server
    if 'awslabs.amplify-gen2-mcp-server' in config['mcpServers']:
        config['mcpServers']['awslabs.amplify-gen2-mcp-server']['disabled'] = False
    
    # Create temporary config file
    temp_fd, temp_path = tempfile.mkstemp(suffix='.json', prefix='mcp_test_')
    
    with os.fdopen(temp_fd, 'w') as f:
        json.dump(config, f, indent=2)
    
    return temp_path


def run_amplify_tests():
    """Run comprehensive tests for the Amplify Gen2 MCP server."""
    
    original_config = "/Users/hejalee/.aws/amazonq/mcp.json.backup"
    
    if not os.path.exists(original_config):
        print(f"❌ Original config file not found: {original_config}")
        return 1
    
    # Create temporary config with Amplify server enabled
    temp_config = create_test_config(original_config)
    
    try:
        print("🚀 Running Amplify Gen2 MCP Server Tests")
        print("=" * 60)
        
        # Import and run the test runner
        from aws_strands_test import AWSStrandsTestRunner
        
        # Initialize with temporary config
        runner = AWSStrandsTestRunner(temp_config)
        
        # Run tests specifically for Amplify Gen2 server
        amplify_server = "awslabs.amplify-gen2-mcp-server"
        
        if amplify_server not in runner.servers:
            print(f"❌ Amplify Gen2 server not found in configuration")
            return 1
        
        # Run the tests
        results = runner.run_tests_for_server(amplify_server)
        
        # Print summary
        runner.print_summary()
        
        # Return appropriate exit code
        failed_tests = sum(1 for r in results if not r.success)
        return 1 if failed_tests > 0 else 0
        
    finally:
        # Clean up temporary config
        if os.path.exists(temp_config):
            os.unlink(temp_config)


def run_local_function_tests():
    """Run tests directly against local Amplify functions."""
    
    print("\n🧪 Running Local Function Tests")
    print("=" * 60)
    
    # Add the awslabs directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    awslabs_dir = os.path.join(current_dir, 'awslabs')
    
    if awslabs_dir not in sys.path:
        sys.path.insert(0, awslabs_dir)
    
    try:
        from amplify_gen2_mcp_server.tools import (
            get_amplify_gen2_guidance,
            generate_amplify_gen2_code,
            get_amplify_gen2_best_practices,
            troubleshoot_amplify_gen2,
            get_amplify_lambda_logs
        )
        
        tests = [
            ("Guidance - Authentication", lambda: get_amplify_gen2_guidance(None, "authentication")),
            ("Guidance - Storage", lambda: get_amplify_gen2_guidance(None, "storage")),
            ("Code Gen - React Auth", lambda: generate_amplify_gen2_code(None, "authentication", "react")),
            ("Code Gen - Vue API", lambda: generate_amplify_gen2_code(None, "api", "vue")),
            ("Best Practices - Auth", lambda: get_amplify_gen2_best_practices(None, "authentication")),
            ("Troubleshoot - Deployment", lambda: troubleshoot_amplify_gen2(None, "deployment fails")),
            ("Lambda Logs - Test Function", lambda: get_amplify_lambda_logs(None, "test-function"))
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"  🧪 {test_name}... ", end="", flush=True)
            
            try:
                result = test_func()
                if result and len(result) > 0:
                    print(f"✅ PASS ({len(result)} chars)")
                    passed += 1
                else:
                    print("❌ FAIL (empty result)")
            except Exception as e:
                print(f"❌ ERROR: {e}")
        
        print(f"\n📊 Local Function Tests: {passed}/{total} passed")
        return 1 if passed < total else 0
        
    except ImportError as e:
        print(f"❌ Could not import Amplify tools: {e}")
        print("   Make sure you're in the correct directory and the tools are available")
        return 1


def main():
    """Main entry point."""
    
    if len(sys.argv) > 1 and sys.argv[1] == "--local-only":
        return run_local_function_tests()
    
    print("🎯 Amplify Gen2 MCP Server Test Suite")
    print("=" * 60)
    
    # Run MCP server tests
    mcp_result = run_amplify_tests()
    
    # Run local function tests
    local_result = run_local_function_tests()
    
    # Overall result
    overall_result = max(mcp_result, local_result)
    
    print("\n" + "=" * 60)
    if overall_result == 0:
        print("🎉 All Amplify Gen2 tests passed!")
    else:
        print("⚠️  Some Amplify Gen2 tests failed")
    
    return overall_result


if __name__ == "__main__":
    sys.exit(main())
