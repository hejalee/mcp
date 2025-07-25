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
import logging
import requests
from .consts import (
    DEFAULT_SEARCH_LIMIT,
    DOCUMENTATION_REPO,
    GITHUB_API_BASE,
    PROJECT_TEMPLATE_FILES,
    SAMPLE_REPOSITORIES,
)
from typing import Any, Dict, List, Optional


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
