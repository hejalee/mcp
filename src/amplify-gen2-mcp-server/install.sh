#!/bin/bash

# AWS Amplify Gen2 MCP Server Installation Script

set -e

echo "🚀 Installing AWS Amplify Gen2 MCP Server..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install the package
echo "📦 Installing package..."
uv pip install -e .

echo "✅ Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Add the MCP server configuration to your ~/.aws/amazonq/mcp.json file"
echo "2. Use the configuration from mcp-config-example.json"
echo "3. Restart your MCP client (e.g., Amazon Q CLI)"
echo ""
echo "🔧 Available tools:"
echo "- search_amplify_gen2_documentation_tool"
echo "- read_amplify_documentation_tool" 
echo "- get_amplify_gen2_guidance_tool"
echo "- generate_amplify_gen2_code_tool"
echo "- get_amplify_gen2_best_practices_tool"
echo "- troubleshoot_amplify_gen2_tool"
echo "- discover_amplify_project_templates_tool"
echo ""
echo "🎉 Ready to help with Amplify Gen2 development!"
