"""Usage examples for the Cloudscape MCP Server.

This file demonstrates how to use the various tools provided by the server.
"""

# Example prompts you can use with your AI assistant:

DOCUMENTATION_EXAMPLES = [
    'Using the Cloudscape MCP server, search for documentation about the Button component and show me its available props and usage examples.',
    'Get detailed documentation for the Table component from Cloudscape, including all its props and examples.',
    'Show me all the color design tokens available in Cloudscape Design System.',
    'Search Cloudscape documentation for information about accessibility best practices.',
    'Find documentation about form validation patterns in Cloudscape.',
]

DEMO_EXAMPLES = [
    'Search the Cloudscape demos for examples of data tables with filtering and sorting functionality.',
    "Get the implementation details for the 'dashboard' demo from the Cloudscape demos repository.",
    'Analyze common patterns for form components across all Cloudscape demos.',
    'Find demo code that shows how to implement a multi-step wizard using Cloudscape components.',
    'Search for examples of responsive layouts in the Cloudscape demos.',
]

PATTERN_ANALYSIS_EXAMPLES = [
    'Analyze how the Button component is typically used across different Cloudscape demos.',
    'Show me common patterns for error handling in Cloudscape demo applications.',
    'Find examples of how to implement custom themes with Cloudscape components.',
    'Analyze patterns for data visualization components in the demos repository.',
]

# Example of how the tools work programmatically (for reference):

TOOL_EXAMPLES = {
    'search_cloudscape_docs': {'query': 'button accessibility', 'max_results': 5},
    'get_cloudscape_component_docs': {'component_name': 'table'},
    'get_cloudscape_design_tokens': {'category': 'color'},
    'search_cloudscape_demos': {'query': 'data table pagination', 'max_results': 10},
    'get_demo_implementation': {'demo_name': 'dashboard'},
    'analyze_demo_patterns': {'component_name': 'form'},
}

if __name__ == '__main__':
    print('Cloudscape MCP Server Usage Examples')
    print('=====================================')
    print()
    print('Documentation Examples:')
    for i, example in enumerate(DOCUMENTATION_EXAMPLES, 1):
        print(f'{i}. {example}')
    print()
    print('Demo Examples:')
    for i, example in enumerate(DEMO_EXAMPLES, 1):
        print(f'{i}. {example}')
    print()
    print('Pattern Analysis Examples:')
    for i, example in enumerate(PATTERN_ANALYSIS_EXAMPLES, 1):
        print(f'{i}. {example}')
