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

"""Main entry point for the AWS Amplify Gen2 MCP Server."""

import os
import sys
from .consts import DEFAULT_CONTENT_LENGTH, DEFAULT_SEARCH_LIMIT
from .tools import (
    discover_amplify_project_templates,
    generate_amplify_gen2_code,
    get_amplify_gen2_best_practices,
    get_amplify_gen2_guidance,
    read_amplify_documentation,
    search_amplify_gen2_documentation,
    troubleshoot_amplify_gen2,
)
from loguru import logger
from mcp.server.fastmcp import FastMCP


# Set up logging
logger.remove()
logger.add(sys.stderr, level=os.getenv('FASTMCP_LOG_LEVEL', 'WARNING'))

# Create MCP server
mcp = FastMCP(
    'AWS Amplify Gen2 MCP Server',
    dependencies=[
        'pydantic',
        'requests',
    ]
)


@mcp.tool()
def search_amplify_gen2_documentation_tool(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> str:
    """Search Amplify Gen2 documentation comprehensively across official docs and sample repositories.

    Args:
        query: Search query string (e.g., "authentication", "data modeling", "file upload")
        limit: Maximum number of results to return (default: 10)

    Returns:
        Comprehensive search results with URLs, relevance scores, and code examples
    """
    return search_amplify_gen2_documentation(None, query, limit)


@mcp.tool()
def read_amplify_documentation_tool(url: str, max_length: int = DEFAULT_CONTENT_LENGTH) -> str:
    """Read specific Amplify documentation content from a URL.

    Args:
        url: URL to the documentation (GitHub or raw URL)
        max_length: Maximum length of content to return (default: 5000)

    Returns:
        Full documentation content in markdown format
    """
    return read_amplify_documentation(None, url, max_length)


@mcp.tool()
def get_amplify_gen2_guidance_tool(topic: str) -> str:
    """Get comprehensive guidance on Amplify Gen2 development topics.

    Args:
        topic: The topic to get guidance on (e.g., "authentication", "data", "storage")

    Returns:
        Comprehensive guidance from official documentation and sample repositories
    """
    return get_amplify_gen2_guidance(None, topic)


@mcp.tool()
def generate_amplify_gen2_code_tool(feature: str, framework: str) -> str:
    """Generate Amplify Gen2 code snippets and configurations using official samples.

    Args:
        feature: The Amplify feature to generate code for (e.g., "authentication", "data", "storage")
        framework: The frontend framework to use (e.g., "React", "Vue", "Angular", "Next.js")

    Returns:
        Generated code from official sample repositories and documentation
    """
    return generate_amplify_gen2_code(None, feature, framework)


@mcp.tool()
def get_amplify_gen2_best_practices_tool(area: str) -> str:
    """Get best practices for Amplify Gen2 development.

    Args:
        area: The area to get best practices for (e.g., "authentication", "data_modeling", "security")

    Returns:
        Best practices and recommendations for the specified area
    """
    return get_amplify_gen2_best_practices(None, area)


@mcp.tool()
def discover_amplify_project_templates_tool(framework: str = None) -> str:
    """Discover available Amplify Gen2 project templates and starter projects.

    Args:
        framework: Optional framework filter (react, vue, angular, next, ai)

    Returns:
        Comprehensive information about available project templates with setup instructions
    """
    return discover_amplify_project_templates(None, framework)


@mcp.tool()
def troubleshoot_amplify_gen2_tool(issue: str) -> str:
    """Get troubleshooting guidance for common Amplify Gen2 issues.

    Args:
        issue: The issue to troubleshoot (e.g., "deployment fails", "authentication error", "data not loading")

    Returns:
        Comprehensive troubleshooting guidance from official sources
    """
    return troubleshoot_amplify_gen2(None, issue)


def main():
    """Run the MCP server with CLI argument support."""
    mcp.run()


if __name__ == '__main__':
    main()
