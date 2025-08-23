# Custom Functions Documentation Update

## Issue
The amplify-gen2-mcp-server currently doesn't properly reference the official custom functions documentation at `https://docs.amplify.aws/nextjs/build-a-backend/functions/custom-functions/` when users ask about implementing custom functions.

## Solution
Update the `tools.py` file to include specific handling for custom functions documentation.

## Changes Required

### 1. Add Custom Functions Documentation Function

Add this new function to `tools.py`:

```python
def get_custom_functions_documentation(framework: str = "nextjs") -> str:
    """Get specific documentation for Amplify Gen2 custom functions.

    Args:
        framework: The framework context (default: nextjs)

    Returns:
        Formatted custom functions documentation content
    """
    try:
        # Direct path to custom functions documentation
        custom_functions_path = f"src/pages/{framework}/build-a-backend/functions/custom-functions/index.mdx"
        
        # Try to fetch the custom functions documentation directly
        content = fetch_github_content(DOCUMENTATION_REPO, custom_functions_path)
        
        if not content:
            # Fallback paths for different frameworks
            fallback_paths = [
                f"src/pages/{framework}/build-a-backend/functions/custom-functions.mdx",
                f"src/pages/gen2/{framework}/build-a-backend/functions/custom-functions/index.mdx",
                "src/pages/nextjs/build-a-backend/functions/custom-functions/index.mdx"  # Default fallback
            ]
            
            for fallback_path in fallback_paths:
                content = fetch_github_content(DOCUMENTATION_REPO, fallback_path)
                if content:
                    break
        
        if content:
            # Truncate if too long
            if len(content) > 4000:
                content = content[:4000] + "\n\n... (content truncated)"

            return f"""
# Custom Functions Documentation

**Framework:** {framework.title()}
**Official URL:** https://docs.amplify.aws/{framework}/build-a-backend/functions/custom-functions/

{content}

## Key Concepts for Custom Functions

### 1. Defining Custom Functions
Custom functions in Amplify Gen2 are defined using the `defineFunction` utility:

```typescript
// amplify/functions/my-function/resource.ts
import {{ defineFunction }} from '@aws-amplify/backend';

export const myFunction = defineFunction({{
  name: 'my-function',
  entry: './handler.ts'
}});
```

### 2. Function Handler
Create your function logic in the handler file:

```typescript
// amplify/functions/my-function/handler.ts
import type {{ APIGatewayProxyHandler }} from 'aws-lambda';

export const handler: APIGatewayProxyHandler = async (event) => {{
  return {{
    statusCode: 200,
    body: JSON.stringify({{ message: 'Hello from custom function!' }})
  }};
}};
```

### 3. Adding to Backend
Include your function in the backend definition:

```typescript
// amplify/backend.ts
import {{ defineBackend }} from '@aws-amplify/backend';
import {{ myFunction }} from './functions/my-function/resource';

defineBackend({{
  myFunction
}});
```

## Related Documentation
- [Functions Overview](https://docs.amplify.aws/{framework}/build-a-backend/functions/)
- [Function Environment Variables](https://docs.amplify.aws/{framework}/build-a-backend/functions/environment-variables/)
- [Function Secrets](https://docs.amplify.aws/{framework}/build-a-backend/functions/secrets/)
            """
        
        return f"Could not fetch custom functions documentation for {framework}"

    except Exception as e:
        logger.error(f"Error getting custom functions documentation: {e}")
        return f"Error retrieving custom functions documentation: {str(e)}"
```

### 2. Update get_amplify_documentation Function

Modify the existing `get_amplify_documentation` function to handle custom functions:

```python
def get_amplify_documentation(topic: str, framework: str = "react") -> str:
    """Get comprehensive documentation for a specific Amplify topic.

    Args:
        topic: The topic to get documentation for
        framework: The framework context (default: react)

    Returns:
        Formatted documentation content
    """
    try:
        # Handle custom functions specifically
        if "custom" in topic.lower() and "function" in topic.lower():
            return get_custom_functions_documentation(framework)
        
        # Handle general functions topic
        if topic.lower() in ["functions", "function", "lambda"]:
            # Try to get both general functions and custom functions documentation
            general_functions = search_amplify_documentation("functions", limit=3)
            custom_functions_doc = get_custom_functions_documentation(framework)
            
            result = f"""
# Functions Documentation

## General Functions Overview
"""
            if general_functions:
                top_result = general_functions[0]
                content = fetch_raw_content(top_result['raw_url'])
                if content:
                    if len(content) > 2000:
                        content = content[:2000] + "\n\n... (content truncated)"
                    result += f"""
**Source:** {top_result['url']}

{content}

"""
            
            result += f"""
## Custom Functions

{custom_functions_doc}
"""
            return result
        
        # Original logic for other topics continues...
        doc_results = search_amplify_documentation(topic, limit=5)
        # ... rest of original function
```

### 3. Update Constants

Add custom functions to the core topics in `consts.py`:

```python
# Update core topics to include custom functions
AMPLIFY_TOPICS = [
    "authentication",
    "data", 
    "storage",
    "functions",
    "custom-functions",  # Add this
    "ai",
    "analytics", 
    "deployment",
    "hosting",
    "monitoring"
]
```

### 4. Update Search Scoring

In the `calculate_relevance_score_from_path` function, add boost for custom functions:

```python
# Add after existing boosts
# Boost for custom functions content
if 'custom-functions' in path_lower or 'custom_functions' in path_lower:
    score += 5.0
```

## Testing

After implementing these changes, test with queries like:
- "How do I implement custom functions in Amplify Gen2?"
- "Show me custom functions documentation"
- "Create a custom Lambda function with Amplify Gen2"

The server should now properly reference the official documentation at:
`https://docs.amplify.aws/nextjs/build-a-backend/functions/custom-functions/`

## Benefits

1. **Accurate Documentation**: Users get the correct, up-to-date custom functions documentation
2. **Framework-Specific**: Supports different frameworks (nextjs, react, vue, angular)
3. **Comprehensive Coverage**: Includes both general functions and custom functions documentation
4. **Fallback Handling**: Multiple fallback paths ensure documentation is found even if paths change
5. **Enhanced Search**: Better search relevance for custom functions queries
