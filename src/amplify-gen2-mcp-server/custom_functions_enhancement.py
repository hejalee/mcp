"""
Enhancement for Amplify Gen2 MCP Server to properly handle custom functions documentation.

This file contains the updated functions that should be integrated into tools.py
to properly reference https://docs.amplify.aws/nextjs/build-a-backend/functions/custom-functions/
"""

import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)

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
        content = fetch_github_content("aws-amplify/docs", custom_functions_path)
        
        if not content:
            # Fallback paths for different frameworks
            fallback_paths = [
                f"src/pages/{framework}/build-a-backend/functions/custom-functions.mdx",
                f"src/pages/gen2/{framework}/build-a-backend/functions/custom-functions/index.mdx",
                "src/pages/nextjs/build-a-backend/functions/custom-functions/index.mdx"  # Default fallback
            ]
            
            for fallback_path in fallback_paths:
                content = fetch_github_content("aws-amplify/docs", fallback_path)
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


def fetch_github_content(repo: str, path: str, branch: str = "main") -> Optional[str]:
    """Fetch content from a GitHub repository file.

    Args:
        repo: Repository in format "owner/repo"
        path: Path to the file in the repository
        branch: Branch name (default: "main")

    Returns:
        File content as string, or None if not found
    """
    try:
        import base64
        
        url = f"https://api.github.com/repos/{repo}/contents/{path}"
        params = {"ref": branch}

        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'AmplifyGen2MCPServer/1.0'
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            content_data = response.json()
            if content_data.get('encoding') == 'base64':
                content = base64.b64decode(content_data['content']).decode('utf-8')
                return content

        return None

    except Exception as e:
        logger.error(f"Error fetching GitHub content from {repo}/{path}: {e}")
        return None


def enhanced_get_amplify_documentation(topic: str, framework: str = "react") -> str:
    """Enhanced version of get_amplify_documentation that properly handles custom functions.

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


def fetch_raw_content(raw_url: str) -> Optional[str]:
    """Fetch content from a raw GitHub URL.

    Args:
        raw_url: Raw GitHub URL

    Returns:
        File content as string, or None if not found
    """
    try:
        headers = {
            'User-Agent': 'AmplifyGen2MCPServer/1.0'
        }

        response = requests.get(raw_url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.text

        return None

    except Exception as e:
        logger.error(f"Error fetching raw content from {raw_url}: {e}")
        return None


def search_amplify_documentation(query: str, limit: int = 10):
    """Placeholder for the existing search function - this would be imported from the original tools.py"""
    # This function exists in the original tools.py file
    pass
