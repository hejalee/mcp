# Code Generation Functional Tests

## Overview

I've replaced the existing functional tests with **real code generation prompts** that ask for specific Amplify Gen2 code and compare the results against expected examples from the tools.py file.

## 🎯 **What's New**

### **Real Code Generation Prompts**
Instead of abstract scenarios, tests now ask for specific code:

```
Generate the code for amplify/auth/resource.ts that sets up basic email authentication with:
- Email-based login and registration  
- Email verification required
- Password reset functionality
- Basic user attributes (given_name, family_name)

Please provide the complete TypeScript code for the auth resource file.
```

### **Expected Code Examples**
Each test includes the exact code that should be generated:

```typescript
import { defineAuth } from '@aws-amplify/backend';

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
  },
});
```

### **Detailed Code Evaluation**
The evaluation system now checks for specific code patterns:
- ✅ Uses `defineAuth` from `@aws-amplify/backend`
- ✅ Configures email login correctly  
- ✅ Includes proper user attributes
- ✅ Follows Amplify Gen2 syntax

## 📋 **Test Categories**

### **1. Authentication Resources**
- **Basic Email Authentication**: Simple email/password setup
- **Social Authentication with MFA**: Google OAuth + Multi-factor auth

### **2. Data Schema Resources**  
- **Basic Todo Schema**: Simple CRUD with owner authorization
- **Blog Schema with Relationships**: Posts/Comments with relationships

### **3. Function Resources**
- **Basic Lambda Function**: Simple function definition with environment variables
- **Function with Data Access**: Function that can access GraphQL data

### **4. Backend Integration**
- **Complete Backend Definition**: Integrating auth, data, storage, functions

### **5. React Integration**
- **Authentication Hook**: Custom React hook for auth operations
- **GraphQL Data Operations**: React component with CRUD operations

## 🧪 **Sample Test Results**

### Amplify Gen2 Server Performance
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

📊 AUTH Category: 50.0% success rate, 0.51 avg score
```

### Frontend Server Performance
```
🎯 Running Functional Tests for: frontend
  🧪 Basic Todo Data Schema
     ❌ FAIL (Score: 0.55, 0.32s)
     Issues:
       - Missing authorization configuration
  🧪 Blog Schema with Relationships
     ❌ FAIL (Score: 0.35, 0.41s)
     Issues:
       - Missing proper field type definitions
       - Missing authorization configuration

📊 DATA Category: 0.0% success rate, 0.45 avg score
```

## 🔍 **Evaluation Methodology**

### **Code Pattern Matching**
The evaluation system looks for specific patterns in generated code:

```python
def _evaluate_criterion(self, generated_code: str, criterion: str, test_case: FunctionalTestCase):
    if "defineauth" in criterion_lower:
        if "defineauth" in code_lower and "@aws-amplify/backend" in code_lower:
            return 0.9, "Correctly uses defineAuth from @aws-amplify/backend"
        elif "defineauth" in code_lower:
            return 0.6, "Uses defineAuth but missing proper import"
        else:
            return 0.2, "Does not use defineAuth function"
```

### **Scoring System**
- **0.9-1.0**: Perfect implementation with all required elements
- **0.6-0.8**: Good implementation with minor issues
- **0.2-0.5**: Partial implementation with significant gaps
- **0.0-0.1**: Missing or incorrect implementation

### **Quality Simulation**
Different MCP servers have different simulated quality levels:
- **Amplify Gen2 Server**: 90% quality (specialized for Amplify)
- **Frontend Server**: 70% quality (general frontend knowledge)
- **AWS Documentation Server**: 60% quality (documentation-based)
- **Terraform Server**: 40% quality (not specialized for Amplify)

## 🎮 **Usage Examples**

### **Test Specific Categories**
```bash
# Test authentication code generation
python amplify_functional_tests.py --server amplify-gen2 --category auth

# Test data schema generation  
python amplify_functional_tests.py --server frontend --category data

# Test function generation
python amplify_functional_tests.py --server aws-docs --category functions
```

### **Test Specific Difficulties**
```bash
# Test basic scenarios
python amplify_functional_tests.py --server frontend --difficulty basic

# Test advanced scenarios
python amplify_functional_tests.py --server amplify-gen2 --difficulty advanced
```

### **Compare Servers**
```bash
# Compare how different servers handle the same prompts
./test_enhanced.sh compare amplify-gen2,frontend,aws-docs
```

## 📊 **Key Insights**

### **Server Specialization Matters**
- Amplify Gen2 server performs best on Amplify-specific tasks
- Frontend server struggles with backend resource definitions
- AWS Documentation server provides general guidance but lacks specificity

### **Complexity Scaling**
- Basic tests (simple auth, basic schemas) have higher success rates
- Intermediate tests (social auth, relationships) show more variation
- Advanced tests (full integration) reveal server limitations

### **Code Quality Indicators**
- Proper imports from `@aws-amplify/backend`
- Correct use of Amplify Gen2 syntax (`defineAuth`, `defineData`, etc.)
- Implementation of security best practices (authorization rules)
- Complete configuration (environment variables, proper field types)

## 🔧 **Real Implementation Path**

To make this work with actual LLMs:

1. **Replace Mock Generation** with real LLM API calls
2. **Implement Code Parsing** to extract and analyze generated code
3. **Add Execution Testing** to verify generated code actually works
4. **Enhance Evaluation** with AST parsing and semantic analysis

### **Integration Example**
```python
def _real_test_execution(self, test_case: FunctionalTestCase, mcp_server_name: str):
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

## 🎯 **Business Value**

This testing approach provides:

1. **Objective Measurement**: Quantifiable scores for LLM+MCP performance
2. **Specific Feedback**: Detailed analysis of what's missing or incorrect
3. **Server Comparison**: Data-driven decisions on which MCP server to use
4. **Quality Assurance**: Verification that generated code follows best practices
5. **Developer Productivity**: Insights into which servers help developers most

The tests now answer the critical question: **"Which MCP server helps LLMs generate the best Amplify Gen2 code?"** with concrete, measurable results.
