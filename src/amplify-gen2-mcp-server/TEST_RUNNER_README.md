# AWS Strands Test Runner for MCP Servers

This test runner provides comprehensive testing capabilities for AWS MCP (Model Context Protocol) servers configured in Amazon Q CLI.

## Features

- **Multi-Server Testing**: Test multiple MCP servers with a single command
- **Configurable Test Cases**: Server-specific and common test cases
- **Detailed Reporting**: Comprehensive test results with timing and error details
- **Flexible Server Selection**: Test all servers or select specific ones
- **Health Checks**: Basic connectivity and configuration validation
- **Real Function Testing**: Tests actual MCP server functions when available

## Quick Start

### List Available Servers
```bash
python aws_strands_test.py --list
```

### Test All Servers
```bash
python aws_strands_test.py --all
```

### Test Specific Servers
```bash
# Test Amplify Gen2 server
python aws_strands_test.py --servers amplify-gen2

# Test multiple servers (partial names work)
python aws_strands_test.py --servers amplify-gen2,aws-docs

# Test with full server names
python aws_strands_test.py --servers "awslabs.amplify-gen2-mcp-server,awslabs.aws-documentation-mcp-server"
```

### Use Custom Config File
```bash
python aws_strands_test.py --config /path/to/custom/mcp.json --all
```

## Test Cases by Server

### Common Tests (All Servers)
- **Server Health Check**: Validates server configuration and command availability

### AWS Documentation MCP Server
- **Documentation Search**: Tests search functionality
- **Documentation Read**: Tests document reading capabilities

### Amplify Gen2 MCP Server
- **Amplify Guidance**: Tests guidance generation for various topics
- **Amplify Code Generation**: Tests code generation for different frameworks
- **Lambda Logs**: Tests Lambda log retrieval functionality

### Terraform MCP Server
- **Terraform Validation**: Tests Terraform configuration validation

### Cloudscape MCP Server
- **Cloudscape Components**: Tests component generation

### Frontend MCP Server
- **Frontend Guidance**: Tests frontend development guidance

## Configuration

The test runner reads MCP server configurations from:
- Default: `/Users/hejalee/.aws/amazonq/mcp.json.backup`
- Custom: Specify with `--config` parameter

### MCP Configuration Format
```json
{
  "mcpServers": {
    "server-name": {
      "command": "uvx",
      "args": ["package-name@latest"],
      "env": {
        "ENV_VAR": "value"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## Test Results

The test runner provides detailed output including:

- **Real-time Progress**: See tests running in real-time
- **Individual Results**: Pass/fail status with timing for each test
- **Error Details**: Detailed error messages for failed tests
- **Summary Report**: Overall statistics and per-server breakdowns
- **Success Rates**: Percentage of tests passed per server

### Sample Output
```
🚀 Testing server: awslabs.amplify-gen2-mcp-server
   Command: uvx --from git+https://github.com/hejalee/mcp.git#subdirectory=src/amplify-gen2-mcp-server awslabs.amplify-gen2-mcp-server
   Status: 🟢 ENABLED
  🧪 Running: Server Health Check
     ✅ PASS (0.12s)
  🧪 Running: Amplify Guidance
     ✅ PASS (1.45s)
  🧪 Running: Amplify Code Generation
     ✅ PASS (0.89s)

================================================================================
📊 TEST SUMMARY
================================================================================
Total Tests: 6
Passed: 5 ✅
Failed: 1 ❌
Success Rate: 83.3%
Total Duration: 4.23s
```

## Extending the Test Runner

### Adding New Test Cases

1. **Add test function** to the `AWSStrandsTestRunner` class:
```python
def _test_my_new_feature(self, server_name: str) -> tuple[bool, str, Optional[str]]:
    """Test my new feature."""
    try:
        # Your test logic here
        return True, "Test completed successfully", None
    except Exception as e:
        return False, "", str(e)
```

2. **Add to server-specific tests** in `get_test_cases()`:
```python
"my-server-name": [
    {
        "name": "My New Feature Test",
        "description": "Tests my new feature",
        "test_func": self._test_my_new_feature
    }
]
```

### Adding New Servers

Simply add the server configuration to your MCP config file. The test runner will automatically detect it and run common tests. Add server-specific tests by extending the `get_test_cases()` method.

## Troubleshooting

### Common Issues

1. **Server Not Found**: Check that the server name in your MCP config matches what you're testing
2. **Command Not Found**: Ensure the MCP server command (like `uvx`) is in your PATH
3. **Import Errors**: Make sure the MCP server packages are properly installed
4. **Permission Errors**: Ensure the test script has execute permissions

### Debug Mode

For more detailed output, you can modify the script to add debug logging or run individual test functions directly.

### Manual Testing

You can also run individual test components:
```python
# Test a specific server directly
runner = AWSStrandsTestRunner()
results = runner.run_tests_for_server("awslabs.amplify-gen2-mcp-server")
```

## Integration with CI/CD

The test runner returns appropriate exit codes:
- `0`: All tests passed
- `1`: Some tests failed or errors occurred

This makes it suitable for integration with CI/CD pipelines:
```bash
python aws_strands_test.py --all
if [ $? -eq 0 ]; then
    echo "All MCP server tests passed!"
else
    echo "Some MCP server tests failed!"
    exit 1
fi
```

## Contributing

When adding new test cases or servers:

1. Follow the existing pattern for test functions
2. Return appropriate success/failure indicators
3. Provide meaningful error messages
4. Add documentation for new test cases
5. Test your changes with multiple server configurations

## License

This test runner follows the same license as the parent MCP server project (Apache 2.0).
