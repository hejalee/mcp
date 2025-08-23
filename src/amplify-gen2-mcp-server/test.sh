#!/bin/bash

# AWS Strands Test Script Wrapper
# This script provides easy access to the MCP server testing functionality

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to print colored output
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to show usage
show_usage() {
    echo "AWS Strands MCP Server Test Runner"
    echo "=================================="
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  list                    List all available MCP servers"
    echo "  all                     Test all MCP servers"
    echo "  amplify                 Test Amplify Gen2 server (full suite)"
    echo "  amplify-local           Test Amplify Gen2 functions locally only"
    echo "  server <name>           Test specific server (partial names work)"
    echo "  help                    Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 list                 # List all servers"
    echo "  $0 all                  # Test all servers"
    echo "  $0 amplify              # Full Amplify Gen2 test suite"
    echo "  $0 amplify-local        # Local Amplify functions only"
    echo "  $0 server aws-docs      # Test AWS documentation server"
    echo "  $0 server amplify-gen2  # Test Amplify Gen2 server via MCP"
    echo ""
}

# Function to activate virtual environment if it exists
activate_venv() {
    if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
        print_color $BLUE "🔧 Activating virtual environment..."
        source "$SCRIPT_DIR/.venv/bin/activate"
    else
        print_color $YELLOW "⚠️  No virtual environment found, using system Python"
    fi
}

# Function to check if Python script exists
check_script() {
    local script_name=$1
    if [ ! -f "$SCRIPT_DIR/$script_name" ]; then
        print_color $RED "❌ Script not found: $script_name"
        exit 1
    fi
}

# Main execution
main() {
    cd "$SCRIPT_DIR"
    
    case "${1:-help}" in
        "list")
            print_color $BLUE "📋 Listing available MCP servers..."
            activate_venv
            check_script "aws_strands_test.py"
            python aws_strands_test.py --list
            ;;
            
        "all")
            print_color $BLUE "🚀 Testing all MCP servers..."
            activate_venv
            check_script "aws_strands_test.py"
            python aws_strands_test.py --all
            ;;
            
        "amplify")
            print_color $BLUE "🎯 Running full Amplify Gen2 test suite..."
            activate_venv
            check_script "run_amplify_tests.py"
            python run_amplify_tests.py
            ;;
            
        "amplify-local")
            print_color $BLUE "🧪 Running local Amplify Gen2 function tests..."
            activate_venv
            check_script "run_amplify_tests.py"
            python run_amplify_tests.py --local-only
            ;;
            
        "server")
            if [ -z "$2" ]; then
                print_color $RED "❌ Please specify a server name"
                echo "Usage: $0 server <server-name>"
                exit 1
            fi
            print_color $BLUE "🎯 Testing server: $2"
            activate_venv
            check_script "aws_strands_test.py"
            python aws_strands_test.py --servers "$2"
            ;;
            
        "help"|"-h"|"--help")
            show_usage
            ;;
            
        *)
            print_color $RED "❌ Unknown command: $1"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
