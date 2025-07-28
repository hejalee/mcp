"""Tests for the Cloudscape MCP server."""

import pytest
from awslabs.cloudscape_mcp_server.server import handle_call_tool, handle_list_tools
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_list_tools():
    """Test that all expected tools are listed."""
    tools = await handle_list_tools()

    expected_tools = [
        'search_cloudscape_docs',
        'get_cloudscape_component_docs',
        'get_cloudscape_design_tokens',
        'search_cloudscape_demos',
        'get_demo_implementation',
        'analyze_demo_patterns',
    ]

    tool_names = [tool.name for tool in tools]

    for expected_tool in expected_tools:
        assert expected_tool in tool_names


@pytest.mark.asyncio
async def test_search_cloudscape_docs():
    """Test searching Cloudscape documentation."""
    with patch('awslabs.cloudscape_mcp_server.server.doc_searcher') as mock_searcher:
        mock_searcher.search_documentation = AsyncMock(return_value=[])

        result = await handle_call_tool('search_cloudscape_docs', {'query': 'button'})

        assert len(result) == 1
        assert 'No documentation found' in result[0].text
        mock_searcher.search_documentation.assert_called_once_with('button', 10)


@pytest.mark.asyncio
async def test_search_cloudscape_demos():
    """Test searching Cloudscape demos."""
    with patch('awslabs.cloudscape_mcp_server.server.demos_searcher') as mock_searcher:
        mock_searcher.search_demos = AsyncMock(return_value=[])

        result = await handle_call_tool('search_cloudscape_demos', {'query': 'table'})

        assert len(result) == 1
        assert 'No demo code found' in result[0].text
        mock_searcher.search_demos.assert_called_once_with('table', 10)


@pytest.mark.asyncio
async def test_invalid_tool():
    """Test calling an invalid tool."""
    result = await handle_call_tool('invalid_tool', {})

    assert len(result) == 1
    assert 'Error executing invalid_tool' in result[0].text
    assert 'Unknown tool: invalid_tool' in result[0].text
