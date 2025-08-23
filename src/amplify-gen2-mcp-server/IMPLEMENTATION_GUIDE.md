# Implementation Guide: Custom Functions Documentation Update

## Overview

This guide provides step-by-step instructions to update the amplify-gen2-mcp-server so that it properly references the official custom functions documentation at `https://docs.amplify.aws/nextjs/build-a-backend/functions/custom-functions/`.

## Current Issue

When users ask about implementing custom functions, the server returns general functions documentation instead of the specific custom functions documentation. The server should specifically reference and fetch content from the custom functions documentation page.

## Solution Implementation

### Step 1: Update tools.py

Add the following function to `awslabs/amplify_gen2_mcp_server/tools.py`:

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

### Step 2: Update get_amplify_documentation Function

Modify the existing `get_amplify_documentation` function in `tools.py` to handle custom functions:

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
        
        # Handle general functions topic - include both general and custom functions
        if topic.lower() in ["functions", "function", "lambda"]:
            # Get general functions documentation
            doc_results = search_amplify_documentation("functions", limit=3)
            
            result = f"""
# Functions Documentation

## General Functions Overview
"""
            if doc_results:
                top_result = doc_results[0]
                content = fetch_raw_content(top_result['raw_url'])
                if content:
                    if len(content) > 2000:
                        content = content[:2000] + "\n\n... (content truncated)"
                    result += f"""
**Source:** {top_result['url']}

{content}

"""
            
            # Add custom functions documentation
            custom_functions_doc = get_custom_functions_documentation(framework)
            result += f"""
---

## Custom Functions

{custom_functions_doc}
"""
            return result
        
        # Original logic for other topics
        doc_results = search_amplify_documentation(topic, limit=5)

        if not doc_results:
            return f"No documentation found for topic: {topic}"

        # Get content from the most relevant result
        top_result = doc_results[0]
        content = fetch_raw_content(top_result['raw_url'])

        if content:
            # Truncate if too long
            if len(content) > 3000:
                content = content[:3000] + "\n\n... (content truncated)"

            result = f"""
# {topic.title()} Documentation

**Source:** {top_result['url']}

{content}

## Related Documentation

"""
            # Add other relevant results
            for result_item in doc_results[1:3]:
                result += f"- [{result_item['title']}]({result_item['url']})\n"
            
            return result

        return f"Could not fetch content for topic: {topic}"

    except Exception as e:
        logger.error(f"Error getting Amplify documentation for {topic}: {e}")
        return f"Error retrieving documentation: {str(e)}"
```

### Step 3: Update Search Relevance Scoring

In the `calculate_relevance_score_from_path` function, add boost for custom functions:

```python
def calculate_relevance_score_from_path(path: str, query: str) -> float:
    """Calculate relevance score for search results based on file path only."""
    score = 0.0
    path_lower = path.lower()
    query_lower = query.lower()

    # Higher score for exact matches in filename
    filename = path_lower.split('/')[-1]
    if query_lower in filename:
        score += 10.0

    # Score for matches in path components
    path_components = path_lower.split('/')
    for component in path_components:
        if query_lower in component:
            score += 5.0

    # Boost for Gen2 specific content
    if 'gen2' in path_lower or 'gen-2' in path_lower:
        score += 3.0

    # Boost for framework-specific content
    frameworks = ['react', 'vue', 'angular', 'nextjs', 'flutter']
    for framework in frameworks:
        if framework in path_lower:
            score += 2.0

    # Boost for core topics
    core_topics = ['auth', 'data', 'storage', 'function', 'api', 'deploy']
    for topic in core_topics:
        if topic in path_lower:
            score += 2.0

    # Boost for build-a-backend content (Gen2 specific)
    if 'build-a-backend' in path_lower:
        score += 4.0

    # ADD THIS: Boost for custom functions content
    if 'custom-functions' in path_lower or 'custom_functions' in path_lower:
        score += 5.0

    # Boost for pages directory (main content)
    if '/pages/' in path_lower:
        score += 1.0

    return score
```

### Step 4: Update Constants (Optional)

In `consts.py`, you can add custom functions to the topics list:

```python
# Common Amplify Gen2 topics for guidance
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

## Testing the Implementation

After making these changes, test with the following queries:

1. **Direct custom functions query:**
   ```
   get_amplify_gen2_guidance_tool("custom functions")
   ```

2. **General functions query (should include both general and custom):**
   ```
   get_amplify_gen2_guidance_tool("functions")
   ```

3. **Search query:**
   ```
   search_amplify_gen2_documentation_tool("custom functions")
   ```

## Expected Results

After implementation:

1. **Custom functions queries** will return the specific custom functions documentation from `https://docs.amplify.aws/nextjs/build-a-backend/functions/custom-functions/`

2. **General functions queries** will return both general functions overview AND custom functions documentation

3. **Search results** will have higher relevance scores for custom functions content

4. **Framework support** will work for nextjs, react, vue, angular with appropriate fallbacks

## Benefits

- ✅ **Accurate Documentation**: Users get the correct custom functions documentation
- ✅ **Framework-Specific**: Supports different frameworks with appropriate paths
- ✅ **Comprehensive**: Includes both general and custom functions information
- ✅ **Robust**: Multiple fallback paths ensure documentation is found
- ✅ **Enhanced Search**: Better relevance scoring for custom functions queries

## Files Modified

1. `awslabs/amplify_gen2_mcp_server/tools.py` - Main implementation
2. `awslabs/amplify_gen2_mcp_server/consts.py` - Optional constants update

## Verification

To verify the fix is working:

1. The server should return content that specifically mentions `defineFunction`
2. The official URL should point to the custom functions documentation
3. Code examples should show custom function implementation patterns
4. The response should include both resource definition and handler examples
