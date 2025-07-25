# AWS Amplify Gen2 MCP Server

Model Context Protocol (MCP) server for comprehensive AWS Amplify Gen2 development assistance.

This MCP server provides intelligent search and guidance tools for AWS Amplify Gen2 development, with direct access to official documentation and sample code repositories.

## Features

- **🔍 Comprehensive Documentation Search**: Search across all Amplify Gen2 documentation with intelligent relevance ranking
- **📖 Documentation Reader**: Fetch and read specific documentation content in markdown format
- **💡 Expert Guidance**: Get prescriptive advice for building applications with Amplify Gen2
- **⚡ Code Generation**: Generate framework-specific code snippets from official templates
- **🛠️ Best Practices**: Access curated best practices for Amplify Gen2 development
- **🔧 Troubleshooting**: Get comprehensive troubleshooting guidance for common issues

## Data Sources

### Official Documentation
- **Primary Source**: [aws-amplify/docs](https://github.com/aws-amplify/docs) repository
- **Live Documentation**: [docs.amplify.aws](https://docs.amplify.aws/)

### Sample Code Repositories
- **React**: [amplify-vite-react-template](https://github.com/aws-samples/amplify-vite-react-template)
- **Next.js**: [amplify-next-template](https://github.com/aws-samples/amplify-next-template)
- **Vue**: [amplify-vue-template](https://github.com/aws-samples/amplify-vue-template)
- **Angular**: [amplify-angular-template](https://github.com/aws-samples/amplify-angular-template)
- **AI Examples**: [amplify-ai-examples](https://github.com/aws-samples/amplify-ai-examples)

## Prerequisites

### Installation Requirements

1. Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/) or the [GitHub README](https://github.com/astral-sh/uv#installation)
2. Install Python 3.10 or newer using `uv python install 3.10` (or a more recent version)

## Installation

| Cursor | VS Code |
|:------:|:-------:|
| [![Install MCP Server](https://cursor.com/deeplink/mcp-install-light.svg)](https://cursor.com/install-mcp?name=awslabs.amplify-gen2-mcp-server&config=eyJjb21tYW5kIjoidXZ4IGF3c2xhYnMuYW1wbGlmeS1nZW4yLW1jcC1zZXJ2ZXJABGF0ZXN0IiwiZW52Ijp7IkZBU1RNQ1BfTE9HX0xFVkVMIjoiRVJST1IifSwiZGlzYWJsZWQiOmZhbHNlLCJhdXRvQXBwcm92ZSI6W119) | [![Install on VS Code](https://img.shields.io/badge/Install_on-VS_Code-FF9900?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=AWS%20Amplify%20Gen2%20MCP%20Server&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22awslabs.amplify-gen2-mcp-server%40latest%22%5D%2C%22env%22%3A%7B%22FASTMCP_LOG_LEVEL%22%3A%22ERROR%22%7D%2C%22disabled%22%3Afalse%2C%22autoApprove%22%3A%5B%5D%7D) |

### Option 1: From Git Repository (Recommended)

```bash
# Clone the repository
git clone <repository-url> amplify-gen2-mcp-server
cd amplify-gen2-mcp-server

# Run the installation script
./install.sh
```

### Option 2: Direct Installation

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the package
uv pip install -e .
```

### Option 3: From PyPI (when published)

```bash
uvx awslabs.amplify-gen2-mcp-server@latest
```

## Configuration

Configure the MCP server in your MCP client configuration (e.g., for Amazon Q Developer CLI, edit `~/.aws/amazonq/mcp.json`):

### Local Development Configuration

```json
{
  "mcpServers": {
    "awslabs.amplify-gen2-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/amplify-gen2-mcp-server",
        "python",
        "-m",
        "awslabs.amplify_gen2_mcp_server.server"
      ],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### GitHub Installation Configuration

```json
{
  "mcpServers": {
    "awslabs.amplify-gen2-mcp-server": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/YOUR_USERNAME/amplify-gen2-mcp-server.git",
        "awslabs.amplify-gen2-mcp-server"
      ],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Docker Configuration

```json
{
  "mcpServers": {
    "awslabs.amplify-gen2-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.amplify-gen2-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

or docker after a successful `docker build -t mcp/amplify-gen2 .`:

```json
{
  "mcpServers": {
    "awslabs.amplify-gen2-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "--interactive",
        "--env",
        "FASTMCP_LOG_LEVEL=ERROR",
        "mcp/amplify-gen2:latest"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## Usage Examples

### Comprehensive Search
- "Search for authentication setup with social providers"
- "Find documentation about data modeling relationships"
- "Show me storage configuration examples"
- "Search for deployment troubleshooting guides"

### Specific Guidance
- "How do I set up authentication with MFA in Amplify Gen2?"
- "What are the best practices for data modeling?"
- "Generate React code for file upload functionality"
- "Help me troubleshoot deployment failures"

### Framework-Specific Development
- "Generate Next.js authentication code"
- "Show Vue.js data fetching examples"
- "Angular storage implementation guide"
- "React AI integration examples"

## Tools

### search_amplify_gen2_documentation

Comprehensively search Amplify Gen2 documentation and sample repositories.

```python
search_amplify_gen2_documentation(query: str, limit: int = 10) -> str
```

**Features:**
- Searches official documentation repository
- Includes sample code from all framework templates
- Intelligent relevance scoring
- Framework and topic-aware results

### read_amplify_documentation

Read specific Amplify documentation content from URLs.

```python
read_amplify_documentation(url: str, max_length: int = 5000) -> str
```

**Features:**
- Supports GitHub and raw URLs
- Returns clean markdown content
- Configurable content length
- Error handling for invalid URLs

### get_amplify_gen2_guidance

Get comprehensive guidance on Amplify Gen2 development topics.

```python
get_amplify_gen2_guidance(topic: str) -> str
```

**Enhanced Features:**
- Combines official documentation with sample code
- Framework-agnostic guidance
- Real-world implementation examples
- Links to relevant resources

### generate_amplify_gen2_code

Generate framework-specific code snippets and configurations.

```python
generate_amplify_gen2_code(feature: str, framework: str) -> str
```

**Enhanced Features:**
- Uses official sample repositories
- Framework-specific implementations
- Complete setup instructions
- Best practice patterns

### get_amplify_gen2_best_practices

Get curated best practices for Amplify Gen2 development.

```python
get_amplify_gen2_best_practices(area: str) -> str
```

### troubleshoot_amplify_gen2

Get comprehensive troubleshooting guidance for common issues.

```python
troubleshoot_amplify_gen2(issue: str) -> str
```

**Enhanced Features:**
- Links to official documentation
- Step-by-step debugging guides
- Common solution patterns
- Prevention strategies

### discover_amplify_project_templates

Discover available Amplify Gen2 project templates and starter projects.

```python
discover_amplify_project_templates(framework: str = None) -> str
```

**Features:**
- Comprehensive project template discovery
- Framework-specific filtering (react, vue, angular, next, ai)
- Detailed file analysis and feature detection
- Quick start instructions for each template
- Feature comparison table
- Direct links to all AWS sample repositories

## Search Capabilities

The server can intelligently search for content related to:

### Core Topics
- **Authentication**: Sign-in, sign-up, social providers, MFA, custom auth flows
- **Data**: GraphQL, schema design, relationships, authorization, real-time subscriptions
- **Storage**: File upload, S3 integration, access patterns, media handling
- **Functions**: Lambda functions, API routes, serverless patterns
- **AI/ML**: Bedrock integration, content generation, chat applications
- **Analytics**: Event tracking, monitoring, user behavior
- **Deployment**: CI/CD, environments, hosting, domain configuration

### Framework Support
- **React**: Hooks, components, state management
- **Next.js**: SSR, API routes, app router
- **Vue**: Composition API, reactivity, components
- **Angular**: Services, modules, dependency injection
- **Flutter**: Widgets, state management, platform integration

### Development Lifecycle
- **Getting Started**: Project setup, initial configuration
- **Development**: Local development, testing, debugging
- **Deployment**: Production deployment, environment management
- **Monitoring**: Logging, analytics, performance optimization

## Advanced Features

### Intelligent Relevance Scoring
- Prioritizes Gen2-specific content
- Boosts framework-relevant results
- Considers file path and naming patterns
- Ranks by topic relevance

### Multi-Source Integration
- Official documentation repository
- Multiple sample code repositories
- Live documentation links
- Community best practices

### Content Formatting
- Clean markdown output
- Syntax-highlighted code blocks
- Structured information hierarchy
- Actionable next steps

## Contributing

This MCP server is designed to provide the most current and accurate Amplify Gen2 information by directly accessing official AWS sources. All content is sourced from:

- Official AWS Amplify documentation
- AWS-maintained sample repositories
- Community-validated best practices

For issues or feature requests, please refer to the official AWS Amplify channels and documentation.
