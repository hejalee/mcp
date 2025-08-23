#!/bin/bash

# Enhanced AWS Strands Test Script Wrapper
# This script provides access to both technical and functional LLM testing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
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
    echo "Enhanced AWS Strands MCP Server Test Runner"
    echo "=========================================="
    echo ""
    echo "This enhanced test runner evaluates how well LLMs can build Amplify Gen2"
    echo "websites using different MCP servers, with both technical and functional tests."
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  list                           List all available MCP servers"
    echo "  technical <server>             Run technical server tests only"
    echo "  functional <server>            Run functional LLM evaluation tests"
    echo "  basic <server>                 Run basic functional tests (beginner level)"
    echo "  intermediate <server>          Run intermediate functional tests"
    echo "  advanced <server>              Run advanced functional tests"
    echo "  comprehensive <server>         Run both technical and functional tests"
    echo "  compare <server1,server2,...>  Compare multiple servers"
    echo "  amplify                        Full Amplify Gen2 test suite"
    echo "  help                           Show this help message"
    echo ""
    echo "Test Categories:"
    echo "  📋 Technical Tests    - Server health, connectivity, basic functionality"
    echo "  🎯 Functional Tests   - LLM's ability to build real Amplify Gen2 applications"
    echo "     • Basic           - Simple auth, CRUD, file upload scenarios"
    echo "     • Intermediate    - Complex data models, social auth, serverless functions"
    echo "     • Advanced        - Full-stack apps, multi-platform, enterprise features"
    echo ""
    echo "Examples:"
    echo "  $0 list                                    # List all servers"
    echo "  $0 functional frontend                     # Test frontend server's LLM capabilities"
    echo "  $0 basic aws-docs                          # Basic functional tests with AWS docs server"
    echo "  $0 comprehensive amplify-gen2              # Full test suite for Amplify server"
    echo "  $0 compare amplify-gen2,frontend,aws-docs  # Compare multiple servers"
    echo ""
    echo "Functional Test Scenarios Include:"
    echo "  🔐 Authentication     - User auth, social login, federated identity"
    echo "  📊 Data Management    - GraphQL APIs, CRUD operations, relationships"
    echo "  📁 Storage           - File uploads, image handling, access control"
    echo "  ⚡ Functions         - Lambda functions, event triggers, integrations"
    echo "  🌐 Hosting           - Deployment, custom domains, CI/CD"
    echo "  🔗 Integration       - Full-stack apps, multi-platform development"
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
            
        "technical")
            if [ -z "$2" ]; then
                print_color $RED "❌ Please specify a server name"
                echo "Usage: $0 technical <server-name>"
                exit 1
            fi
            print_color $BLUE "🔧 Running technical tests for: $2"
            activate_venv
            check_script "aws_strands_test_enhanced.py"
            python aws_strands_test_enhanced.py --server "$2" --technical
            ;;
            
        "functional")
            if [ -z "$2" ]; then
                print_color $RED "❌ Please specify a server name"
                echo "Usage: $0 functional <server-name>"
                exit 1
            fi
            print_color $PURPLE "🎯 Running functional LLM evaluation tests for: $2"
            activate_venv
            check_script "aws_strands_test_enhanced.py"
            python aws_strands_test_enhanced.py --server "$2" --functional
            ;;
            
        "basic")
            if [ -z "$2" ]; then
                print_color $RED "❌ Please specify a server name"
                echo "Usage: $0 basic <server-name>"
                exit 1
            fi
            print_color $GREEN "🎓 Running basic functional tests for: $2"
            activate_venv
            check_script "aws_strands_test_enhanced.py"
            python aws_strands_test_enhanced.py --server "$2" --basic
            ;;
            
        "intermediate")
            if [ -z "$2" ]; then
                print_color $RED "❌ Please specify a server name"
                echo "Usage: $0 intermediate <server-name>"
                exit 1
            fi
            print_color $YELLOW "🚀 Running intermediate functional tests for: $2"
            activate_venv
            check_script "aws_strands_test_enhanced.py"
            python aws_strands_test_enhanced.py --server "$2" --intermediate
            ;;
            
        "advanced")
            if [ -z "$2" ]; then
                print_color $RED "❌ Please specify a server name"
                echo "Usage: $0 advanced <server-name>"
                exit 1
            fi
            print_color $RED "🔥 Running advanced functional tests for: $2"
            activate_venv
            check_script "aws_strands_test_enhanced.py"
            python aws_strands_test_enhanced.py --server "$2" --advanced
            ;;
            
        "comprehensive")
            if [ -z "$2" ]; then
                print_color $RED "❌ Please specify a server name"
                echo "Usage: $0 comprehensive <server-name>"
                exit 1
            fi
            print_color $CYAN "🎖️ Running comprehensive tests (technical + functional) for: $2"
            activate_venv
            check_script "aws_strands_test_enhanced.py"
            python aws_strands_test_enhanced.py --server "$2" --all
            ;;
            
        "compare")
            if [ -z "$2" ]; then
                print_color $RED "❌ Please specify server names to compare"
                echo "Usage: $0 compare <server1,server2,server3>"
                exit 1
            fi
            print_color $PURPLE "🏆 Comparing servers: $2"
            activate_venv
            check_script "aws_strands_test_enhanced.py"
            python aws_strands_test_enhanced.py --compare "$2" --functional
            ;;
            
        "amplify")
            print_color $CYAN "🎯 Running full Amplify Gen2 test suite..."
            activate_venv
            check_script "run_amplify_tests.py"
            python run_amplify_tests.py
            ;;
            
        "demo")
            print_color $PURPLE "🎬 Running demo of functional tests..."
            echo ""
            print_color $CYAN "This will demonstrate the functional testing capabilities:"
            echo "1. Basic authentication setup test"
            echo "2. Data management test"
            echo "3. File upload test"
            echo ""
            activate_venv
            check_script "amplify_functional_tests.py"
            python amplify_functional_tests.py --server "demo-server" --category auth
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

# Show banner
print_color $CYAN "╔══════════════════════════════════════════════════════════════╗"
print_color $CYAN "║           Enhanced AWS Strands MCP Test Suite               ║"
print_color $CYAN "║        Technical + Functional LLM Evaluation Tests          ║"
print_color $CYAN "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Run main function with all arguments
main "$@"
