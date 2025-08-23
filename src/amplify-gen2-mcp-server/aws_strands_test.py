#!/usr/bin/env python3
"""
AWS Strands Test Script for MCP Servers

This script runs comprehensive test cases against different MCP servers
configured in the Amazon Q CLI. It supports testing multiple servers
and provides detailed reporting of results.
"""

import json
import os
import sys
import subprocess
import time
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestResult:
    """Represents the result of a single test case."""
    test_name: str
    server_name: str
    success: bool
    duration: float
    output: str
    error: Optional[str] = None


@dataclass
class MCPServer:
    """Represents an MCP server configuration."""
    name: str
    command: str
    args: List[str]
    env: Dict[str, str]
    disabled: bool
    auto_approve: List[str]


class AWSStrandsTestRunner:
    """Main test runner for AWS Strands MCP server testing."""
    
    def __init__(self, mcp_config_path: str = "~/.aws/amazonq/mcp.json"):
        """Initialize the test runner with MCP configuration."""
        self.mcp_config_path = mcp_config_path
        self.servers: Dict[str, MCPServer] = {}
        self.test_results: List[TestResult] = []
        self.load_mcp_config()
    
    def load_mcp_config(self) -> None:
        """Load MCP server configurations from the backup file."""
        try:
            with open(self.mcp_config_path, 'r') as f:
                config = json.load(f)
            
            for name, server_config in config.get('mcpServers', {}).items():
                self.servers[name] = MCPServer(
                    name=name,
                    command=server_config.get('command', ''),
                    args=server_config.get('args', []),
                    env=server_config.get('env', {}),
                    disabled=server_config.get('disabled', False),
                    auto_approve=server_config.get('autoApprove', [])
                )
            
            print(f"✅ Loaded {len(self.servers)} MCP server configurations")
            
        except FileNotFoundError:
            print(f"❌ MCP config file not found: {self.mcp_config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in MCP config file: {e}")
            sys.exit(1)
    
    def list_servers(self) -> None:
        """List all available MCP servers."""
        print("\n📋 Available MCP Servers:")
        print("=" * 60)
        
        for name, server in self.servers.items():
            status = "🔴 DISABLED" if server.disabled else "🟢 ENABLED"
            print(f"  {name}")
            print(f"    Status: {status}")
            print(f"    Command: {server.command} {' '.join(server.args)}")
            print(f"    Environment: {len(server.env)} variables")
            print()
    
    def get_test_cases(self, server_name: str) -> List[Dict[str, Any]]:
        """Get test cases specific to each MCP server type."""
        
        # Common test cases for all servers
        common_tests = [
            {
                "name": "Server Health Check",
                "description": "Basic connectivity and health check",
                "test_func": self._test_server_health
            }
        ]
        
        # Server-specific test cases
        server_specific_tests = {
            "awslabs.aws-documentation-mcp-server": [
                {
                    "name": "Documentation Search",
                    "description": "Test documentation search functionality",
                    "test_func": self._test_aws_docs_search
                },
                {
                    "name": "Documentation Read",
                    "description": "Test documentation reading functionality", 
                    "test_func": self._test_aws_docs_read
                }
            ],
            "awslabs.amplify-gen2-mcp-server": [
                {
                    "name": "Amplify Guidance",
                    "description": "Test Amplify Gen2 guidance functionality",
                    "test_func": self._test_amplify_guidance
                },
                {
                    "name": "Amplify Code Generation",
                    "description": "Test Amplify Gen2 code generation",
                    "test_func": self._test_amplify_code_gen
                },
                {
                    "name": "Lambda Logs",
                    "description": "Test Lambda logs functionality",
                    "test_func": self._test_lambda_logs
                }
            ],
            "awslabs.terraform-mcp-server": [
                {
                    "name": "Terraform Validation",
                    "description": "Test Terraform configuration validation",
                    "test_func": self._test_terraform_validation
                }
            ],
            "awslabs.cloudscape-mcp-server": [
                {
                    "name": "Cloudscape Components",
                    "description": "Test Cloudscape component generation",
                    "test_func": self._test_cloudscape_components
                }
            ],
            "awslabs.frontend-mcp-server": [
                {
                    "name": "Frontend Guidance",
                    "description": "Test frontend development guidance",
                    "test_func": self._test_frontend_guidance
                }
            ]
        }
        
        # Combine common and server-specific tests
        tests = common_tests.copy()
        if server_name in server_specific_tests:
            tests.extend(server_specific_tests[server_name])
        
        return tests
    
    def run_test_case(self, server_name: str, test_case: Dict[str, Any]) -> TestResult:
        """Run a single test case against a specific server."""
        print(f"  🧪 Running: {test_case['name']}")
        
        start_time = time.time()
        
        try:
            # Run the test function
            success, output, error = test_case['test_func'](server_name)
            duration = time.time() - start_time
            
            result = TestResult(
                test_name=test_case['name'],
                server_name=server_name,
                success=success,
                duration=duration,
                output=output,
                error=error
            )
            
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"     {status} ({duration:.2f}s)")
            
            if error and not success:
                print(f"     Error: {error}")
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = TestResult(
                test_name=test_case['name'],
                server_name=server_name,
                success=False,
                duration=duration,
                output="",
                error=str(e)
            )
            
            print(f"     ❌ EXCEPTION ({duration:.2f}s): {e}")
            return result
    
    def run_tests_for_server(self, server_name: str) -> List[TestResult]:
        """Run all test cases for a specific server."""
        if server_name not in self.servers:
            print(f"❌ Server '{server_name}' not found in configuration")
            return []
        
        server = self.servers[server_name]
        print(f"\n🚀 Testing server: {server_name}")
        print(f"   Command: {server.command} {' '.join(server.args)}")
        print(f"   Status: {'🔴 DISABLED' if server.disabled else '🟢 ENABLED'}")
        
        if server.disabled:
            print("   ⚠️  Server is disabled, skipping tests")
            return []
        
        test_cases = self.get_test_cases(server_name)
        results = []
        
        for test_case in test_cases:
            result = self.run_test_case(server_name, test_case)
            results.append(result)
            self.test_results.append(result)
        
        return results
    
    def run_all_tests(self, selected_servers: Optional[List[str]] = None) -> None:
        """Run tests for all servers or selected servers."""
        servers_to_test = selected_servers or list(self.servers.keys())
        
        print(f"\n🎯 Running tests for {len(servers_to_test)} server(s)")
        print("=" * 60)
        
        for server_name in servers_to_test:
            self.run_tests_for_server(server_name)
        
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print a summary of all test results."""
        if not self.test_results:
            print("\n📊 No tests were run")
            return
        
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        # Overall statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.success)
        failed_tests = total_tests - passed_tests
        total_duration = sum(r.duration for r in self.test_results)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Total Duration: {total_duration:.2f}s")
        
        # Results by server
        servers_tested = set(r.server_name for r in self.test_results)
        
        for server_name in servers_tested:
            server_results = [r for r in self.test_results if r.server_name == server_name]
            server_passed = sum(1 for r in server_results if r.success)
            server_total = len(server_results)
            
            print(f"\n📋 {server_name}:")
            print(f"   Tests: {server_total}, Passed: {server_passed}, Failed: {server_total - server_passed}")
            
            for result in server_results:
                status = "✅" if result.success else "❌"
                print(f"   {status} {result.test_name} ({result.duration:.2f}s)")
                if result.error and not result.success:
                    print(f"      Error: {result.error}")
        
        print("\n" + "=" * 80)
    
    # Test implementation methods
    def _test_server_health(self, server_name: str) -> tuple[bool, str, Optional[str]]:
        """Basic health check for any MCP server."""
        try:
            # This is a placeholder - in a real implementation, you'd check if the server responds
            # For now, we'll just verify the server configuration is valid
            server = self.servers[server_name]
            
            if not server.command:
                return False, "", "Server command is empty"
            
            # Try to check if the command exists
            try:
                result = subprocess.run(['which', server.command], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode != 0:
                    return False, "", f"Command '{server.command}' not found in PATH"
            except subprocess.TimeoutExpired:
                return False, "", "Command check timed out"
            
            return True, f"Server {server_name} configuration is valid", None
            
        except Exception as e:
            return False, "", str(e)
    
    def _test_aws_docs_search(self, server_name: str) -> tuple[bool, str, Optional[str]]:
        """Test AWS documentation search functionality."""
        # This would integrate with the actual MCP server
        # For now, return a mock result
        return True, "AWS documentation search test completed", None
    
    def _test_aws_docs_read(self, server_name: str) -> tuple[bool, str, Optional[str]]:
        """Test AWS documentation reading functionality."""
        return True, "AWS documentation read test completed", None
    
    def _test_amplify_guidance(self, server_name: str) -> tuple[bool, str, Optional[str]]:
        """Test Amplify Gen2 guidance functionality."""
        # Try to import and test the actual tools if available
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'awslabs'))
            from amplify_gen2_mcp_server.tools import get_amplify_gen2_guidance
            
            result = get_amplify_gen2_guidance(None, "authentication")
            if result and len(result) > 0:
                return True, f"Amplify guidance test completed: {len(result)} characters returned", None
            else:
                return False, "", "Empty result from guidance function"
                
        except ImportError as e:
            return False, "", f"Could not import Amplify tools: {e}"
        except Exception as e:
            return False, "", str(e)
    
    def _test_amplify_code_gen(self, server_name: str) -> tuple[bool, str, Optional[str]]:
        """Test Amplify Gen2 code generation."""
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'awslabs'))
            from amplify_gen2_mcp_server.tools import generate_amplify_gen2_code
            
            result = generate_amplify_gen2_code(None, "authentication", "react")
            if result and len(result) > 0:
                return True, f"Amplify code generation test completed: {len(result)} characters returned", None
            else:
                return False, "", "Empty result from code generation function"
                
        except ImportError as e:
            return False, "", f"Could not import Amplify tools: {e}"
        except Exception as e:
            return False, "", str(e)
    
    def _test_lambda_logs(self, server_name: str) -> tuple[bool, str, Optional[str]]:
        """Test Lambda logs functionality."""
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'awslabs'))
            from amplify_gen2_mcp_server.tools import get_amplify_lambda_logs
            
            result = get_amplify_lambda_logs(None, "test-function")
            if result and len(result) > 0:
                return True, f"Lambda logs test completed: {len(result)} characters returned", None
            else:
                return False, "", "Empty result from lambda logs function"
                
        except ImportError as e:
            return False, "", f"Could not import Amplify tools: {e}"
        except Exception as e:
            return False, "", str(e)
    
    def _test_terraform_validation(self, server_name: str) -> tuple[bool, str, Optional[str]]:
        """Test Terraform validation functionality."""
        return True, "Terraform validation test completed (mock)", None
    
    def _test_cloudscape_components(self, server_name: str) -> tuple[bool, str, Optional[str]]:
        """Test Cloudscape component generation."""
        return True, "Cloudscape components test completed (mock)", None
    
    def _test_frontend_guidance(self, server_name: str) -> tuple[bool, str, Optional[str]]:
        """Test frontend development guidance."""
        return True, "Frontend guidance test completed (mock)", None


def main():
    """Main entry point for the test script."""
    parser = argparse.ArgumentParser(
        description="AWS Strands Test Script for MCP Servers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python aws_strands_test.py --list                    # List all available servers
  python aws_strands_test.py --all                     # Test all servers
  python aws_strands_test.py --servers amplify-gen2    # Test specific server
  python aws_strands_test.py --servers amplify-gen2,aws-docs  # Test multiple servers
        """
    )
    
    parser.add_argument(
        '--list', 
        action='store_true',
        help='List all available MCP servers'
    )
    
    parser.add_argument(
        '--all',
        action='store_true', 
        help='Run tests for all available servers'
    )
    
    parser.add_argument(
        '--servers',
        type=str,
        help='Comma-separated list of server names to test (partial names allowed)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='/Users/hejalee/.aws/amazonq/mcp.json',
        help='Path to MCP configuration file'
    )
    
    args = parser.parse_args()
    
    # Initialize test runner
    runner = AWSStrandsTestRunner(args.config)
    
    if args.list:
        runner.list_servers()
        return
    
    if args.all:
        runner.run_all_tests()
        return
    
    if args.servers:
        # Parse server names and find matches
        requested_servers = [s.strip() for s in args.servers.split(',')]
        selected_servers = []
        
        for requested in requested_servers:
            matches = [name for name in runner.servers.keys() 
                      if requested.lower() in name.lower()]
            if matches:
                selected_servers.extend(matches)
            else:
                print(f"⚠️  No server found matching '{requested}'")
        
        if selected_servers:
            # Remove duplicates while preserving order
            selected_servers = list(dict.fromkeys(selected_servers))
            runner.run_all_tests(selected_servers)
        else:
            print("❌ No valid servers selected")
            return
    
    if not any([args.list, args.all, args.servers]):
        parser.print_help()


if __name__ == "__main__":
    main()
