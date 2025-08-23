# Lambda Logs Function Feature

## Overview
Added a comprehensive `get_amplify_lambda_logs` function to the Amplify Gen2 MCP server that retrieves and formats Lambda function logs from AWS CloudWatch Logs, specifically designed for debugging and monitoring Amplify Gen2 Lambda functions.

## What Was Added

### 1. New Function in `tools.py`
- **Function**: `get_amplify_lambda_logs(ctx, function_name: str, hours: int = 1, region: str = None, profile: str = None) -> str`
- **Purpose**: Retrieves CloudWatch logs for Amplify Gen2 Lambda functions with intelligent formatting and helpful debugging information
- **Features**:
  - Supports partial function name matching for easy discovery
  - Configurable time range for log retrieval
  - Formatted log output with timestamps and visual indicators
  - Comprehensive error handling and troubleshooting guidance
  - Helpful AWS CLI commands and console links
  - Support for multiple AWS profiles and regions
  - Graceful handling when boto3 is not available

### 2. MCP Tool Registration in `server.py`
- **Tool Name**: `get_amplify_lambda_logs_tool`
- **Parameters**: 
  - `function_name` (required): Name or partial name of the Lambda function
  - `hours` (optional, default: 1): Number of hours to look back
  - `region` (optional): AWS region
  - `profile` (optional): AWS profile to use
- **Integration**: Properly registered with the FastMCP server

### 3. Dependencies Updated in `pyproject.toml`
- Added `boto3>=1.26.0` to the dependencies list
- Ensures AWS SDK functionality is available

### 4. Documentation Updates in `README.md`
- Added comprehensive documentation for the new tool
- Included usage examples, parameters, and requirements
- Listed all features and capabilities

## Key Features

### Smart Function Discovery
- **Partial Name Matching**: Search for functions using partial names (e.g., "data-access" finds "amplify-myapp-dev-data-access-abc123")
- **Multiple Results**: Shows up to 5 matching functions
- **Function Metadata**: Displays ARN, runtime, and last modified date

### Intelligent Log Formatting
- **Visual Indicators**: Uses emojis to categorize different log types:
  - 🟢 Function start events
  - 🔴 Function end events  
  - 📊 Performance reports
  - ❌ Errors and exceptions
  - ⚠️ Warnings
  - ℹ️ General information
- **Timestamp Formatting**: Human-readable timestamps for easy debugging
- **Recent Events**: Shows the most recent 20 log events per function

### Comprehensive Error Handling
- **Missing boto3**: Provides installation instructions and alternative methods
- **No Credentials**: Shows multiple ways to configure AWS credentials
- **No Functions Found**: Suggests troubleshooting steps and common naming patterns
- **Permission Issues**: Displays required IAM permissions
- **Network/API Errors**: Provides debugging guidance

### Helpful Context and Commands
- **AWS CLI Commands**: Ready-to-use commands for extended log analysis
- **Amplify CLI Commands**: Amplify-specific log commands
- **CloudWatch Console Links**: Direct links to view logs in AWS console
- **Troubleshooting Guide**: Common issues and solutions

## Usage Examples

### Basic Usage
```python
# Get logs for a function (last 1 hour)
logs = get_amplify_lambda_logs(None, "my-function")

# Get logs for the last 24 hours
logs = get_amplify_lambda_logs(None, "data-access", hours=24)

# Use specific region and profile
logs = get_amplify_lambda_logs(None, "auth-trigger", hours=6, region="us-west-2", profile="dev")
```

### MCP Tool Usage
```bash
# Through MCP client - basic usage
get_amplify_lambda_logs_tool(function_name="my-function")

# With all parameters
get_amplify_lambda_logs_tool(function_name="data-access", hours=12, region="us-east-1", profile="production")
```

### Common Amplify Function Patterns
The function handles typical Amplify Gen2 function naming patterns:
- `amplify-<app-name>-<env>-<function-name>-<hash>`
- Partial matching works: searching "data-access" finds the full generated name

## Error Handling Scenarios

### 1. boto3 Not Available
```
# Lambda Logs - boto3 Not Available

## Error
The boto3 library is not available. To use Lambda logs functionality, install boto3:

```bash
pip install boto3
```

## Alternative Methods
[Shows AWS CLI, Console, and Amplify CLI alternatives]
```

### 2. AWS Credentials Not Configured
```
# Lambda Logs - AWS Credentials Not Found

## Setup AWS Credentials
[Shows multiple credential configuration methods]

## Required IAM Permissions
[Shows exact JSON policy needed]
```

### 3. No Functions Found
```
# Lambda Logs - No Functions Found

## Search Results
No Lambda functions found matching: **function-name**

## Suggestions
[Provides troubleshooting steps and naming pattern guidance]
```

## Output Format Example

```markdown
# Lambda Logs for "data-access"

**Time Range:** 2025-01-29 21:00:00 - 2025-01-29 22:00:00 UTC
**Region:** us-east-1
**Profile:** default

## Function: amplify-myapp-dev-data-access-abc123

**Details:**
- **ARN:** arn:aws:lambda:us-east-1:123456789012:function:amplify-myapp-dev-data-access-abc123
- **Runtime:** nodejs18.x
- **Last Modified:** 2025-01-29T20:30:00.000+0000
- **Log Group:** /aws/lambda/amplify-myapp-dev-data-access-abc123

**Log Events (15 entries):**

🟢 **21:45:32** - START RequestId: abc-123-def Version: $LATEST
ℹ️ **21:45:32** - Processing data access request
📊 **21:45:33** - REPORT RequestId: abc-123-def Duration: 1234.56 ms
🔴 **21:45:33** - END RequestId: abc-123-def

## Useful Commands
[Shows AWS CLI, Amplify CLI commands, and console links]

## Troubleshooting
[Provides debugging guidance for common issues]
```

## Requirements

### Runtime Requirements
- **boto3**: AWS SDK for Python (automatically installed with the package)
- **AWS Credentials**: Configured via AWS CLI, environment variables, or IAM roles
- **Network Access**: Ability to reach AWS APIs

### IAM Permissions Required
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

## Testing

Created comprehensive tests to verify:
- Function imports correctly
- Graceful handling when boto3 is not available
- Proper error handling for various scenarios
- MCP tool registration works correctly
- Parameter validation and processing
- Output formatting and content quality

## Benefits for Developers

1. **Unified Interface**: Access Lambda logs directly from the MCP server without switching tools
2. **Intelligent Search**: Find functions using partial names, perfect for Amplify's generated names
3. **Rich Formatting**: Visual indicators and timestamps make logs easy to read and debug
4. **Comprehensive Guidance**: Built-in troubleshooting and helpful commands
5. **Multi-Environment Support**: Works with different AWS profiles and regions
6. **Graceful Degradation**: Provides alternatives when dependencies aren't available
7. **Time-Efficient**: Quick access to recent logs without navigating AWS console

## Files Modified

1. **`awslabs/amplify_gen2_mcp_server/tools.py`**: Added the main `get_amplify_lambda_logs` function with comprehensive error handling
2. **`awslabs/amplify_gen2_mcp_server/server.py`**: Added MCP tool registration and import
3. **`pyproject.toml`**: Added boto3 dependency
4. **`README.md`**: Updated documentation with new tool information

## Future Enhancements

Potential areas for future improvement:
1. **Real-time Log Streaming**: Add support for following logs in real-time
2. **Log Filtering**: Add support for filtering logs by patterns or log levels
3. **Multiple Functions**: Support querying logs from multiple functions simultaneously
4. **Export Options**: Add options to export logs to files
5. **Performance Metrics**: Include function performance analysis from logs
6. **Integration with Amplify CLI**: Direct integration with `npx ampx logs` commands
7. **Log Aggregation**: Combine logs from related functions (e.g., all functions in an app)

This feature significantly enhances the debugging and monitoring capabilities of the Amplify Gen2 MCP server, making it easier for developers to troubleshoot their Lambda functions directly from their development environment.
