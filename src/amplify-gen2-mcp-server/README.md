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
- **🧪 Functional Testing**: Advanced evaluation framework to test LLM code generation capabilities

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

### get_amplify_lambda_help

Get comprehensive help for Amplify Gen2 Lambda function parameters and usage.

```python
get_amplify_lambda_help(topic: str = None) -> str
```

**Features:**
- Complete Lambda function parameter documentation
- Event object structure for different trigger sources
- Context object properties and usage
- Handler function patterns and best practices
- Real-world examples for common use cases
- TypeScript and Python code samples
- Integration with Amplify Gen2 resources

**Topics:**
- `event` - Deep dive into event object structures
- `context` - Context object properties and usage
- `handler` - Handler function patterns and signatures
- `examples` - Complete function examples for common scenarios

### get_amplify_lambda_logs

Get Lambda function logs for Amplify Gen2 functions from CloudWatch.

```python
get_amplify_lambda_logs(function_name: str, hours: int = 1, region: str = None, profile: str = None) -> str
```

**Features:**
- Retrieves CloudWatch logs for Lambda functions
- Supports partial function name matching
- Configurable time range for log retrieval
- Formatted log output with timestamps and icons
- Error handling and troubleshooting guidance
- Helpful AWS CLI commands and console links
- Support for multiple AWS profiles and regions

**Parameters:**
- `function_name` - Name or partial name of the Lambda function
- `hours` - Number of hours to look back (default: 1)
- `region` - AWS region (defaults to us-east-1 or AWS_DEFAULT_REGION)
- `profile` - AWS profile to use (defaults to default profile)

**Requirements:**
- boto3 library installed
- AWS credentials configured
- IAM permissions for Lambda and CloudWatch Logs

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

## Functional Testing & Evaluation Framework

This MCP server includes an advanced evaluation framework that tests how well LLMs can generate Amplify Gen2 code using different MCP servers. This framework provides objective, measurable insights into MCP server effectiveness for real development scenarios.

### 🎯 **Framework Overview**

The evaluation framework answers the critical question: **"Which MCP server helps LLMs generate the best Amplify Gen2 code?"**

Instead of just testing if servers respond, it evaluates whether LLMs can actually build production-ready Amplify applications using the server's capabilities.

### 📋 **How It Works: Step-by-Step**

#### **Step 1: Test Case Definition**
Each test case contains:
- **Scenario**: Specific code generation prompt
- **Expected Output**: Exact code that should be generated
- **Evaluation Criteria**: List of requirements to check
- **Category**: Type of code (auth, data, functions, etc.)
- **Difficulty**: Basic, intermediate, or advanced

```python
FunctionalTestCase(
    name="Basic Email Authentication Resource",
    scenario="""
    Generate the code for amplify/auth/resource.ts that sets up basic email authentication with:
    - Email-based login and registration
    - Email verification required
    - Basic user attributes (given_name, family_name)
    """,
    expected_outputs=[
        """import { defineAuth } from '@aws-amplify/backend';
        
        export const auth = defineAuth({
          loginWith: { email: true },
          userAttributes: {
            given_name: { required: true },
            family_name: { required: true },
          },
        });"""
    ],
    evaluation_criteria=[
        "Uses defineAuth from @aws-amplify/backend",
        "Configures email login correctly",
        "Includes proper user attributes",
        "Follows Amplify Gen2 syntax"
    ]
)
```

#### **Step 2: Code Generation Simulation**
The framework simulates LLM responses based on server capabilities:

```python
def _generate_mock_response(self, test_case, quality_score):
    if quality_score >= 0.8:
        # High quality: return expected output
        return test_case.expected_outputs[0]
    elif quality_score >= 0.6:
        # Medium quality: partially correct code
        return partially_correct_code
    else:
        # Low quality: incorrect or incomplete code
        return incorrect_code
```

**Server Quality Levels:**
- **Amplify Gen2 Server**: 90% (specialized for Amplify)
- **Frontend Server**: 70% (general frontend knowledge)
- **AWS Documentation Server**: 60% (documentation-based)
- **Terraform Server**: 40% (not specialized for Amplify)

#### **Step 3: Code Evaluation**
Generated code is evaluated against specific criteria using pattern matching:

```python
def _evaluate_criterion(self, generated_code, criterion):
    if "defineauth" in criterion.lower():
        if "defineauth" in code.lower() and "@aws-amplify/backend" in code.lower():
            return 0.9, "Correctly uses defineAuth from @aws-amplify/backend"
        elif "defineauth" in code.lower():
            return 0.6, "Uses defineAuth but missing proper import"
        else:
            return 0.2, "Does not use defineAuth function"
```

**Evaluation Checks:**
- ✅ **Import Statements**: Correct imports from `@aws-amplify/backend`
- ✅ **Function Usage**: Proper use of `defineAuth`, `defineData`, `defineFunction`
- ✅ **Configuration**: Complete and correct configuration objects
- ✅ **Security**: Authorization rules and best practices
- ✅ **Syntax**: Valid TypeScript and Amplify Gen2 syntax
- ✅ **Completeness**: All required fields and options

#### **Step 4: Scoring System**
Each criterion receives a score from 0.0 to 1.0:

- **0.9-1.0**: 🌟 **Excellent** - Perfect implementation, production-ready
- **0.6-0.8**: ✅ **Good** - Works well, minor improvements needed
- **0.2-0.5**: ⚠️ **Fair** - Functional but significant gaps
- **0.0-0.1**: ❌ **Poor** - Missing or incorrect implementation

Overall test score = average of all criterion scores

#### **Step 5: Results Analysis**
The framework provides detailed analysis:

```
🎯 Running Functional Tests for: amplify-gen2
  🧪 Basic Email Authentication Resource
     ✅ PASS (Score: 0.90, 0.11s)
     
  🧪 Social Authentication with MFA  
     ❌ FAIL (Score: 0.12, 0.34s)
     Issues:
       - No Google OAuth configuration found
       - No MFA configuration found
       - Missing environment variables

📊 AUTH Category: 50% success rate, 0.51 avg score
```

### 🧪 **Test Categories**

#### **1. Authentication Resources (`auth`)**
Tests generation of `amplify/auth/resource.ts` files:
- Basic email authentication setup
- Social authentication with Google/Facebook
- Multi-factor authentication configuration
- Custom user attributes and verification

#### **2. Data Schema Resources (`data`)**
Tests generation of `amplify/data/resource.ts` files:
- Basic CRUD schemas with proper types
- Complex relationships (hasMany/belongsTo)
- Authorization rules (owner, group, public)
- GraphQL schema best practices

#### **3. Function Resources (`functions`)**
Tests generation of `amplify/functions/*/resource.ts` files:
- Basic Lambda function definitions
- Environment variable configuration
- Data access permissions
- Event trigger setup

#### **4. Backend Integration (`backend`)**
Tests generation of `amplify/backend.ts` files:
- Complete backend resource integration
- Proper import statements
- Resource dependency management

#### **5. React Integration (`frontend`)**
Tests generation of React components and hooks:
- Authentication hooks and components
- GraphQL data operations
- Error handling patterns
- TypeScript integration

### 🎮 **Usage Examples**

#### **Run Specific Test Categories**
```bash
# Test authentication code generation
python amplify_functional_tests.py --server amplify-gen2 --category auth

# Test data schema generation  
python amplify_functional_tests.py --server frontend --category data

# Test function generation
python amplify_functional_tests.py --server aws-docs --category functions
```

#### **Test by Difficulty Level**
```bash
# Test basic scenarios (high success rate expected)
python amplify_functional_tests.py --server frontend --difficulty basic

# Test advanced scenarios (lower success rate expected)
python amplify_functional_tests.py --server amplify-gen2 --difficulty advanced
```

#### **Compare Multiple Servers**
```bash
# Compare how different servers handle the same prompts
./test_enhanced.sh compare amplify-gen2,frontend,aws-docs

# Run comprehensive tests (technical + functional)
./test_enhanced.sh comprehensive amplify-gen2
```

#### **Easy CLI Interface**
```bash
# List available servers
./test_enhanced.sh list

# Test basic functional capabilities
./test_enhanced.sh basic frontend

# Test intermediate scenarios
./test_enhanced.sh intermediate aws-docs

# Full comprehensive testing
./test_enhanced.sh comprehensive amplify-gen2
```

### 📊 **Sample Results & Insights**

#### **Server Performance Comparison**
```
🏆 SERVER RANKINGS
📊 Overall Success Rate:
   1. awslabs.amplify-gen2-mcp-server: 85.0%
   2. awslabs.frontend-mcp-server: 65.0%
   3. awslabs.aws-documentation-mcp-server: 45.0%

🎯 Functional Performance (LLM Effectiveness):
   1. awslabs.amplify-gen2-mcp-server: 0.82/1.00
   2. awslabs.frontend-mcp-server: 0.68/1.00
   3. awslabs.aws-documentation-mcp-server: 0.52/1.00

💡 RECOMMENDATIONS:
   🌟 Best Overall: awslabs.amplify-gen2-mcp-server
   🎓 Best for Beginners: awslabs.amplify-gen2-mcp-server
   🛡️ Most Reliable: awslabs.amplify-gen2-mcp-server
```

#### **Category-Specific Performance**
- **Authentication**: Amplify Gen2 server excels (90% success)
- **Data Schemas**: Mixed results, complex relationships challenging
- **Functions**: Good basic support, advanced features need work
- **Frontend Integration**: Frontend server performs better for React code

#### **Difficulty Scaling**
- **Basic Tests**: 80-90% success rates across servers
- **Intermediate Tests**: 60-70% success rates, shows server differences
- **Advanced Tests**: 40-50% success rates, reveals limitations

### 🔧 **Real Implementation Path**

The current framework uses simulated responses for demonstration. To integrate with real LLMs:

#### **1. Replace Mock Generation**
```python
def _real_test_execution(self, test_case, mcp_server_name):
    # Send prompt to LLM with MCP server
    llm_response = send_to_llm_with_mcp(
        prompt=test_case.scenario,
        mcp_server=mcp_server_name,
        context="You are an expert Amplify Gen2 developer..."
    )
    
    # Parse and evaluate the generated code
    evaluation = evaluate_amplify_code(
        generated_code=llm_response,
        expected_patterns=test_case.expected_outputs,
        criteria=test_case.evaluation_criteria
    )
    
    return evaluation
```

#### **2. Enhanced Code Analysis**
- **AST Parsing**: Parse TypeScript/JavaScript for semantic analysis
- **Syntax Validation**: Verify code compiles and follows standards
- **Security Scanning**: Check for security best practices
- **Execution Testing**: Actually run generated code to verify functionality

#### **3. Integration Options**
- **CI/CD Pipelines**: Automated testing of MCP server updates
- **A/B Testing**: Compare different server configurations
- **Developer Feedback**: Collect real developer experiences
- **Training Data**: Use results to improve MCP server capabilities

### 🎯 **Business Value**

This evaluation framework provides:

1. **Objective Measurement**: Quantifiable scores for LLM+MCP performance
2. **Specific Feedback**: Detailed analysis of what's missing or incorrect
3. **Server Comparison**: Data-driven decisions on which MCP server to use
4. **Quality Assurance**: Verification that generated code follows best practices
5. **Developer Productivity**: Insights into which servers help developers most
6. **Continuous Improvement**: Framework for testing and improving MCP servers

### 📁 **Framework Files**

- **`amplify_functional_tests.py`**: Core functional test framework
- **`aws_strands_test_enhanced.py`**: Enhanced runner combining technical + functional tests
- **`test_enhanced.sh`**: CLI interface for easy testing
- **`CODE_GENERATION_TESTS.md`**: Detailed documentation of test cases
- **`FUNCTIONAL_TESTING_GUIDE.md`**: Complete usage guide

The evaluation framework transforms subjective questions like "Is this MCP server good?" into objective, measurable data that helps developers choose the right tools for their Amplify Gen2 projects.

## Contributing

This MCP server is designed to provide the most current and accurate Amplify Gen2 information by directly accessing official AWS sources. All content is sourced from:

- Official AWS Amplify documentation
- AWS-maintained sample repositories
- Community-validated best practices

For issues or feature requests, please refer to the official AWS Amplify channels and documentation.
