# Lambda Help Function Feature

## Overview
Added a comprehensive `get_amplify_lambda_help` function to the Amplify Gen2 MCP server that provides detailed guidance on Lambda function parameters, event structures, context objects, and usage patterns.

## What Was Added

### 1. New Function in `tools.py`
- **Function**: `get_amplify_lambda_help(ctx, topic: str = None) -> str`
- **Purpose**: Provides comprehensive help for Amplify Gen2 Lambda function parameters and usage
- **Features**:
  - Complete Lambda function parameter documentation
  - Event object structure for different trigger sources
  - Context object properties and usage
  - Handler function patterns and best practices
  - Real-world examples for common use cases
  - TypeScript and Python code samples
  - Integration with Amplify Gen2 resources

### 2. MCP Tool Registration in `server.py`
- **Tool Name**: `get_amplify_lambda_help_tool`
- **Parameters**: Optional `topic` parameter for focused help
- **Integration**: Properly registered with the FastMCP server

### 3. Documentation Updates in `README.md`
- Added comprehensive documentation for the new tool
- Included usage examples and available topics
- Listed all features and capabilities

## Available Topics

The function supports the following specific topics:

### `event` - Event Object Deep Dive
- Custom event structures
- API Gateway event format
- Cognito trigger events
- S3 events
- DynamoDB streams
- Event parsing examples

### `context` - Context Object Deep Dive
- Complete context object properties
- Runtime information access
- Memory and timeout monitoring
- Request tracking
- Usage examples

### `handler` - Handler Function Patterns
- Basic handler structure
- Typed handlers (TypeScript)
- Error handling patterns
- Amplify data access integration
- Best practices

### `examples` - Complete Function Examples
- User registration handler
- File processing handler
- API endpoint handler
- Scheduled function handler
- Real-world implementation patterns

## Function Capabilities

### Base Documentation (No Topic)
- Overview of Lambda functions in Amplify Gen2
- Function handler signatures for Node.js/TypeScript and Python
- Event object structure variations
- Context object properties
- Amplify Gen2 function definition patterns
- Common function patterns
- Environment variables access
- Error handling best practices
- Testing approaches
- Event sources and parameters
- Debugging tips

### Topic-Specific Help
When a specific topic is provided, the function returns the base documentation plus detailed information about that topic, providing comprehensive guidance for developers.

## Usage Examples

### Basic Usage
```python
# Get general lambda help
help_content = get_amplify_lambda_help(None)
```

### Topic-Specific Usage
```python
# Get event object help
event_help = get_amplify_lambda_help(None, "event")

# Get context object help
context_help = get_amplify_lambda_help(None, "context")

# Get handler patterns help
handler_help = get_amplify_lambda_help(None, "handler")

# Get complete examples
examples_help = get_amplify_lambda_help(None, "examples")
```

### MCP Tool Usage
```bash
# Through MCP client
get_amplify_lambda_help_tool()
get_amplify_lambda_help_tool(topic="event")
```

## Testing

Created comprehensive tests to verify:
- Function imports correctly
- Base help content is generated
- Topic-specific content is included
- All topics work as expected
- MCP tool registration is successful
- Content quality and completeness

## Benefits

1. **Comprehensive Reference**: Provides complete documentation for Lambda function development in Amplify Gen2
2. **Context-Aware Help**: Offers specific guidance based on the topic requested
3. **Real-World Examples**: Includes practical, working code examples
4. **Multi-Language Support**: Covers both TypeScript/Node.js and Python implementations
5. **Integration Focused**: Specifically tailored for Amplify Gen2 patterns and best practices
6. **Debugging Support**: Includes troubleshooting tips and monitoring guidance

## Files Modified

1. **`awslabs/amplify_gen2_mcp_server/tools.py`**: Added the main `get_amplify_lambda_help` function
2. **`awslabs/amplify_gen2_mcp_server/server.py`**: Added MCP tool registration
3. **`README.md`**: Updated documentation with new tool information
4. **Test files**: Created comprehensive tests to verify functionality

## Future Enhancements

Potential areas for future improvement:
1. Add more event source examples (EventBridge, SQS, etc.)
2. Include performance optimization tips
3. Add security best practices section
4. Include monitoring and observability guidance
5. Add integration examples with other AWS services
6. Include deployment and CI/CD patterns

This feature significantly enhances the Amplify Gen2 MCP server by providing developers with comprehensive, contextual help for Lambda function development, making it easier to understand parameters, implement handlers, and follow best practices.
