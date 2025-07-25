#!/bin/sh
# Simple health check for the MCP server
# This script checks if the process is running

set -e

# Check if the process is running
if pgrep -f "python -m awslabs.amplify_gen2_mcp_server" > /dev/null; then
    exit 0
else
    exit 1
fi
