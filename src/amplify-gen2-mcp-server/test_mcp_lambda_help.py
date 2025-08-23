#!/usr/bin/env python3
"""Test script for the MCP server lambda help tool."""

import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'awslabs'))

from amplify_gen2_mcp_server.server import mcp

async def test_mcp_lambda_help():
    """Test the MCP server lambda help tool."""
    
    print("=== Testing MCP Lambda Help Tool ===\n")
    
    # Get the tool
    tools = await mcp.list_tools()
    lambda_help_tool = None
    
    for tool in tools:
        if tool.name == 'get_amplify_lambda_help_tool':
            lambda_help_tool = tool
            break
    
    if lambda_help_tool:
        print(f"✓ Found lambda help tool: {lambda_help_tool.name}")
        print(f"  Description: {lambda_help_tool.description}")
        print(f"  Parameters: {lambda_help_tool.inputSchema}")
        print()
        
        # Test calling the tool
        try:
            result = await mcp.call_tool('get_amplify_lambda_help_tool', {})
            print(f"✓ Tool call successful")
            print(f"  Result length: {len(result.content[0].text)} characters")
            print(f"  Contains expected content: {'AWS Amplify Gen2 Lambda Functions' in result.content[0].text}")
            print()
            
            # Test with topic parameter
            result_with_topic = await mcp.call_tool('get_amplify_lambda_help_tool', {'topic': 'event'})
            print(f"✓ Tool call with topic successful")
            print(f"  Result length: {len(result_with_topic.content[0].text)} characters")
            print(f"  Contains topic-specific content: {'Event Object Deep Dive' in result_with_topic.content[0].text}")
            
        except Exception as e:
            print(f"✗ Tool call failed: {e}")
    else:
        print("✗ Lambda help tool not found")
        print("Available tools:")
        for tool in tools:
            print(f"  - {tool.name}")

if __name__ == "__main__":
    asyncio.run(test_mcp_lambda_help())
