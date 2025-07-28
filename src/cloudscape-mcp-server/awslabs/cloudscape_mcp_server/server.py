"""Main MCP server implementation for Cloudscape Design System."""

import asyncio
from .demos import CloudscapeDemosSearcher
from .documentation import CloudscapeDocumentationSearcher
from loguru import logger
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    Resource,
    TextContent,
    Tool,
)
from pydantic import AnyUrl
from typing import Any


# Initialize searchers
doc_searcher = CloudscapeDocumentationSearcher()
demos_searcher = CloudscapeDemosSearcher()

# Create MCP server
server = Server('cloudscape-mcp-server')


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri=AnyUrl('cloudscape://documentation'),
            name='Cloudscape Documentation',
            description='Access to Cloudscape Design System documentation',
            mimeType='text/plain',
        ),
        Resource(
            uri=AnyUrl('cloudscape://demos'),
            name='Cloudscape Demos',
            description='Access to Cloudscape demos repository',
            mimeType='text/plain',
        ),
    ]


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Read a specific resource."""
    if uri.scheme != 'cloudscape':
        raise ValueError(f'Unsupported URI scheme: {uri.scheme}')

    if uri.path == 'documentation':
        return 'Cloudscape Design System documentation search interface'
    elif uri.path == 'demos':
        return 'Cloudscape demos repository search interface'
    else:
        raise ValueError(f'Unknown resource path: {uri.path}')


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name='search_cloudscape_docs',
            description='Search Cloudscape Design System documentation for relevant content',
            inputSchema={
                'type': 'object',
                'properties': {
                    'query': {'type': 'string', 'description': 'Search query for documentation'},
                    'max_results': {
                        'type': 'integer',
                        'description': 'Maximum number of results to return',
                        'default': 10,
                    },
                },
                'required': ['query'],
            },
        ),
        Tool(
            name='get_cloudscape_component_docs',
            description='Get detailed documentation for a specific Cloudscape component',
            inputSchema={
                'type': 'object',
                'properties': {
                    'component_name': {
                        'type': 'string',
                        'description': "Name of the Cloudscape component (e.g., 'button', 'table', 'form')",
                    }
                },
                'required': ['component_name'],
            },
        ),
        Tool(
            name='get_cloudscape_design_tokens',
            description='Get Cloudscape design tokens (colors, spacing, typography, etc.)',
            inputSchema={
                'type': 'object',
                'properties': {
                    'category': {
                        'type': 'string',
                        'description': "Optional category filter (e.g., 'color', 'spacing', 'typography')",
                    }
                },
                'required': [],
            },
        ),
        Tool(
            name='search_cloudscape_demos',
            description='Search through Cloudscape demos repository for code examples',
            inputSchema={
                'type': 'object',
                'properties': {
                    'query': {'type': 'string', 'description': 'Search query for demo code'},
                    'max_results': {
                        'type': 'integer',
                        'description': 'Maximum number of results to return',
                        'default': 10,
                    },
                },
                'required': ['query'],
            },
        ),
        Tool(
            name='get_demo_implementation',
            description='Get implementation details for a specific demo',
            inputSchema={
                'type': 'object',
                'properties': {
                    'demo_name': {'type': 'string', 'description': 'Name of the demo to retrieve'}
                },
                'required': ['demo_name'],
            },
        ),
        Tool(
            name='analyze_demo_patterns',
            description='Analyze common patterns in Cloudscape demo implementations',
            inputSchema={
                'type': 'object',
                'properties': {
                    'component_name': {
                        'type': 'string',
                        'description': 'Optional component name to filter patterns',
                    }
                },
                'required': [],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == 'search_cloudscape_docs':
            query = arguments['query']
            max_results = arguments.get('max_results', 10)

            results = await doc_searcher.search_documentation(query, max_results)

            if not results:
                return [
                    TextContent(type='text', text=f'No documentation found for query: {query}')
                ]

            response_text = f"Found {len(results)} documentation results for '{query}':\\n\\n"

            for i, result in enumerate(results, 1):
                response_text += f'## {i}. {result.title}\\n'
                response_text += f'**URL:** {result.url}\\n'
                if result.component_type:
                    response_text += f'**Component Type:** {result.component_type}\\n'
                response_text += f'**Content:**\\n{result.content[:500]}...\\n\\n'

            return [TextContent(type='text', text=response_text)]

        elif name == 'get_cloudscape_component_docs':
            component_name = arguments['component_name']

            component_info = await doc_searcher.get_component_documentation(component_name)

            if not component_info:
                return [
                    TextContent(
                        type='text', text=f'No documentation found for component: {component_name}'
                    )
                ]

            response_text = f'# {component_info.name} Component\\n\\n'
            response_text += f'**Description:** {component_info.description}\\n\\n'

            if component_info.props:
                response_text += '## Props\\n'
                for prop in component_info.props:
                    response_text += f'- {prop}\\n'
                response_text += '\\n'

            if component_info.examples:
                response_text += '## Examples\\n'
                for i, example in enumerate(component_info.examples, 1):
                    response_text += f'### Example {i}\\n```\\n{example}\\n```\\n\\n'

            if component_info.related_components:
                response_text += '## Related Components\\n'
                for comp in component_info.related_components:
                    response_text += f'- {comp}\\n'

            return [TextContent(type='text', text=response_text)]

        elif name == 'get_cloudscape_design_tokens':
            category = arguments.get('category')

            tokens = await doc_searcher.get_design_tokens(category)

            if not tokens:
                category_text = f" for category '{category}'" if category else ''
                return [TextContent(type='text', text=f'No design tokens found{category_text}')]

            response_text = '# Cloudscape Design Tokens\\n\\n'
            if category:
                response_text += f'**Category:** {category}\\n\\n'

            # Group by category
            categories = {}
            for token in tokens:
                if token.category not in categories:
                    categories[token.category] = []
                categories[token.category].append(token)

            for cat, cat_tokens in categories.items():
                response_text += f'## {cat.title()}\\n\\n'
                for token in cat_tokens:
                    response_text += f'**{token.name}:** `{token.value}`'
                    if token.description:
                        response_text += f' - {token.description}'
                    response_text += '\\n'
                response_text += '\\n'

            return [TextContent(type='text', text=response_text)]

        elif name == 'search_cloudscape_demos':
            query = arguments['query']
            max_results = arguments.get('max_results', 10)

            results = await demos_searcher.search_demos(query, max_results)

            if not results:
                return [TextContent(type='text', text=f'No demo code found for query: {query}')]

            response_text = f"Found {len(results)} demo results for '{query}':\\n\\n"

            for i, result in enumerate(results, 1):
                response_text += f'## {i}. {result.demo_name}\\n'
                response_text += f'**File:** {result.file_path}\\n'
                if result.description:
                    response_text += f'**Description:** {result.description}\\n'
                if result.components_used:
                    response_text += f'**Components Used:** {", ".join(result.components_used)}\\n'
                response_text += f'**Code:**\\n```\\n{result.content[:1000]}...\\n```\\n\\n'

            return [TextContent(type='text', text=response_text)]

        elif name == 'get_demo_implementation':
            demo_name = arguments['demo_name']

            demo = await demos_searcher.get_demo_implementation(demo_name)

            if not demo:
                return [
                    TextContent(type='text', text=f'No demo implementation found for: {demo_name}')
                ]

            response_text = f'# {demo.demo_name} Implementation\\n\\n'
            response_text += f'**File:** {demo.file_path}\\n'
            if demo.description:
                response_text += f'**Description:** {demo.description}\\n'
            if demo.components_used:
                response_text += f'**Components Used:** {", ".join(demo.components_used)}\\n'
            response_text += f'\\n**Full Code:**\\n```\\n{demo.content}\\n```\\n'

            return [TextContent(type='text', text=response_text)]

        elif name == 'analyze_demo_patterns':
            component_name = arguments.get('component_name')

            patterns = await demos_searcher.analyze_demo_patterns(component_name)

            if not patterns:
                filter_text = f" for component '{component_name}'" if component_name else ''
                return [TextContent(type='text', text=f'No demo patterns found{filter_text}')]

            response_text = '# Demo Patterns Analysis\\n\\n'
            if component_name:
                response_text += f'**Filtered by component:** {component_name}\\n\\n'

            for i, pattern in enumerate(patterns, 1):
                response_text += f'## Pattern {i}: {pattern.demo_name}\\n'
                response_text += f'**File:** {pattern.file_path}\\n'
                if pattern.components_used:
                    response_text += f'**Components:** {", ".join(pattern.components_used)}\\n'
                response_text += f'**Code Sample:**\\n```\\n{pattern.content[:800]}...\\n```\\n\\n'

            return [TextContent(type='text', text=response_text)]

        else:
            raise ValueError(f'Unknown tool: {name}')

    except Exception as e:
        logger.error(f'Error in tool {name}: {e}')
        return [TextContent(type='text', text=f'Error executing {name}: {str(e)}')]


async def main():
    """Main entry point for the server."""
    # Import here to avoid issues with event loops
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name='cloudscape-mcp-server',
                server_version='1.0.0',
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )


if __name__ == '__main__':
    asyncio.run(main())
