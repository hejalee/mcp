# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the AWS Amplify Gen2 MCP Server main server module."""

from awslabs.amplify_gen2_mcp_server import server
from unittest.mock import patch


def test_server_initialization():
    """Test that the MCP server initializes correctly."""
    assert server.mcp is not None
    assert server.mcp.name == 'AWS Amplify Gen2 MCP Server'


def test_tool_registration():
    """Test that all tools are properly registered."""
    # Test that the tool functions exist and are callable
    expected_tools = [
        server.search_amplify_gen2_documentation_tool,
        server.read_amplify_documentation_tool,
        server.get_amplify_gen2_guidance_tool,
        server.generate_amplify_gen2_code_tool,
        server.get_amplify_gen2_best_practices_tool,
        server.discover_amplify_project_templates_tool,
        server.troubleshoot_amplify_gen2_tool
    ]

    for tool_func in expected_tools:
        assert callable(tool_func)


@patch('awslabs.amplify_gen2_mcp_server.server.mcp.run')
def test_main_function(mock_run):
    """Test the main function calls mcp.run()."""
    server.main()
    mock_run.assert_called_once()


def test_search_tool_wrapper():
    """Test the search tool wrapper function."""
    with patch('awslabs.amplify_gen2_mcp_server.server.search_amplify_gen2_documentation') as mock_search:
        mock_search.return_value = "test result"

        result = server.search_amplify_gen2_documentation_tool("test query", 5)

        mock_search.assert_called_once_with(None, "test query", 5)
        assert result == "test result"


def test_read_tool_wrapper():
    """Test the read documentation tool wrapper function."""
    with patch('awslabs.amplify_gen2_mcp_server.server.read_amplify_documentation') as mock_read:
        mock_read.return_value = "test content"

        result = server.read_amplify_documentation_tool("https://example.com", 1000)

        mock_read.assert_called_once_with(None, "https://example.com", 1000)
        assert result == "test content"
