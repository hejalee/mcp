# Cloudscape MCP Server

An AWS Labs Model Context Protocol (MCP) server that provides access to Cloudscape Design System documentation and demo code examples. This server enables AI assistants to search through official Cloudscape documentation and analyze real-world implementation patterns from the demos repository.

## Features

### Documentation Search
- **Search Documentation**: Find relevant content across Cloudscape Design System docs
- **Component Details**: Get comprehensive information about specific Cloudscape components
- **Design Tokens**: Access Cloudscape design tokens for colors, spacing, typography, and more

### Demo Code Analysis
- **Search Demos**: Find code examples in the Cloudscape demos repository
- **Implementation Details**: Get full implementation code for specific demos
- **Pattern Analysis**: Analyze common patterns and best practices across demos

## Installation

### Using uvx (recommended)
```bash
uvx awslabs.cloudscape-mcp-server@latest
```

### Using pip
```bash
pip install awslabs.cloudscape-mcp-server
```

## Configuration

### Amazon Q Developer CLI

Add to your `~/.aws/amazonq/mcp.json`:

```json
{
  "mcpServers": {
    "awslabs.cloudscape-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.cloudscape-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

### Cline

Add to your `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "awslabs.cloudscape-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.cloudscape-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

### Cursor

Add to your `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "awslabs.cloudscape-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.cloudscape-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

## Available Tools

### Documentation Tools

#### `search_cloudscape_docs`
Search Cloudscape Design System documentation for relevant content.

**Parameters:**
- `query` (string, required): Search query for documentation
- `max_results` (integer, optional): Maximum number of results to return (default: 10)

**Example:**
```
Search for "button component accessibility" in Cloudscape documentation
```

#### `get_cloudscape_component_docs`
Get detailed documentation for a specific Cloudscape component.

**Parameters:**
- `component_name` (string, required): Name of the Cloudscape component (e.g., 'button', 'table', 'form')

**Example:**
```
Get documentation for the "table" component
```

#### `get_cloudscape_design_tokens`
Get Cloudscape design tokens for colors, spacing, typography, etc.

**Parameters:**
- `category` (string, optional): Category filter (e.g., 'color', 'spacing', 'typography')

**Example:**
```
Get all color design tokens
```

### Demo Repository Tools

#### `search_cloudscape_demos`
Search through Cloudscape demos repository for code examples.

**Parameters:**
- `query` (string, required): Search query for demo code
- `max_results` (integer, optional): Maximum number of results to return (default: 10)

**Example:**
```
Search for "data table with pagination" examples in demos
```

#### `get_demo_implementation`
Get implementation details for a specific demo.

**Parameters:**
- `demo_name` (string, required): Name of the demo to retrieve

**Example:**
```
Get implementation for "dashboard" demo
```

#### `analyze_demo_patterns`
Analyze common patterns in Cloudscape demo implementations.

**Parameters:**
- `component_name` (string, optional): Component name to filter patterns

**Example:**
```
Analyze patterns for "form" components across all demos
```

## Usage Examples

### Finding Component Documentation
```
Using the Cloudscape MCP server, search for documentation about the Button component and show me its available props and usage examples.
```

### Analyzing Demo Code
```
Search the Cloudscape demos for examples of data tables with filtering and sorting functionality.
```

### Getting Design Tokens
```
Get all the color design tokens from Cloudscape so I can use them in my custom CSS.
```

### Pattern Analysis
```
Analyze common patterns for form validation in the Cloudscape demos repository.
```

## How It Works

The Cloudscape MCP Server provides two main capabilities:

1. **Documentation Search**: Crawls and searches the official Cloudscape Design System website (https://cloudscape.design) to find relevant documentation, component details, and design tokens.

2. **Demo Repository Analysis**: Clones and analyzes the Cloudscape demos repository (https://github.com/cloudscape-design/demos) to provide real-world code examples and implementation patterns.

## Development

### Prerequisites
- Python 3.10+
- uv (recommended) or pip

### Setup
```bash
git clone https://github.com/awslabs/mcp.git
cd mcp/src/cloudscape-mcp-server
uv venv && uv sync --all-groups
```

### Testing
```bash
uv run pytest
```

### Running Locally
```bash
uv run awslabs.cloudscape-mcp-server
```

## Contributing

Contributions are welcome! Please see the main repository's [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.

## Related Resources

- [Cloudscape Design System](https://cloudscape.design)
- [Cloudscape Demos Repository](https://github.com/cloudscape-design/demos)
- [AWS MCP Servers](https://github.com/awslabs/mcp)
- [Model Context Protocol](https://modelcontextprotocol.io)
