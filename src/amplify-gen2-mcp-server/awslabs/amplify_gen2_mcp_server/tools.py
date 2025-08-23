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

"""Tools for the AWS Amplify Gen2 MCP Server."""

import base64
import json
import logging
import os
import requests
from datetime import datetime, timedelta
from .consts import (
    DEFAULT_SEARCH_LIMIT,
    DOCUMENTATION_REPO,
    GITHUB_API_BASE,
    PROJECT_TEMPLATE_FILES,
    SAMPLE_REPOSITORIES,
)
from typing import Any, Dict, List, Optional

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False


logger = logging.getLogger(__name__)

def search_amplify_documentation(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> List[Dict]:
    """Search Amplify documentation by browsing the repository structure.

    Args:
        query: Search query string
        limit: Maximum number of results to return

    Returns:
        List of search results with file information and relevance
    """
    try:
        # Since GitHub Code Search API requires auth, we'll use a different approach
        # Get the repository tree and search through file paths and names
        search_results = []

        # Get the repository tree
        tree_url = f"{GITHUB_API_BASE}/repos/{DOCUMENTATION_REPO}/git/trees/main?recursive=1"

        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'AmplifyGen2MCPServer/1.0'
        }

        response = requests.get(tree_url, headers=headers, timeout=10)

        if response.status_code == 200:
            tree_data = response.json()

            # Filter for markdown files and calculate relevance
            for item in tree_data.get('tree', []):
                if item['type'] == 'blob' and item['path'].endswith(('.md', '.mdx')):
                    # Calculate relevance score based on path and filename
                    relevance_score = calculate_relevance_score_from_path(item['path'], query)

                    if relevance_score > 0:  # Only include relevant results
                        search_results.append({
                            'rank_order': len(search_results) + 1,
                            'url': f"https://github.com/{DOCUMENTATION_REPO}/blob/main/{item['path']}",
                            'raw_url': f"https://raw.githubusercontent.com/{DOCUMENTATION_REPO}/main/{item['path']}",
                            'title': extract_title_from_path(item['path']),
                            'path': item['path'],
                            'relevance_score': relevance_score,
                            'repository': DOCUMENTATION_REPO
                        })

            # Sort by relevance score
            search_results.sort(key=lambda x: x['relevance_score'], reverse=True)

            # Update rank order after sorting
            for i, result in enumerate(search_results):
                result['rank_order'] = i + 1

            return search_results[:limit]

        return []

    except Exception as e:
        logger.error(f"Error searching Amplify documentation: {e}")
        return []

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

    # Boost for pages directory (main content)
    if '/pages/' in path_lower:
        score += 1.0

    return score

def calculate_relevance_score(item: Dict, query: str) -> float:
    """Calculate relevance score for search results."""
    score = 0.0
    path = item['path'].lower()
    query_lower = query.lower()

    # Higher score for exact matches in filename
    filename = path.split('/')[-1]
    if query_lower in filename:
        score += 10.0

    # Score for matches in path components
    path_components = path.split('/')
    for component in path_components:
        if query_lower in component:
            score += 5.0

    # Boost for Gen2 specific content
    if 'gen2' in path or 'gen-2' in path:
        score += 3.0

    # Boost for framework-specific content
    frameworks = ['react', 'vue', 'angular', 'nextjs', 'flutter']
    for framework in frameworks:
        if framework in path:
            score += 2.0

    # Boost for core topics
    core_topics = ['auth', 'data', 'storage', 'function', 'api', 'deploy']
    for topic in core_topics:
        if topic in path:
            score += 2.0

    return score

def extract_title_from_path(path: str) -> str:
    """Extract a readable title from file path."""
    filename = path.split('/')[-1].replace('.md', '').replace('.mdx', '')

    # Convert kebab-case and snake_case to title case
    title = filename.replace('-', ' ').replace('_', ' ')
    title = ' '.join(word.capitalize() for word in title.split())

    # Add context from parent directories
    path_parts = path.split('/')[:-1]  # Exclude filename
    if len(path_parts) > 0:
        context = ' - '.join(part.replace('-', ' ').title() for part in path_parts[-2:])
        title = f"{title} ({context})"

    return title

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
        url = f"{GITHUB_API_BASE}/repos/{repo}/contents/{path}"
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

def discover_project_templates(framework: str = None) -> Dict[str, Any]:
    """Discover available project templates and their key files.

    Args:
        framework: Optional framework filter (react, vue, angular, next, ai)

    Returns:
        Dictionary with template information and available files
    """
    templates = {}

    # Determine which repositories to check
    repos_to_check = SAMPLE_REPOSITORIES.copy()
    if framework:
        framework_key = framework.lower()
        if framework_key == "nextjs":
            framework_key = "next"

        if framework_key in repos_to_check:
            repos_to_check = {framework_key: repos_to_check[framework_key]}

    for framework_name, repo in repos_to_check.items():
        template_info = {
            'framework': framework_name,
            'repository': repo,
            'github_url': f"https://github.com/{repo}",
            'available_files': {},
            'key_features': []
        }

        # Check for key project files
        for file_path, description in PROJECT_TEMPLATE_FILES.items():
            try:
                content = fetch_raw_content(f"https://raw.githubusercontent.com/{repo}/main/{file_path}")
                if content:
                    template_info['available_files'][file_path] = {
                        'description': description,
                        'size': len(content),
                        'url': f"https://raw.githubusercontent.com/{repo}/main/{file_path}",
                        'preview': content[:200] + "..." if len(content) > 200 else content
                    }

                    # Extract key features from package.json
                    if file_path == "package.json" and content:
                        try:
                            import json
                            pkg_data = json.loads(content)
                            if 'dependencies' in pkg_data:
                                deps = pkg_data['dependencies']
                                if '@aws-amplify/backend' in deps:
                                    template_info['key_features'].append('Amplify Gen2 Backend')
                                if '@aws-amplify/ui-react' in deps:
                                    template_info['key_features'].append('Amplify UI Components')
                                if 'next' in deps:
                                    template_info['key_features'].append('Next.js Framework')
                                if 'react' in deps:
                                    template_info['key_features'].append('React Framework')
                                if 'vue' in deps:
                                    template_info['key_features'].append('Vue Framework')
                                if '@angular/core' in deps:
                                    template_info['key_features'].append('Angular Framework')
                        except Exception:
                            pass

            except Exception as e:
                logger.debug(f"Could not fetch {file_path} from {repo}: {e}")
                continue

        templates[framework_name] = template_info

    return templates

def search_sample_repositories(query: str, framework: str = None) -> List[Dict]:
    """Search for code examples in sample repositories using direct file access.

    Args:
        query: Search query
        framework: Optional framework filter

    Returns:
        List of code examples from sample repositories
    """
    results = []

    # Get template information
    templates = discover_project_templates(framework)

    for framework_name, template_info in templates.items():
        repo = template_info['repository']

        # Search through available files for query matches
        for file_path, file_info in template_info['available_files'].items():
            # Check if query matches file path or content
            if (query.lower() in file_path.lower() or
                query.lower() in file_info.get('preview', '').lower()):

                relevance_score = calculate_relevance_score_from_path(file_path, query)

                # Boost score for template files
                if file_path in ['package.json', 'README.md', 'amplify/backend.ts']:
                    relevance_score += 5.0

                results.append({
                    'framework': framework_name,
                    'repository': repo,
                    'path': file_path,
                    'url': f"https://github.com/{repo}/blob/main/{file_path}",
                    'raw_url': f"https://raw.githubusercontent.com/{repo}/main/{file_path}",
                    'title': f"{framework_name.title()} - {extract_title_from_path(file_path)}",
                    'relevance_score': relevance_score,
                    'description': file_info['description'],
                    'size': file_info['size']
                })

    # Sort by relevance score
    results.sort(key=lambda x: x['relevance_score'], reverse=True)

    return results


def get_file_extension(file_path: str) -> str:
    """Get file extension for syntax highlighting."""
    ext = file_path.split('.')[-1].lower()
    extension_map = {
        'ts': 'typescript',
        'tsx': 'tsx',
        'js': 'javascript',
        'jsx': 'jsx',
        'vue': 'vue',
        'md': 'markdown',
        'json': 'json',
        'yml': 'yaml',
        'yaml': 'yaml'
    }
    return extension_map.get(ext, ext)




def get_amplify_documentation(topic: str, framework: str = "react") -> str:
    """Get comprehensive documentation for a specific Amplify topic.

    Args:
        topic: The topic to get documentation for
        framework: The framework context (default: react)

    Returns:
        Formatted documentation content
    """
    try:
        # Search for documentation related to the topic
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

            return f"""
# {topic.title()} Documentation

**Source:** {top_result['url']}

{content}

## Related Documentation

"""
            # Add other relevant results
            for result in doc_results[1:3]:
                return f"- [{result['title']}]({result['url']})\n"

        return f"Could not fetch content for topic: {topic}"

    except Exception as e:
        logger.error(f"Error getting Amplify documentation for {topic}: {e}")
        return f"Error retrieving documentation: {str(e)}"


def get_sample_code(feature: str, framework: str = "react") -> str:
    """Get sample code for a specific Amplify feature and framework.

    Args:
        feature: The Amplify feature to get code for
        framework: The framework to get code for

    Returns:
        Formatted sample code content
    """
    try:
        # Search for code examples in sample repositories
        sample_results = search_sample_repositories(feature, framework)

        if not sample_results:
            return f"No sample code found for {feature} in {framework}"

        result = f"""
## Sample Code Examples

**Feature:** {feature}
**Framework:** {framework.title()}

"""

        # Get content from the most relevant samples
        for i, sample in enumerate(sample_results[:3], 1):
            # Fetch the actual code content
            repo = sample['repository']
            path = sample['path']
            content = fetch_github_content(repo, path)

            if content:
                # Truncate if too long
                if len(content) > 1000:
                    content = content[:1000] + "\n\n... (code truncated)"

                result += f"""
### {i}. {sample.get('title', path.split('/')[-1])}

**Repository:** https://github.com/{repo}
**File:** {path}

```{get_file_extension(path)}
{content}
```

"""

        return result

    except Exception as e:
        logger.error(f"Error getting sample code for {feature}/{framework}: {e}")
        return f"Error retrieving sample code: {str(e)}"


def discover_amplify_project_templates(ctx: Any, framework: str = None) -> str:
    """Discover available Amplify Gen2 project templates and starter projects.

    Args:
        ctx: MCP context
        framework: Optional framework filter (react, vue, angular, next, ai)

    Returns:
        Comprehensive information about available project templates
    """
    logger.info(f"Discovering Amplify project templates for framework: {framework or 'all'}")

    try:
        templates = discover_project_templates(framework)

        if not templates:
            return "No project templates found."

        result = f"""
# Amplify Gen2 Project Templates

**Available Templates:** {len(templates)} framework{'s' if len(templates) != 1 else ''}

"""

        for framework_name, template_info in templates.items():
            result += f"""
## {framework_name.upper()} Template

**Repository:** [{template_info['repository']}]({template_info['github_url']})
**Key Features:** {', '.join(template_info['key_features']) if template_info['key_features'] else 'Standard Amplify Gen2 setup'}

### Available Files ({len(template_info['available_files'])})

"""

            # Group files by category
            config_files = []
            amplify_files = []
            source_files = []

            for file_path, file_info in template_info['available_files'].items():
                if file_path.startswith('amplify/'):
                    amplify_files.append((file_path, file_info))
                elif file_path in ['package.json', 'README.md']:
                    config_files.append((file_path, file_info))
                else:
                    source_files.append((file_path, file_info))

            # Display config files
            if config_files:
                result += "**Configuration Files:**\n"
                for file_path, file_info in config_files:
                    result += f"- `{file_path}` - {file_info['description']} ({file_info['size']} bytes)\n"
                result += "\n"

            # Display Amplify files
            if amplify_files:
                result += "**Amplify Backend Files:**\n"
                for file_path, file_info in amplify_files:
                    result += f"- `{file_path}` - {file_info['description']} ({file_info['size']} bytes)\n"
                result += "\n"

            # Display source files
            if source_files:
                result += "**Source Files:**\n"
                for file_path, file_info in source_files:
                    result += f"- `{file_path}` - {file_info['description']} ({file_info['size']} bytes)\n"
                result += "\n"

            result += f"""
### Quick Start

```bash
# Clone the template
git clone https://github.com/{template_info['repository']}.git my-amplify-app
cd my-amplify-app

# Install dependencies
npm install

# Deploy the backend
npx ampx sandbox

# Start development server
npm run dev
```

**Template URL:** {template_info['github_url']}

---

"""

        result += """
## Getting Started with Templates

1. **Choose a Framework:** Select the template that matches your preferred frontend framework
2. **Clone the Repository:** Use the git clone command above to get started
3. **Follow Setup Instructions:** Each template includes detailed README instructions
4. **Customize:** Modify the Amplify backend configuration in the `amplify/` directory

## Template Features Comparison

| Framework | Auth | Data/API | Storage | AI/ML | UI Components |
|-----------|------|----------|---------|-------|---------------|"""

        for framework_name, template_info in templates.items():
            features = template_info['key_features']
            auth = "✅" if any('auth' in f.lower() for f in features) else "📋"
            data = "✅" if any('backend' in f.lower() for f in features) else "📋"
            storage = "✅" if any('storage' in f.lower() for f in features) else "📋"
            ai = "✅" if framework_name == 'ai' else "📋"
            ui = "✅" if any('ui' in f.lower() for f in features) else "📋"

            result += f"\n| {framework_name.title()} | {auth} | {data} | {storage} | {ai} | {ui} |"

        result += """

**Legend:** ✅ = Included, 📋 = Available to add

## Next Steps

- **Explore Templates:** Visit the GitHub repositories to see the full code
- **Read Documentation:** Check each template's README for specific setup instructions
- **Get Help:** Use the troubleshooting tool if you encounter issues during setup

**Official Documentation:** https://docs.amplify.aws/
        """

        return result

    except Exception as e:
        logger.error(f"Error discovering project templates: {e}")
        return f"Error discovering project templates: {str(e)}"


def search_amplify_gen2_documentation(ctx: Any, query: str, limit: int = 10) -> str:
    """Search Amplify Gen2 documentation comprehensively.

    Args:
        ctx: MCP context
        query: Search query string
        limit: Maximum number of results to return

    Returns:
        Comprehensive search results from official documentation and samples
    """
    logger.info(f"Searching Amplify Gen2 documentation for: {query}")

    # Search official documentation
    doc_results = search_amplify_documentation(query, limit)

    # Search sample repositories
    sample_results = search_sample_repositories(query)

    # Format results
    result = f"""
# Amplify Gen2 Documentation Search Results

**Query:** {query}
**Found:** {len(doc_results)} documentation results, {len(sample_results)} code examples

## Official Documentation

"""

    if doc_results:
        for i, result_item in enumerate(doc_results[:limit], 1):
            result += f"""
### {i}. {result_item['title']}
**URL:** {result_item['url']}
**Path:** {result_item['path']}
**Relevance Score:** {result_item['relevance_score']:.1f}

"""
    else:
        result += "No documentation results found.\n\n"

    result += "## Code Examples\n\n"

    if sample_results:
        for i, sample in enumerate(sample_results[:5], 1):
            result += f"""
### {i}. {sample['title']}
**Framework:** {sample['framework'].title()}
**Repository:** https://github.com/{sample['repository']}
**File:** {sample['path']}
**URL:** {sample['url']}

"""
    else:
        result += "No code examples found.\n\n"

    result += """
## Next Steps

1. **Read Documentation:** Click on the documentation URLs above to read the full content
2. **Explore Code:** Visit the repository URLs to see complete implementation examples
3. **Get Content:** Use the read_amplify_documentation tool with specific URLs for full content

**Available Search Topics:**
- Authentication, authorization, sign-in, sign-up, MFA
- Data modeling, GraphQL, API, database, schema
- Storage, file upload, S3, media
- Functions, Lambda, serverless, API
- Deployment, hosting, CI/CD, environments
- AI, machine learning, Bedrock, generation
- Analytics, monitoring, logging
- Push notifications, real-time, subscriptions

**Available Frameworks:** React, Vue, Angular, Next.js, Flutter
    """

    return result

def read_amplify_documentation(ctx: Any, url: str, max_length: int = 5000) -> str:
    """Read specific Amplify documentation content.

    Args:
        ctx: MCP context
        url: URL to the documentation (GitHub or raw URL)
        max_length: Maximum length of content to return

    Returns:
        Full documentation content in markdown format
    """
    logger.info(f"Reading Amplify documentation from: {url}")

    try:
        # Handle different URL formats
        if "raw.githubusercontent.com" in url:
            content = fetch_raw_content(url)
        elif "github.com" in url and "/blob/" in url:
            # Convert GitHub blob URL to raw URL
            raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            content = fetch_raw_content(raw_url)
        else:
            # Try to extract repo and path from GitHub URL
            parts = url.split("/")
            if len(parts) >= 7 and "github.com" in url:
                repo = f"{parts[3]}/{parts[4]}"
                path = "/".join(parts[7:])  # Skip /blob/main/
                content = fetch_github_content(repo, path)
            else:
                return f"Error: Unable to parse URL format: {url}"

        if content:
            # Truncate if too long
            if len(content) > max_length:
                content = content[:max_length] + f"\n\n... (truncated, {len(content) - max_length} more characters available)"

            return f"""
# Amplify Documentation Content

**Source:** {url}

{content}

---
*Content from official AWS Amplify documentation repository*
            """
        else:
            return f"Error: Could not fetch content from {url}"

    except Exception as e:
        logger.error(f"Error reading documentation from {url}: {e}")
        return f"Error reading documentation: {str(e)}"

def get_amplify_gen2_guidance(ctx: Any, topic: str) -> str:
    """Provides guidance on Amplify Gen2 development using official documentation and samples.

    Args:
        ctx: MCP context
        topic: The topic to get guidance on

    Returns:
        Comprehensive guidance from official documentation and sample repositories
    """
    logger.info(f"Getting guidance on Amplify Gen2 topic: {topic}")

    # Fetch official documentation from GitHub docs repository
    documentation = get_amplify_documentation(topic, "react")

    # Get sample code from official repositories
    sample_code = get_sample_code(topic, "react")

    # Combine documentation with sample code
    result = f"""
{documentation}

{sample_code}

## Additional Resources

**Official Documentation:** https://docs.amplify.aws/react/build-a-backend/{topic}/
**Sample Repositories:**
- React Template: https://github.com/{SAMPLE_REPOSITORIES['react']}
- Next.js Template: https://github.com/{SAMPLE_REPOSITORIES['next']}
- Vue Template: https://github.com/{SAMPLE_REPOSITORIES['vue']}
- Angular Template: https://github.com/{SAMPLE_REPOSITORIES['angular']}

**Quick Start:**
```bash
npm create amplify@latest my-amplify-app
cd my-amplify-app
npx ampx sandbox
```
    """

    return result


def generate_amplify_gen2_code(ctx: Any, feature: str, framework: str) -> str:
    """Generates Amplify Gen2 code snippets and configurations using official samples.

    Args:
        ctx: MCP context
        feature: The Amplify feature to generate code for
        framework: The frontend framework to use (e.g., React, Vue)

    Returns:
        Generated code from official sample repositories and documentation
    """
    logger.info(f"Generating Amplify Gen2 code for feature: {feature} with framework: {framework}")

    # Get official documentation
    documentation = get_amplify_documentation(feature, framework.lower())

    # Get sample code from official repositories
    sample_code = get_sample_code(feature, framework.lower())

    # Combine documentation and sample code
    result = f"""
# Amplify Gen2 {feature.title()} Implementation for {framework.title()}

{documentation}

{sample_code}

## Implementation Steps

1. **Create New Amplify Project:**
   ```bash
   npm create amplify@latest my-{feature}-app
   cd my-{feature}-app
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

3. **Start Development Environment:**
   ```bash
   npx ampx sandbox
   ```

4. **Deploy to Production:**
   ```bash
   npx ampx deploy
   ```

## Additional Resources

**Framework-Specific Templates:**
- React: https://github.com/{SAMPLE_REPOSITORIES.get('react', 'aws-samples/amplify-vite-react-template')}
- Next.js: https://github.com/{SAMPLE_REPOSITORIES.get('next', 'aws-samples/amplify-next-template')}
- Vue: https://github.com/{SAMPLE_REPOSITORIES.get('vue', 'aws-samples/amplify-vue-template')}
- Angular: https://github.com/{SAMPLE_REPOSITORIES.get('angular', 'aws-samples/amplify-angular-template')}

**Official Documentation:** https://docs.amplify.aws/{framework.lower()}/build-a-backend/{feature}/
    """

    return result


def get_amplify_gen2_best_practices(ctx: Any, area: str) -> str:
    """Provides best practices for Amplify Gen2 development.

    Args:
        ctx: MCP context
        area: The area to get best practices for

    Returns:
        Best practices for the specified area
    """
    logger.info(f"Getting best practices for Amplify Gen2 area: {area}")

    # This is a placeholder implementation. Replace with actual implementation.
    best_practices = {
        "authentication": """
# Amplify Gen2 Authentication Best Practices

1. **Use Social Identity Providers**
   - Implement social login (Google, Facebook, Apple) for better user experience
   - Example:
     ```typescript
     export const auth = defineAuth({
       loginWith: {
         email: true,
         phone: false,
         externalProviders: {
           google: {
             clientId: process.env.GOOGLE_CLIENT_ID,
             scopes: ['profile', 'email', 'openid'],
           },
         },
       },
     });
     ```

2. **Implement Multi-Factor Authentication (MFA)**
   - Enable MFA for sensitive applications
   - Example:
     ```typescript
     export const auth = defineAuth({
       loginWith: {
         email: true,
       },
       multifactor: {
         mode: 'OPTIONAL', // or 'REQUIRED'
         sms: true,
         totp: true,
       },
     });
     ```

3. **Custom Authentication Flow**
   - Use custom authentication when you need specialized auth logic
   - Example:
     ```typescript
     async function handleCustomAuth() {
       try {
         const { nextStep } = await signIn({ username });

         if (nextStep.signInStep === 'CONFIRM_SIGN_IN_WITH_CUSTOM_CHALLENGE') {
           // Handle custom challenge
           await confirmSignIn({ challengeResponse: 'your-challenge-response' });
         }
       } catch (error) {
         console.error('Error during custom auth:', error);
       }
     }
     ```

4. **Secure User Attributes**
   - Only request necessary user attributes
   - Mark sensitive attributes as required only when necessary
   - Example:
     ```typescript
     export const auth = defineAuth({
       loginWith: {
         email: true,
       },
       userAttributes: {
         given_name: {
           required: true,
         },
         family_name: {
           required: true,
         },
         // Only request phone_number if absolutely necessary
         phone_number: {
           required: false,
           mutable: true,
         },
       },
     });
     ```

5. **Implement Proper Sign-Out**
   - Always sign out from all devices when handling sensitive data
   - Example:
     ```typescript
     await signOut({ global: true });
     ```
        """,
        "data_modeling": """
# Amplify Gen2 Data Modeling Best Practices

1. **Use Strong Typing**
   - Leverage TypeScript for type safety
   - Example:
     ```typescript
     import { a, defineData } from '@aws-amplify/backend';

     const schema = a.schema({
       Todo: a.model({
         id: a.id(),
         name: a.string().required(),
         priority: a.enum(['LOW', 'MEDIUM', 'HIGH']).required(),
       }),
     });
     ```

2. **Implement Proper Authorization**
   - Use fine-grained access controls
   - Example:
     ```typescript
     const schema = a.schema({
       Todo: a.model({
         id: a.id(),
         name: a.string().required(),
         ownerId: a.string().required(),
       }).authorization((allow) => [
         // Owner can do all operations
         allow.owner().to(['create', 'read', 'update', 'delete']),

         // Team members can read and update
         allow.groups(['TeamMembers']).to(['read', 'update']),

         // Everyone can read
         allow.public().to(['read']),
       ]),
     });
     ```

3. **Use Relationships Effectively**
   - Define clear relationships between models
   - Example:
     ```typescript
     const schema = a.schema({
       Project: a.model({
         id: a.id(),
         name: a.string().required(),
         // One-to-many relationship
         tasks: a.hasMany('Task'),
       }),

       Task: a.model({
         id: a.id(),
         title: a.string().required(),
         // Many-to-one relationship
         project: a.belongsTo('Project'),
         // Many-to-many relationship
         assignees: a.manyToMany('User'),
       }),

       User: a.model({
         id: a.id(),
         username: a.string().required(),
         // Many-to-many relationship
         assignedTasks: a.manyToMany('Task'),
       }),
     });
     ```

4. **Implement Data Validation**
   - Use schema validators to ensure data integrity
   - Example:
     ```typescript
     const schema = a.schema({
       User: a.model({
         id: a.id(),
         email: a.string().required().email(),
         age: a.integer().min(18).max(120),
         username: a.string().required().minLength(3).maxLength(20),
       }),
     });
     ```

5. **Use Indexes for Query Performance**
   - Add indexes for frequently queried fields
   - Example:
     ```typescript
     const schema = a.schema({
       Post: a.model({
         id: a.id(),
         title: a.string().required(),
         category: a.string().required(),
         createdAt: a.datetime().required(),
       }).addIndex('byCategory', {
         sortKey: 'createdAt',
         fields: ['category', 'createdAt'],
       }),
     });
     ```
        """,
        # Add more areas as needed
    }

    if area.lower() in best_practices:
        return best_practices[area.lower()]
    else:
        return f"Best practices for '{area}' are not available yet. Please try areas like 'authentication' or 'data_modeling'."


def troubleshoot_amplify_gen2(ctx: Any, issue: str) -> str:
    """Helps troubleshoot common Amplify Gen2 issues by referencing live documentation and providing solutions.

    Args:
        ctx: MCP context
        issue: The issue to troubleshoot

    Returns:
        Troubleshooting guidance for the specified issue
    """
    logger.info(f"Troubleshooting Amplify Gen2 issue: {issue}")

    # Map common issues to documentation topics
    issue_to_topic_map = {
        "deployment": "deployment",
        "deploy": "deployment",
        "build": "deployment",
        "auth": "authentication",
        "authentication": "authentication",
        "login": "authentication",
        "signin": "authentication",
        "data": "data",
        "graphql": "data",
        "api": "data",
        "storage": "storage",
        "file": "storage",
        "upload": "storage",
    }

    # Find relevant documentation topic
    relevant_topic = None
    for keyword, topic in issue_to_topic_map.items():
        if keyword in issue.lower():
            relevant_topic = topic
            break

    # Get official documentation if we found a relevant topic
    docs_reference = ""
    if relevant_topic:
        docs_reference = f"\n## Official Documentation\n{get_amplify_documentation(relevant_topic, 'react')}\n"

    # Comprehensive troubleshooting guides
    troubleshooting_guides = {
        "deployment": """
# Troubleshooting Amplify Gen2 Deployment Issues

## Common Deployment Problems and Solutions

### 1. Authentication/Credentials Issues
**Symptoms:** Permission denied, invalid credentials, or authentication errors during deployment

**Solutions:**
```bash
# Check your AWS credentials
aws sts get-caller-identity

# Configure AWS CLI if needed
aws configure

# Or use AWS SSO
aws sso login --profile your-profile

# Verify Amplify CLI authentication
npx ampx configure profile
```

### 2. CloudFormation Stack Failures
**Symptoms:** Stack creation/update failures, resource limit errors

**Solutions:**
```bash
# Check stack status
npx ampx status

# View detailed logs
npx ampx logs

# Clean up failed stacks
npx ampx delete

# Check AWS CloudFormation console for detailed error messages
```

### 3. Build Failures
**Symptoms:** Build process fails, dependency errors, TypeScript compilation errors

**Solutions:**
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for TypeScript errors
npx tsc --noEmit

# Validate your backend configuration
npx ampx validate

# Generate fresh client code
npx ampx generate graphql-client-code
```

### 4. Resource Naming Conflicts
**Symptoms:** Resources already exist errors, naming conflicts

**Solutions:**
- Use unique resource names in your backend configuration
- Check existing AWS resources in your account
- Consider using different AWS regions
- Delete conflicting resources if safe to do so

### 5. Environment Issues
**Symptoms:** Different behavior between local and deployed environments

**Solutions:**
```bash
# List available environments
npx ampx env list

# Switch environments
npx ampx env checkout <env-name>

# Create new environment
npx ampx env add <env-name>

# Deploy to specific environment
npx ampx deploy --env <env-name>
```
        """,

        "authentication": """
# Troubleshooting Amplify Gen2 Authentication Issues

## Common Authentication Problems and Solutions

### 1. Sign-In/Sign-Up Failures
**Symptoms:** Users cannot sign in, sign-up errors, validation failures

**Debug Steps:**
```typescript
import { signIn, signUp } from 'aws-amplify/auth';

// Add detailed error logging
async function debugSignIn(username: string, password: string) {
  try {
    const result = await signIn({ username, password });
    console.log('Sign-in successful:', result);
    return result;
  } catch (error) {
    console.error('Sign-in error:', {
      name: error.name,
      message: error.message,
      code: error.code,
      stack: error.stack
    });
    throw error;
  }
}
```

**Common Solutions:**
- Verify user exists and is confirmed in Cognito User Pool
- Check password requirements match your auth configuration
- Ensure email/username format is correct
- Verify user account is not locked or disabled

### 2. Token/Session Issues
**Symptoms:** Unexpected logouts, API authentication failures, token expiration

**Solutions:**
```typescript
import { fetchAuthSession, getCurrentUser } from 'aws-amplify/auth';

// Check current auth state
async function debugAuthState() {
  try {
    const user = await getCurrentUser();
    console.log('Current user:', user);

    const session = await fetchAuthSession();
    console.log('Session valid:', !!session.tokens);
    console.log('Access token expires:', session.tokens?.accessToken?.payload.exp);

    return { user, session };
  } catch (error) {
    console.error('Auth state error:', error);
    return null;
  }
}
```

### 3. Social Provider Issues
**Symptoms:** Social login fails, redirect problems, OAuth errors

**Solutions:**
- Verify OAuth configuration in AWS Cognito console
- Check callback URLs match your application URLs
- Ensure social provider app credentials are correct
- Test redirect URLs are accessible

### 4. MFA Problems
**Symptoms:** MFA not triggering, verification code issues

**Solutions:**
```typescript
import { signIn, confirmSignIn } from 'aws-amplify/auth';

async function handleMfaFlow(username: string, password: string) {
  try {
    const { nextStep } = await signIn({ username, password });

    console.log('Next step:', nextStep);

    if (nextStep.signInStep === 'CONFIRM_SIGN_IN_WITH_SMS_CODE') {
      // Handle SMS MFA
      const code = prompt('Enter SMS code:');
      await confirmSignIn({ confirmationCode: code });
    } else if (nextStep.signInStep === 'CONFIRM_SIGN_IN_WITH_TOTP_CODE') {
      // Handle TOTP MFA
      const code = prompt('Enter TOTP code:');
      await confirmSignIn({ confirmationCode: code });
    }
  } catch (error) {
    console.error('MFA error:', error);
  }
}
```

### 5. Configuration Issues
**Symptoms:** Auth not working after deployment, configuration errors

**Solutions:**
```bash
# Regenerate configuration
npx ampx generate

# Check amplify_outputs.json exists and is valid
cat amplify_outputs.json

# Verify Amplify.configure() is called before auth operations
```
        """,

        "data": """
# Troubleshooting Amplify Gen2 Data Issues

## Common Data/GraphQL Problems and Solutions

### 1. Schema Validation Errors
**Symptoms:** Schema deployment fails, GraphQL validation errors

**Solutions:**
```bash
# Validate schema before deployment
npx ampx validate

# Check for common schema issues:
# - Circular references in relationships
# - Invalid field types
# - Missing authorization rules
# - Incorrect enum values
```

**Example of fixing common schema issues:**
```typescript
// ❌ Problematic schema
const schema = a.schema({
  Post: a.model({
    title: a.string(),
    // Missing authorization
  }),
});

// ✅ Fixed schema
const schema = a.schema({
  Post: a.model({
    title: a.string().required(),
    content: a.string(),
  }).authorization((allow) => [
    allow.owner(),
    allow.public().to(['read'])
  ]),
});
```

### 2. Client Generation Issues
**Symptoms:** Generated client types are incorrect, compilation errors

**Solutions:**
```bash
# Regenerate client code
npx ampx generate graphql-client-code

# Clear generated files and regenerate
rm -rf src/graphql/
npx ampx generate graphql-client-code

# Check TypeScript compilation
npx tsc --noEmit
```

### 3. Authorization Errors
**Symptoms:** Access denied errors, unauthorized operations

**Debug Authorization:**
```typescript
import { generateClient } from 'aws-amplify/data';
import { getCurrentUser } from 'aws-amplify/auth';

const client = generateClient<Schema>();

async function debugDataAccess() {
  try {
    // Check current user
    const user = await getCurrentUser();
    console.log('Current user:', user);

    // Try data operation with error handling
    const result = await client.models.Todo.list();
    console.log('Data access successful:', result);
  } catch (error) {
    console.error('Data access error:', {
      name: error.name,
      message: error.message,
      errors: error.errors // GraphQL specific errors
    });
  }
}
```

### 4. Real-time Subscription Issues
**Symptoms:** Subscriptions not working, connection problems

**Solutions:**
```typescript
// Debug subscriptions
const subscription = client.models.Todo.onCreate().subscribe({
  next: (data) => console.log('Subscription data:', data),
  error: (error) => console.error('Subscription error:', error),
});

// Clean up subscriptions
useEffect(() => {
  return () => subscription.unsubscribe();
}, []);
```

### 5. Performance Issues
**Symptoms:** Slow queries, large response sizes

**Solutions:**
- Add appropriate indexes to your schema
- Use pagination for large datasets
- Implement proper filtering
- Consider using custom resolvers for complex queries

```typescript
// Use pagination
const { data: todos, nextToken } = await client.models.Todo.list({
  limit: 20,
  nextToken: previousNextToken
});

// Use filtering
const { data: completedTodos } = await client.models.Todo.list({
  filter: { completed: { eq: true } }
});
```
        """,

        "storage": """
# Troubleshooting Amplify Gen2 Storage Issues

## Common Storage Problems and Solutions

### 1. Upload Failures
**Symptoms:** File uploads fail, permission errors, size limit errors

**Debug Upload Issues:**
```typescript
import { uploadData } from 'aws-amplify/storage';

async function debugUpload(file: File) {
  try {
    console.log('Uploading file:', {
      name: file.name,
      size: file.size,
      type: file.type
    });

    const result = await uploadData({
      key: `uploads/${file.name}`,
      data: file,
      options: {
        contentType: file.type,
        onProgress: ({ transferredBytes, totalBytes }) => {
          console.log(`Upload progress: ${transferredBytes}/${totalBytes}`);
        }
      }
    }).result;

    console.log('Upload successful:', result);
    return result;
  } catch (error) {
    console.error('Upload error:', {
      name: error.name,
      message: error.message,
      code: error.code
    });
    throw error;
  }
}
```

### 2. Access Permission Issues
**Symptoms:** Access denied errors, unauthorized file operations

**Solutions:**
- Check your storage access rules configuration
- Verify user authentication status
- Ensure file paths match your access patterns

```typescript
// Example of proper access configuration
export const storage = defineStorage({
  name: 'myProjectFiles',
  access: (allow) => ({
    'public/*': [
      allow.authenticated.to(['read', 'write']),
      allow.guest.to(['read'])
    ],
    'private/{entity_id}/*': [
      allow.entity('identity').to(['read', 'write', 'delete'])
    ]
  })
});
```

### 3. Download/Access Issues
**Symptoms:** Cannot download files, broken URLs, access errors

**Debug Download Issues:**
```typescript
import { getUrl, downloadData } from 'aws-amplify/storage';

async function debugDownload(key: string) {
  try {
    // Get signed URL
    const linkToStorageFile = await getUrl({
      key,
      options: {
        accessLevel: 'protected', // or 'private', 'public'
        expiresIn: 3600 // 1 hour
      }
    });

    console.log('Download URL:', linkToStorageFile.url);

    // Or download data directly
    const downloadResult = await downloadData({ key }).result;
    console.log('Download successful:', downloadResult);

    return downloadResult;
  } catch (error) {
    console.error('Download error:', error);
    throw error;
  }
}
```

### 4. File Listing Issues
**Symptoms:** Cannot list files, empty results, permission errors

**Solutions:**
```typescript
import { list } from 'aws-amplify/storage';

async function debugList() {
  try {
    const result = await list({
      prefix: 'uploads/',
      options: {
        accessLevel: 'protected',
        pageSize: 100
      }
    });

    console.log('Files found:', result.items);
    return result;
  } catch (error) {
    console.error('List error:', error);
    throw error;
  }
}
```

### 5. Configuration Issues
**Symptoms:** Storage not working after deployment, configuration errors

**Solutions:**
```bash
# Regenerate configuration
npx ampx generate

# Check storage configuration in backend
cat amplify/storage/resource.ts

# Verify storage is included in backend definition
cat amplify/backend.ts
```
        """,
    }

    # Find the most relevant troubleshooting guide
    for key, guide in troubleshooting_guides.items():
        if key.lower() in issue.lower():
            return f"{guide}{docs_reference}"

    # If no specific match, provide general troubleshooting guidance
    return f"""
# General Amplify Gen2 Troubleshooting

## Issue: {issue}

### General Debugging Steps:

1. **Check System Status:**
   ```bash
   npx ampx status
   npx ampx logs
   ```

2. **Validate Configuration:**
   ```bash
   npx ampx validate
   ```

3. **Regenerate Client Code:**
   ```bash
   npx ampx generate graphql-client-code
   ```

4. **Check AWS Console:**
   - CloudFormation stacks
   - Cognito User Pools
   - AppSync APIs
   - S3 buckets

### Common Issue Categories:
- **deployment** - Build and deployment problems
- **authentication** - Sign-in, sign-up, and auth issues
- **data** - GraphQL, schema, and database issues
- **storage** - File upload, download, and access issues

### Getting Help:
- Visit: https://docs.amplify.aws/react/
- GitHub Issues: https://github.com/aws-amplify/amplify-js/issues
- Discord Community: https://discord.gg/amplify

{docs_reference}
    """


def get_amplify_lambda_help(ctx, topic: str = None) -> str:
    """Get comprehensive help for Amplify Gen2 Lambda function parameters and usage.

    Args:
        ctx: MCP context (unused but required for consistency)
        topic: Optional specific topic to focus on (e.g., "event", "context", "handler", "examples")

    Returns:
        Comprehensive Lambda function help documentation
    """
    
    base_help = """
# AWS Amplify Gen2 Lambda Functions - Parameter Guide

## Overview
Lambda functions in Amplify Gen2 are serverless functions that can be triggered by various events and integrated with your Amplify backend resources like data, authentication, and storage.

## Function Handler Signature

### Node.js/TypeScript Handler
```typescript
export const handler = async (event: any, context: any): Promise<any> => {
    // Your function logic here
    return {
        statusCode: 200,
        body: JSON.stringify({ message: 'Success' })
    };
};
```

### Python Handler
```python
def lambda_handler(event, context):
    # Your function logic here
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Success'})
    }
```

## Event Object Structure

The `event` parameter contains the input data for your Lambda function. The structure varies based on how the function is invoked:

### 1. Direct Invocation (Test Events)
```json
{
    "key1": "value1",
    "key2": "value2",
    "customData": {
        "nested": "object"
    }
}
```

### 2. API Gateway Integration
```json
{
    "httpMethod": "POST",
    "path": "/api/endpoint",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer token"
    },
    "body": "{\\"data\\": \\"value\\"}",
    "queryStringParameters": {
        "param1": "value1"
    },
    "pathParameters": {
        "id": "123"
    }
}
```

### 3. Cognito Triggers
```json
{
    "version": "1",
    "region": "us-east-1",
    "userPoolId": "us-east-1_XXXXXXXXX",
    "userName": "user@example.com",
    "request": {
        "userAttributes": {
            "email": "user@example.com",
            "email_verified": "true"
        }
    },
    "response": {}
}
```

### 4. S3 Events
```json
{
    "Records": [
        {
            "eventVersion": "2.1",
            "eventSource": "aws:s3",
            "eventName": "ObjectCreated:Put",
            "s3": {
                "bucket": {
                    "name": "my-bucket"
                },
                "object": {
                    "key": "uploads/file.jpg",
                    "size": 1024
                }
            }
        }
    ]
}
```

## Context Object Properties

The `context` parameter provides runtime information about the Lambda function execution:

```typescript
interface LambdaContext {
    // Function metadata
    functionName: string;           // Name of the Lambda function
    functionVersion: string;        // Version of the function
    invokedFunctionArn: string;     // ARN of the invoked function
    
    // Request metadata
    awsRequestId: string;           // Unique request ID
    logGroupName: string;           // CloudWatch log group
    logStreamName: string;          // CloudWatch log stream
    
    // Runtime information
    memoryLimitInMB: string;        // Memory allocated to function
    getRemainingTimeInMillis(): number; // Time remaining in execution
    
    // Client context (mobile apps)
    clientContext?: {
        client: {
            installation_id: string;
            app_title: string;
            app_version_name: string;
            app_version_code: string;
            app_package_name: string;
        };
        env: {
            platform_version: string;
            platform: string;
            make: string;
            model: string;
            locale: string;
        };
    };
    
    // Cognito identity (authenticated users)
    identity?: {
        cognitoIdentityId: string;
        cognitoIdentityPoolId: string;
    };
}
```

## Amplify Gen2 Function Definition

### Basic Function Definition
```typescript
// amplify/functions/my-function/resource.ts
import { defineFunction } from '@aws-amplify/backend';

export const myFunction = defineFunction({
    name: 'my-function',
    entry: './handler.ts'
});
```

### Function with Environment Variables
```typescript
// amplify/functions/my-function/resource.ts
import { defineFunction } from '@aws-amplify/backend';

export const myFunction = defineFunction({
    name: 'my-function',
    entry: './handler.ts',
    environment: {
        API_URL: 'https://api.example.com',
        DEBUG_MODE: 'true'
    }
});
```

### Function with Data Access
```typescript
// amplify/functions/data-access/resource.ts
import { defineFunction } from '@aws-amplify/backend';

export const dataAccessFunction = defineFunction({
    name: 'data-access',
    entry: './handler.ts'
});

// In amplify/data/resource.ts
import { dataAccessFunction } from '../functions/data-access/resource';

const schema = a.schema({
    Todo: a.model({
        content: a.string(),
        done: a.boolean()
    })
}).authorization(allow => [
    allow.resource(dataAccessFunction)
]);
```

## Common Function Patterns

### 1. Data Processing Function
```typescript
// amplify/functions/process-data/handler.ts
import type { Handler } from 'aws-lambda';
import { Amplify } from 'aws-amplify';
import { generateClient } from 'aws-amplify/data';
import { getAmplifyDataClientConfig } from '@aws-amplify/backend/function/runtime';
import type { Schema } from '../../data/resource';

const amplifyConfig = getAmplifyDataClientConfig();
Amplify.configure(amplifyConfig);
const client = generateClient<Schema>();

export const handler: Handler = async (event, context) => {
    console.log('Event:', JSON.stringify(event, null, 2));
    console.log('Context:', JSON.stringify(context, null, 2));
    
    try {
        // Process the data
        const result = await client.models.Todo.create({
            content: event.content,
            done: false
        });
        
        return {
            statusCode: 200,
            body: JSON.stringify({
                message: 'Data processed successfully',
                result: result.data
            })
        };
    } catch (error) {
        console.error('Error:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({
                message: 'Error processing data',
                error: error.message
            })
        };
    }
};
```

### 2. Authentication Trigger Function
```typescript
// amplify/functions/auth-trigger/handler.ts
import type { PreSignUpTriggerHandler } from 'aws-lambda';

export const handler: PreSignUpTriggerHandler = async (event, context) => {
    console.log('Pre-signup event:', JSON.stringify(event, null, 2));
    
    // Auto-confirm user
    event.response.autoConfirmUser = true;
    event.response.autoVerifyEmail = true;
    
    // Add custom attributes
    event.response.userAttributes = {
        ...event.request.userAttributes,
        'custom:role': 'user'
    };
    
    return event;
};
```

### 3. File Processing Function
```typescript
// amplify/functions/process-file/handler.ts
import type { S3Handler } from 'aws-lambda';
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';

const s3Client = new S3Client({});

export const handler: S3Handler = async (event, context) => {
    console.log('S3 event:', JSON.stringify(event, null, 2));
    
    for (const record of event.Records) {
        const bucket = record.s3.bucket.name;
        const key = record.s3.object.key;
        
        try {
            // Get the object from S3
            const command = new GetObjectCommand({
                Bucket: bucket,
                Key: key
            });
            
            const response = await s3Client.send(command);
            console.log(`Processed file: ${key} from bucket: ${bucket}`);
            
            // Process the file content here
            
        } catch (error) {
            console.error(`Error processing file ${key}:`, error);
        }
    }
    
    return { statusCode: 200 };
};
```

## Environment Variables Access

### Node.js/TypeScript
```typescript
export const handler = async (event, context) => {
    const apiUrl = process.env.API_URL;
    const debugMode = process.env.DEBUG_MODE === 'true';
    
    if (debugMode) {
        console.log('Debug mode enabled');
    }
    
    // Use environment variables
};
```

### Python
```python
import os

def lambda_handler(event, context):
    api_url = os.environ.get('API_URL')
    debug_mode = os.environ.get('DEBUG_MODE') == 'true'
    
    if debug_mode:
        print('Debug mode enabled')
    
    # Use environment variables
```

## Error Handling Best Practices

### Structured Error Responses
```typescript
export const handler = async (event, context) => {
    try {
        // Function logic
        return {
            statusCode: 200,
            body: JSON.stringify({ success: true, data: result })
        };
    } catch (error) {
        console.error('Function error:', error);
        
        return {
            statusCode: 500,
            body: JSON.stringify({
                success: false,
                error: {
                    message: error.message,
                    type: error.constructor.name,
                    requestId: context.awsRequestId
                }
            })
        };
    }
};
```

## Testing Lambda Functions

### Local Testing
```typescript
// test/handler.test.ts
import { handler } from '../amplify/functions/my-function/handler';

describe('Lambda Handler', () => {
    it('should process event correctly', async () => {
        const event = {
            key: 'test-value'
        };
        
        const context = {
            awsRequestId: 'test-request-id',
            functionName: 'test-function',
            getRemainingTimeInMillis: () => 30000
        };
        
        const result = await handler(event, context);
        expect(result.statusCode).toBe(200);
    });
});
```

## Common Event Sources and Their Parameters

### 1. API Gateway REST API
- `event.httpMethod`: HTTP method (GET, POST, etc.)
- `event.path`: Request path
- `event.headers`: Request headers
- `event.body`: Request body (string)
- `event.queryStringParameters`: Query parameters
- `event.pathParameters`: Path parameters

### 2. API Gateway HTTP API
- `event.version`: Event version
- `event.routeKey`: Route key
- `event.rawPath`: Raw path
- `event.headers`: Request headers
- `event.body`: Request body
- `event.queryStringParameters`: Query parameters

### 3. Cognito User Pool Triggers
- `event.userPoolId`: User pool ID
- `event.userName`: Username
- `event.request`: Request data
- `event.response`: Response data to modify

### 4. S3 Events
- `event.Records[].s3.bucket.name`: Bucket name
- `event.Records[].s3.object.key`: Object key
- `event.Records[].eventName`: Event type

### 5. DynamoDB Streams
- `event.Records[].dynamodb.Keys`: Item keys
- `event.Records[].dynamodb.NewImage`: New item data
- `event.Records[].dynamodb.OldImage`: Old item data
- `event.Records[].eventName`: Event type (INSERT, MODIFY, REMOVE)

## Debugging Tips

1. **Use console.log extensively**:
   ```typescript
   console.log('Event:', JSON.stringify(event, null, 2));
   console.log('Context:', JSON.stringify(context, null, 2));
   ```

2. **Check CloudWatch Logs**:
   - Function logs appear in CloudWatch
   - Use structured logging for better searchability

3. **Test with different event types**:
   - Create test events in Lambda console
   - Use AWS SAM for local testing

4. **Monitor function metrics**:
   - Duration, error rate, throttles
   - Memory usage and timeout issues

## Related Documentation
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Amplify Gen2 Functions](https://docs.amplify.aws/react/build-a-backend/functions/)
- [AWS Lambda Event Sources](https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html)
"""

    # Topic-specific help sections
    topic_specific = {
        "event": """
## Event Object Deep Dive

The event object structure depends on the trigger source:

### Custom Event Structure
When invoking directly or through custom triggers:
```json
{
    "customField": "value",
    "data": {
        "nested": "object"
    },
    "array": [1, 2, 3]
}
```

### API Gateway Event Structure
```json
{
    "resource": "/users/{id}",
    "path": "/users/123",
    "httpMethod": "GET",
    "headers": {
        "Accept": "application/json",
        "Authorization": "Bearer token"
    },
    "multiValueHeaders": {},
    "queryStringParameters": {
        "filter": "active"
    },
    "multiValueQueryStringParameters": {},
    "pathParameters": {
        "id": "123"
    },
    "stageVariables": null,
    "requestContext": {
        "requestId": "request-id",
        "stage": "prod",
        "resourceId": "resource-id",
        "httpMethod": "GET",
        "resourcePath": "/users/{id}",
        "path": "/prod/users/123",
        "accountId": "123456789012",
        "apiId": "api-id",
        "protocol": "HTTP/1.1",
        "requestTime": "09/Apr/2015:12:34:56 +0000",
        "requestTimeEpoch": 1428582896000,
        "identity": {
            "cognitoIdentityPoolId": null,
            "accountId": null,
            "cognitoIdentityId": null,
            "caller": null,
            "sourceIp": "127.0.0.1",
            "principalOrgId": null,
            "accessKey": null,
            "cognitoAuthenticationType": null,
            "cognitoAuthenticationProvider": null,
            "userArn": null,
            "userAgent": "Custom User Agent String",
            "user": null
        }
    },
    "body": "{\\"key\\": \\"value\\"}",
    "isBase64Encoded": false
}
```
        """,
        
        "context": """
## Context Object Deep Dive

The context object provides runtime information:

### Available Properties
```typescript
interface LambdaContext {
    // Function identification
    functionName: string;           // "my-amplify-function"
    functionVersion: string;        // "$LATEST" or version number
    invokedFunctionArn: string;     // Full ARN of the function
    
    // Request tracking
    awsRequestId: string;           // Unique ID for this invocation
    logGroupName: string;           // "/aws/lambda/my-function"
    logStreamName: string;          // "2023/01/01/[$LATEST]abcd1234"
    
    // Runtime limits
    memoryLimitInMB: string;        // "128", "256", etc.
    getRemainingTimeInMillis(): number; // Time left before timeout
    
    // Optional context (mobile/web apps)
    clientContext?: ClientContext;
    identity?: CognitoIdentity;
}
```

### Using Context for Monitoring
```typescript
export const handler = async (event, context) => {
    const startTime = Date.now();
    
    console.log(`Function: ${context.functionName}`);
    console.log(`Request ID: ${context.awsRequestId}`);
    console.log(`Memory limit: ${context.memoryLimitInMB}MB`);
    console.log(`Time remaining: ${context.getRemainingTimeInMillis()}ms`);
    
    // Your function logic
    
    const duration = Date.now() - startTime;
    console.log(`Execution duration: ${duration}ms`);
    
    return { statusCode: 200 };
};
```
        """,
        
        "handler": """
## Handler Function Patterns

### Basic Handler Structure
```typescript
export const handler = async (event: any, context: any): Promise<any> => {
    // Initialization (runs once per container)
    
    try {
        // Main logic
        const result = await processEvent(event);
        
        return {
            statusCode: 200,
            body: JSON.stringify(result)
        };
    } catch (error) {
        console.error('Handler error:', error);
        
        return {
            statusCode: 500,
            body: JSON.stringify({
                error: error.message,
                requestId: context.awsRequestId
            })
        };
    }
};
```

### Typed Handler (TypeScript)
```typescript
import type { APIGatewayProxyHandler, APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';

export const handler: APIGatewayProxyHandler = async (
    event: APIGatewayProxyEvent,
    context: Context
): Promise<APIGatewayProxyResult> => {
    // Type-safe handler implementation
    
    return {
        statusCode: 200,
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
            message: 'Success',
            requestId: context.awsRequestId
        })
    };
};
```

### Handler with Amplify Data Access
```typescript
import { Amplify } from 'aws-amplify';
import { generateClient } from 'aws-amplify/data';
import { getAmplifyDataClientConfig } from '@aws-amplify/backend/function/runtime';
import type { Schema } from '../../data/resource';

// Initialize Amplify (outside handler for reuse)
const amplifyConfig = getAmplifyDataClientConfig();
Amplify.configure(amplifyConfig);
const client = generateClient<Schema>();

export const handler = async (event, context) => {
    try {
        // Access Amplify data
        const todos = await client.models.Todo.list();
        
        return {
            statusCode: 200,
            body: JSON.stringify({
                todos: todos.data,
                count: todos.data.length
            })
        };
    } catch (error) {
        console.error('Data access error:', error);
        throw error;
    }
};
```
        """,
        
        "examples": """
## Complete Function Examples

### 1. User Registration Handler
```typescript
// amplify/functions/user-registration/handler.ts
import type { PostConfirmationTriggerHandler } from 'aws-lambda';
import { DynamoDBClient, PutItemCommand } from '@aws-sdk/client-dynamodb';

const dynamoClient = new DynamoDBClient({});

export const handler: PostConfirmationTriggerHandler = async (event, context) => {
    console.log('Post-confirmation event:', JSON.stringify(event, null, 2));
    
    try {
        // Create user profile in DynamoDB
        await dynamoClient.send(new PutItemCommand({
            TableName: process.env.USER_TABLE_NAME,
            Item: {
                userId: { S: event.request.userAttributes.sub },
                email: { S: event.request.userAttributes.email },
                createdAt: { S: new Date().toISOString() },
                status: { S: 'active' }
            }
        }));
        
        console.log(`User profile created for: ${event.request.userAttributes.email}`);
        
    } catch (error) {
        console.error('Error creating user profile:', error);
        // Don't throw - this would prevent user confirmation
    }
    
    return event;
};
```

### 2. File Processing Handler
```typescript
// amplify/functions/process-upload/handler.ts
import type { S3Handler } from 'aws-lambda';
import { S3Client, GetObjectCommand, PutObjectCommand } from '@aws-sdk/client-s3';
import sharp from 'sharp';

const s3Client = new S3Client({});

export const handler: S3Handler = async (event, context) => {
    console.log('S3 event:', JSON.stringify(event, null, 2));
    
    for (const record of event.Records) {
        const bucket = record.s3.bucket.name;
        const key = record.s3.object.key;
        
        // Skip if not an image
        if (!key.match(/\\.(jpg|jpeg|png|gif)$/i)) {
            continue;
        }
        
        try {
            // Get original image
            const getCommand = new GetObjectCommand({
                Bucket: bucket,
                Key: key
            });
            
            const response = await s3Client.send(getCommand);
            const imageBuffer = await response.Body?.transformToByteArray();
            
            if (!imageBuffer) {
                console.error(`No image data for ${key}`);
                continue;
            }
            
            // Create thumbnail
            const thumbnail = await sharp(Buffer.from(imageBuffer))
                .resize(200, 200, { fit: 'inside' })
                .jpeg({ quality: 80 })
                .toBuffer();
            
            // Save thumbnail
            const thumbnailKey = key.replace(/\\.[^.]+$/, '_thumb.jpg');
            
            await s3Client.send(new PutObjectCommand({
                Bucket: bucket,
                Key: thumbnailKey,
                Body: thumbnail,
                ContentType: 'image/jpeg'
            }));
            
            console.log(`Thumbnail created: ${thumbnailKey}`);
            
        } catch (error) {
            console.error(`Error processing ${key}:`, error);
        }
    }
    
    return { statusCode: 200 };
};
```

### 3. API Endpoint Handler
```typescript
// amplify/functions/api-handler/handler.ts
import type { APIGatewayProxyHandler } from 'aws-lambda';
import { Amplify } from 'aws-amplify';
import { generateClient } from 'aws-amplify/data';
import { getAmplifyDataClientConfig } from '@aws-amplify/backend/function/runtime';
import type { Schema } from '../../data/resource';

const amplifyConfig = getAmplifyDataClientConfig();
Amplify.configure(amplifyConfig);
const client = generateClient<Schema>();

export const handler: APIGatewayProxyHandler = async (event, context) => {
    console.log('API request:', JSON.stringify(event, null, 2));
    
    const { httpMethod, path, body, queryStringParameters } = event;
    
    try {
        switch (httpMethod) {
            case 'GET':
                if (path.includes('/todos')) {
                    const todos = await client.models.Todo.list({
                        limit: queryStringParameters?.limit ? 
                            parseInt(queryStringParameters.limit) : 10
                    });
                    
                    return {
                        statusCode: 200,
                        headers: {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        body: JSON.stringify({
                            todos: todos.data,
                            nextToken: todos.nextToken
                        })
                    };
                }
                break;
                
            case 'POST':
                if (path.includes('/todos')) {
                    const todoData = JSON.parse(body || '{}');
                    
                    const newTodo = await client.models.Todo.create({
                        content: todoData.content,
                        done: false
                    });
                    
                    return {
                        statusCode: 201,
                        headers: {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        body: JSON.stringify({
                            todo: newTodo.data
                        })
                    };
                }
                break;
                
            default:
                return {
                    statusCode: 405,
                    headers: {
                        'Access-Control-Allow-Origin': '*'
                    },
                    body: JSON.stringify({
                        error: 'Method not allowed'
                    })
                };
        }
        
        return {
            statusCode: 404,
            headers: {
                'Access-Control-Allow-Origin': '*'
            },
            body: JSON.stringify({
                error: 'Not found'
            })
        };
        
    } catch (error) {
        console.error('API handler error:', error);
        
        return {
            statusCode: 500,
            headers: {
                'Access-Control-Allow-Origin': '*'
            },
            body: JSON.stringify({
                error: 'Internal server error',
                requestId: context.awsRequestId
            })
        };
    }
};
```

### 4. Scheduled Function Handler
```typescript
// amplify/functions/scheduled-task/handler.ts
import type { ScheduledHandler } from 'aws-lambda';
import { SESClient, SendEmailCommand } from '@aws-sdk/client-ses';
import { Amplify } from 'aws-amplify';
import { generateClient } from 'aws-amplify/data';
import { getAmplifyDataClientConfig } from '@aws-amplify/backend/function/runtime';
import type { Schema } from '../../data/resource';

const sesClient = new SESClient({});
const amplifyConfig = getAmplifyDataClientConfig();
Amplify.configure(amplifyConfig);
const client = generateClient<Schema>();

export const handler: ScheduledHandler = async (event, context) => {
    console.log('Scheduled event:', JSON.stringify(event, null, 2));
    
    try {
        // Get pending notifications
        const notifications = await client.models.Notification.list({
            filter: {
                status: { eq: 'pending' },
                scheduledFor: { le: new Date().toISOString() }
            }
        });
        
        console.log(`Found ${notifications.data.length} pending notifications`);
        
        for (const notification of notifications.data) {
            try {
                // Send email
                await sesClient.send(new SendEmailCommand({
                    Source: process.env.FROM_EMAIL,
                    Destination: {
                        ToAddresses: [notification.email]
                    },
                    Message: {
                        Subject: {
                            Data: notification.subject
                        },
                        Body: {
                            Text: {
                                Data: notification.body
                            }
                        }
                    }
                }));
                
                // Update notification status
                await client.models.Notification.update({
                    id: notification.id,
                    status: 'sent',
                    sentAt: new Date().toISOString()
                });
                
                console.log(`Notification sent: ${notification.id}`);
                
            } catch (error) {
                console.error(`Failed to send notification ${notification.id}:`, error);
                
                // Mark as failed
                await client.models.Notification.update({
                    id: notification.id,
                    status: 'failed',
                    error: error.message
                });
            }
        }
        
        return {
            statusCode: 200,
            body: JSON.stringify({
                processed: notifications.data.length,
                timestamp: new Date().toISOString()
            })
        };
        
    } catch (error) {
        console.error('Scheduled task error:', error);
        throw error;
    }
};
```
        """
    }
    
    if topic and topic.lower() in topic_specific:
        return base_help + "\n\n" + topic_specific[topic.lower()]
    
    return base_help


def get_amplify_lambda_logs(ctx, function_name: str, hours: int = 1, region: str = None, profile: str = None) -> str:
    """Get Lambda function logs for Amplify Gen2 functions from CloudWatch.

    Args:
        ctx: MCP context (unused but required for consistency)
        function_name: Name of the Lambda function (can be partial name for search)
        hours: Number of hours to look back for logs (default: 1)
        region: AWS region (defaults to us-east-1 or AWS_DEFAULT_REGION)
        profile: AWS profile to use (defaults to default profile)

    Returns:
        Formatted log entries from CloudWatch Logs
    """
    
    if not BOTO3_AVAILABLE:
        return """
# Lambda Logs - boto3 Not Available

## Error
The boto3 library is not available. To use Lambda logs functionality, install boto3:

```bash
pip install boto3
```

## Alternative Methods

### 1. AWS CLI
```bash
# List log groups
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/"

# Get recent logs
aws logs filter-log-events --log-group-name "/aws/lambda/your-function-name" --start-time $(date -d '1 hour ago' +%s)000

# Follow logs in real-time
aws logs tail "/aws/lambda/your-function-name" --follow
```

### 2. AWS Console
1. Go to AWS Lambda console
2. Select your function
3. Click on "Monitor" tab
4. Click "View logs in CloudWatch"

### 3. Amplify CLI
```bash
# View function logs
npx ampx logs function <function-name>

# Follow logs
npx ampx logs function <function-name> --follow
```
        """
    
    try:
        # Set up AWS session
        session_kwargs = {}
        if profile:
            session_kwargs['profile_name'] = profile
        if region:
            session_kwargs['region_name'] = region
        elif os.environ.get('AWS_DEFAULT_REGION'):
            session_kwargs['region_name'] = os.environ.get('AWS_DEFAULT_REGION')
        else:
            session_kwargs['region_name'] = 'us-east-1'
        
        session = boto3.Session(**session_kwargs)
        logs_client = session.client('logs')
        lambda_client = session.client('lambda')
        
        # Calculate time range
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        start_timestamp = int(start_time.timestamp() * 1000)
        end_timestamp = int(end_time.timestamp() * 1000)
        
        # Find matching Lambda functions
        matching_functions = []
        try:
            paginator = lambda_client.get_paginator('list_functions')
            for page in paginator.paginate():
                for func in page['Functions']:
                    if function_name.lower() in func['FunctionName'].lower():
                        matching_functions.append({
                            'name': func['FunctionName'],
                            'arn': func['FunctionArn'],
                            'runtime': func['Runtime'],
                            'last_modified': func['LastModified']
                        })
        except ClientError as e:
            return f"""
# Lambda Logs - Error Listing Functions

## Error
Failed to list Lambda functions: {str(e)}

## Possible Solutions
1. Check AWS credentials are configured
2. Verify IAM permissions for Lambda:ListFunctions
3. Ensure correct region is specified
4. Check if the AWS profile is valid

## Required IAM Permissions
```json
{{
    "Version": "2012-10-17",
    "Statement": [
        {{
            "Effect": "Allow",
            "Action": [
                "lambda:ListFunctions",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:FilterLogEvents"
            ],
            "Resource": "*"
        }}
    ]
}}
```
            """
        
        if not matching_functions:
            return f"""
# Lambda Logs - No Functions Found

## Search Results
No Lambda functions found matching: **{function_name}**

## Suggestions
1. Check the function name spelling
2. Verify the function exists in region: **{session_kwargs.get('region_name', 'us-east-1')}**
3. Try a partial name search
4. List all functions to see available options

## List All Functions
Use the AWS CLI to see all functions:
```bash
aws lambda list-functions --region {session_kwargs.get('region_name', 'us-east-1')}
```

## Common Amplify Function Naming Patterns
- `amplify-<app-name>-<env>-<function-name>-<hash>`
- Functions often have long generated names in Amplify
            """
        
        # Get logs for each matching function
        results = []
        
        for func in matching_functions[:5]:  # Limit to first 5 matches
            func_name = func['name']
            log_group_name = f"/aws/lambda/{func_name}"
            
            try:
                # Check if log group exists
                logs_client.describe_log_groups(logGroupNamePrefix=log_group_name)
                
                # Get log events
                response = logs_client.filter_log_events(
                    logGroupName=log_group_name,
                    startTime=start_timestamp,
                    endTime=end_timestamp,
                    limit=100  # Limit to recent 100 events per function
                )
                
                events = response.get('events', [])
                
                if events:
                    results.append({
                        'function': func,
                        'events': events,
                        'log_group': log_group_name
                    })
                else:
                    results.append({
                        'function': func,
                        'events': [],
                        'log_group': log_group_name,
                        'no_events': True
                    })
                    
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    results.append({
                        'function': func,
                        'events': [],
                        'log_group': log_group_name,
                        'error': 'Log group not found (function may not have been invoked yet)'
                    })
                else:
                    results.append({
                        'function': func,
                        'events': [],
                        'log_group': log_group_name,
                        'error': str(e)
                    })
        
        # Format results
        output = f"""
# Lambda Logs for "{function_name}"

**Time Range:** {start_time.strftime('%Y-%m-%d %H:%M:%S')} - {end_time.strftime('%Y-%m-%d %H:%M:%S')} UTC
**Region:** {session_kwargs.get('region_name', 'us-east-1')}
**Profile:** {profile or 'default'}

"""
        
        for result in results:
            func = result['function']
            events = result.get('events', [])
            log_group = result['log_group']
            
            output += f"""
## Function: {func['name']}

**Details:**
- **ARN:** {func['arn']}
- **Runtime:** {func['runtime']}
- **Last Modified:** {func['last_modified']}
- **Log Group:** {log_group}

"""
            
            if result.get('error'):
                output += f"""
**Error:** {result['error']}

"""
            elif result.get('no_events'):
                output += f"""
**No log events found** in the last {hours} hour(s).

**Possible reasons:**
- Function hasn't been invoked recently
- Function completed without logging
- Logs may be in a different time range

**To get more logs:**
```bash
aws logs filter-log-events --log-group-name "{log_group}" --start-time $(date -d '24 hours ago' +%s)000
```

"""
            else:
                output += f"""
**Log Events ({len(events)} entries):**

"""
                for event in events[-20:]:  # Show last 20 events
                    timestamp = datetime.fromtimestamp(event['timestamp'] / 1000)
                    message = event['message'].strip()
                    
                    # Format different types of log messages
                    if message.startswith('START RequestId:'):
                        output += f"🟢 **{timestamp.strftime('%H:%M:%S')}** - {message}\n"
                    elif message.startswith('END RequestId:'):
                        output += f"🔴 **{timestamp.strftime('%H:%M:%S')}** - {message}\n"
                    elif message.startswith('REPORT RequestId:'):
                        output += f"📊 **{timestamp.strftime('%H:%M:%S')}** - {message}\n"
                    elif 'ERROR' in message.upper() or 'Exception' in message:
                        output += f"❌ **{timestamp.strftime('%H:%M:%S')}** - {message}\n"
                    elif 'WARN' in message.upper():
                        output += f"⚠️ **{timestamp.strftime('%H:%M:%S')}** - {message}\n"
                    else:
                        output += f"ℹ️ **{timestamp.strftime('%H:%M:%S')}** - {message}\n"
                
                output += "\n"
        
        # Add helpful commands
        output += f"""
## Useful Commands

### Get More Logs
```bash
# Get logs for specific function
aws logs filter-log-events --log-group-name "/aws/lambda/{matching_functions[0]['name']}" --start-time $(date -d '24 hours ago' +%s)000

# Follow logs in real-time
aws logs tail "/aws/lambda/{matching_functions[0]['name']}" --follow

# Get logs with specific filter
aws logs filter-log-events --log-group-name "/aws/lambda/{matching_functions[0]['name']}" --filter-pattern "ERROR"
```

### Amplify CLI Commands
```bash
# View function logs
npx ampx logs function {function_name}

# Follow function logs
npx ampx logs function {function_name} --follow
```

### CloudWatch Console
[View in CloudWatch Console](https://console.aws.amazon.com/cloudwatch/home?region={session_kwargs.get('region_name', 'us-east-1')}#logsV2:log-groups/log-group/$252Faws$252Flambda$252F{matching_functions[0]['name'].replace('/', '$252F') if matching_functions else 'function-name'})

## Troubleshooting

### No Logs Appearing
1. **Function not invoked**: Trigger the function to generate logs
2. **Permissions**: Ensure Lambda has CloudWatch Logs permissions
3. **Time range**: Try expanding the time range
4. **Region**: Verify you're looking in the correct region

### Common Log Patterns
- **Cold starts**: Look for "START RequestId" without recent activity
- **Timeouts**: Check for missing "END RequestId" messages
- **Memory issues**: Look for "Process exited before completing request"
- **Errors**: Search for "ERROR", "Exception", or error stack traces
        """
        
        return output
        
    except NoCredentialsError:
        return """
# Lambda Logs - AWS Credentials Not Found

## Error
AWS credentials are not configured.

## Setup AWS Credentials

### Option 1: AWS CLI
```bash
aws configure
```

### Option 2: Environment Variables
```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_DEFAULT_REGION=us-east-1
```

### Option 3: AWS Profile
```bash
aws configure --profile your-profile-name
```

### Option 4: IAM Role (EC2/Lambda)
If running on AWS infrastructure, ensure the IAM role has the required permissions.

## Required IAM Permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:ListFunctions",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:FilterLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```
        """
    
    except Exception as e:
        return f"""
# Lambda Logs - Unexpected Error

## Error
{str(e)}

## Troubleshooting Steps
1. Check AWS credentials and permissions
2. Verify the region is correct
3. Ensure the function name exists
4. Check network connectivity to AWS

## Manual Alternatives
```bash
# List all Lambda functions
aws lambda list-functions

# Get logs directly
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/"
aws logs filter-log-events --log-group-name "/aws/lambda/your-function-name"
```
        """
