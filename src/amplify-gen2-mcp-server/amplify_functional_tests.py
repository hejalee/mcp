#!/usr/bin/env python3
"""
Amplify Gen2 Functional Test Suite

This test suite evaluates how well an LLM can build Amplify Gen2 websites
using MCP servers. Tests are focused on real development scenarios and
are independent of the specific MCP server implementation.
"""

import json
import os
import sys
import time
import tempfile
import shutil
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FunctionalTestCase:
    """Represents a functional test case for Amplify Gen2 development."""
    name: str
    description: str
    scenario: str
    expected_outputs: List[str]
    evaluation_criteria: List[str]
    difficulty: str  # "basic", "intermediate", "advanced"
    category: str    # "auth", "data", "storage", "hosting", "functions", "integration"


@dataclass
class TestResult:
    """Result of a functional test execution."""
    test_name: str
    success: bool
    score: float  # 0.0 to 1.0
    duration: float
    outputs_generated: List[str]
    evaluation_details: Dict[str, Any]
    error: Optional[str] = None


class AmplifyFunctionalTestRunner:
    """Runs functional tests for Amplify Gen2 development scenarios."""
    
    def __init__(self):
        """Initialize the functional test runner."""
        self.test_cases = self._load_test_cases()
        self.results: List[TestResult] = []
    
    def _load_test_cases(self) -> List[FunctionalTestCase]:
        """Load all functional test cases with actual code generation prompts."""
        return [
            # Authentication Resource Tests
            FunctionalTestCase(
                name="Basic Email Authentication Resource",
                description="Generate amplify/auth/resource.ts for email authentication",
                scenario="""
                Generate the code for amplify/auth/resource.ts that sets up basic email authentication with the following requirements:
                - Email-based login and registration
                - Email verification required
                - Password reset functionality
                - Basic user attributes (given_name, family_name)
                
                Please provide the complete TypeScript code for the auth resource file.
                """,
                expected_outputs=[
                    """import { defineAuth } from '@aws-amplify/backend';

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
});"""
                ],
                evaluation_criteria=[
                    "Uses defineAuth from @aws-amplify/backend",
                    "Configures email login correctly",
                    "Includes proper user attributes",
                    "Follows Amplify Gen2 syntax"
                ],
                difficulty="basic",
                category="auth"
            ),
            
            FunctionalTestCase(
                name="Social Authentication with MFA",
                description="Generate auth resource with social providers and MFA",
                scenario="""
                Generate the code for amplify/auth/resource.ts that includes:
                - Email authentication
                - Google OAuth integration
                - Multi-factor authentication (optional mode)
                - SMS and TOTP support
                
                Please provide the complete TypeScript code for the auth resource file.
                """,
                expected_outputs=[
                    """import { defineAuth } from '@aws-amplify/backend';

export const auth = defineAuth({
  loginWith: {
    email: true,
    externalProviders: {
      google: {
        clientId: process.env.GOOGLE_CLIENT_ID,
        scopes: ['profile', 'email', 'openid'],
      },
    },
  },
  multifactor: {
    mode: 'OPTIONAL',
    sms: true,
    totp: true,
  },
});"""
                ],
                evaluation_criteria=[
                    "Includes Google OAuth configuration",
                    "Configures MFA with SMS and TOTP",
                    "Uses environment variables for client ID",
                    "Sets MFA mode correctly"
                ],
                difficulty="intermediate",
                category="auth"
            ),
            
            # Data Schema Tests
            FunctionalTestCase(
                name="Basic Todo Data Schema",
                description="Generate amplify/data/resource.ts for a Todo application",
                scenario="""
                Generate the code for amplify/data/resource.ts that creates a Todo application schema with:
                - Todo model with id, content, done, and createdAt fields
                - Owner-based authorization (users can only access their own todos)
                - Proper field types and requirements
                
                Please provide the complete TypeScript code for the data resource file.
                """,
                expected_outputs=[
                    """import { a, defineData } from '@aws-amplify/backend';

const schema = a.schema({
  Todo: a.model({
    id: a.id(),
    content: a.string().required(),
    done: a.boolean().default(false),
    createdAt: a.datetime(),
  }).authorization(allow => [allow.owner()]),
});

export type Schema = ClientSchema<typeof schema>;

export const data = defineData({
  schema,
  authorizationModes: {
    defaultAuthorizationMode: 'userPool',
  },
});"""
                ],
                evaluation_criteria=[
                    "Uses a.schema and defineData correctly",
                    "Includes proper field types (id, string, boolean, datetime)",
                    "Implements owner-based authorization",
                    "Exports Schema type correctly"
                ],
                difficulty="basic",
                category="data"
            ),
            
            FunctionalTestCase(
                name="Blog Schema with Relationships",
                description="Generate data schema for a blog with posts and comments",
                scenario="""
                Generate the code for amplify/data/resource.ts for a blog application with:
                - Post model (id, title, content, authorId, createdAt)
                - Comment model (id, content, postId, authorId, createdAt)
                - Proper relationships between posts and comments
                - Authorization allowing owners to manage their content and public read access
                
                Please provide the complete TypeScript code for the data resource file.
                """,
                expected_outputs=[
                    """import { a, defineData } from '@aws-amplify/backend';

const schema = a.schema({
  Post: a.model({
    id: a.id(),
    title: a.string().required(),
    content: a.string().required(),
    authorId: a.string().required(),
    createdAt: a.datetime(),
    comments: a.hasMany('Comment', 'postId'),
  }).authorization(allow => [
    allow.owner().to(['create', 'update', 'delete']),
    allow.authenticated().to(['read'])
  ]),
  
  Comment: a.model({
    id: a.id(),
    content: a.string().required(),
    postId: a.id().required(),
    authorId: a.string().required(),
    createdAt: a.datetime(),
    post: a.belongsTo('Post', 'postId'),
  }).authorization(allow => [
    allow.owner().to(['create', 'update', 'delete']),
    allow.authenticated().to(['read'])
  ]),
});

export type Schema = ClientSchema<typeof schema>;

export const data = defineData({
  schema,
  authorizationModes: {
    defaultAuthorizationMode: 'userPool',
  },
});"""
                ],
                evaluation_criteria=[
                    "Defines proper hasMany/belongsTo relationships",
                    "Uses correct field types and requirements",
                    "Implements granular authorization rules",
                    "Includes proper model structure"
                ],
                difficulty="intermediate",
                category="data"
            ),
            
            # Function Tests
            FunctionalTestCase(
                name="Basic Lambda Function Resource",
                description="Generate amplify/functions/my-function/resource.ts",
                scenario="""
                Generate the code for amplify/functions/email-sender/resource.ts that:
                - Defines a function named 'email-sender'
                - Points to handler.ts as entry point
                - Includes environment variables for API_URL and SES_REGION
                - Uses proper Amplify Gen2 function definition syntax
                
                Please provide the complete TypeScript code for the function resource file.
                """,
                expected_outputs=[
                    """import { defineFunction } from '@aws-amplify/backend';

export const emailSender = defineFunction({
  name: 'email-sender',
  entry: './handler.ts',
  environment: {
    API_URL: 'https://api.example.com',
    SES_REGION: 'us-east-1'
  }
});"""
                ],
                evaluation_criteria=[
                    "Uses defineFunction from @aws-amplify/backend",
                    "Configures name and entry point correctly",
                    "Includes environment variables",
                    "Follows proper naming conventions"
                ],
                difficulty="basic",
                category="functions"
            ),
            
            FunctionalTestCase(
                name="Function with Data Access",
                description="Generate function resource with data access permissions",
                scenario="""
                Generate the code for amplify/functions/data-processor/resource.ts that:
                - Defines a function named 'data-processor'
                - Points to handler.ts as entry point
                - Has access to the data schema for CRUD operations
                - Includes proper data access configuration
                
                Also show how to grant this function access in the data resource.
                """,
                expected_outputs=[
                    """// amplify/functions/data-processor/resource.ts
import { defineFunction } from '@aws-amplify/backend';

export const dataProcessor = defineFunction({
  name: 'data-processor',
  entry: './handler.ts'
});

// In amplify/data/resource.ts - add to schema authorization
const schema = a.schema({
  Todo: a.model({
    content: a.string(),
    done: a.boolean()
  })
}).authorization(allow => [
  allow.resource(dataProcessor)
]);"""
                ],
                evaluation_criteria=[
                    "Defines function resource correctly",
                    "Shows proper data access integration",
                    "Uses allow.resource() authorization",
                    "Demonstrates cross-resource references"
                ],
                difficulty="intermediate",
                category="functions"
            ),
            
            # Backend Integration Tests
            FunctionalTestCase(
                name="Complete Backend Definition",
                description="Generate amplify/backend.ts with all resources",
                scenario="""
                Generate the code for amplify/backend.ts that integrates:
                - Auth resource (imported from ./auth/resource)
                - Data resource (imported from ./data/resource)
                - Storage resource (imported from ./storage/resource)
                - Function resource (imported from ./functions/email-sender/resource)
                
                Please provide the complete TypeScript code for the backend definition file.
                """,
                expected_outputs=[
                    """import { defineBackend } from '@aws-amplify/backend';
import { auth } from './auth/resource';
import { data } from './data/resource';
import { storage } from './storage/resource';
import { emailSender } from './functions/email-sender/resource';

export const backend = defineBackend({
  auth,
  data,
  storage,
  emailSender,
});"""
                ],
                evaluation_criteria=[
                    "Uses defineBackend from @aws-amplify/backend",
                    "Imports all resources correctly",
                    "Includes auth, data, storage, and functions",
                    "Follows proper backend definition pattern"
                ],
                difficulty="basic",
                category="backend"
            ),
            
            # React Integration Tests
            FunctionalTestCase(
                name="React Authentication Hook",
                description="Generate React hook for authentication",
                scenario="""
                Generate a React custom hook called useAuth that:
                - Handles sign in, sign up, and sign out
                - Manages authentication state
                - Provides error handling
                - Uses AWS Amplify Auth APIs
                
                Please provide the complete TypeScript code for the useAuth hook.
                """,
                expected_outputs=[
                    """import { useState, useEffect } from 'react';
import { signIn, signUp, signOut, getCurrentUser } from 'aws-amplify/auth';

export function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkAuthState();
  }, []);

  const checkAuthState = async () => {
    try {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
    } catch (error) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSignIn = async (username: string, password: string) => {
    try {
      setError(null);
      await signIn({ username, password });
      await checkAuthState();
    } catch (error) {
      setError(error.message);
    }
  };

  const handleSignUp = async (username: string, password: string) => {
    try {
      setError(null);
      await signUp({ username, password });
    } catch (error) {
      setError(error.message);
    }
  };

  const handleSignOut = async () => {
    try {
      await signOut();
      setUser(null);
    } catch (error) {
      setError(error.message);
    }
  };

  return {
    user,
    loading,
    error,
    signIn: handleSignIn,
    signUp: handleSignUp,
    signOut: handleSignOut,
  };
}"""
                ],
                evaluation_criteria=[
                    "Uses correct Amplify Auth imports",
                    "Implements proper state management",
                    "Includes error handling",
                    "Provides clean API interface"
                ],
                difficulty="intermediate",
                category="frontend"
            ),
            
            FunctionalTestCase(
                name="GraphQL Data Operations",
                description="Generate React component with GraphQL operations",
                scenario="""
                Generate a React component called TodoList that:
                - Fetches todos using GraphQL
                - Creates new todos
                - Updates todo completion status
                - Deletes todos
                - Uses the Amplify data client
                
                Please provide the complete TypeScript React component code.
                """,
                expected_outputs=[
                    """import React, { useState, useEffect } from 'react';
import { generateClient } from 'aws-amplify/data';
import type { Schema } from '../amplify/data/resource';

const client = generateClient<Schema>();

export function TodoList() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const { data } = await client.models.Todo.list();
      setTodos(data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
  };

  const createTodo = async () => {
    try {
      await client.models.Todo.create({
        content: newTodo,
        done: false,
      });
      setNewTodo('');
      fetchTodos();
    } catch (error) {
      console.error('Error creating todo:', error);
    }
  };

  const updateTodo = async (id: string, done: boolean) => {
    try {
      await client.models.Todo.update({
        id,
        done,
      });
      fetchTodos();
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const deleteTodo = async (id: string) => {
    try {
      await client.models.Todo.delete({ id });
      fetchTodos();
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  return (
    <div>
      <h2>Todo List</h2>
      <div>
        <input
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          placeholder="Enter new todo"
        />
        <button onClick={createTodo}>Add Todo</button>
      </div>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.done}
              onChange={(e) => updateTodo(todo.id, e.target.checked)}
            />
            <span>{todo.content}</span>
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}"""
                ],
                evaluation_criteria=[
                    "Uses generateClient correctly",
                    "Implements CRUD operations properly",
                    "Includes proper error handling",
                    "Uses TypeScript with Schema types"
                ],
                difficulty="intermediate",
                category="frontend"
            )
        ]
    
    def run_functional_test(self, test_case: FunctionalTestCase, mcp_server_name: str) -> TestResult:
        """Run a single functional test case."""
        print(f"  🧪 Running: {test_case.name}")
        print(f"     Category: {test_case.category} | Difficulty: {test_case.difficulty}")
        
        start_time = time.time()
        
        try:
            # This is where you would integrate with the actual LLM + MCP server
            # For now, we'll simulate the test execution
            success, score, outputs, evaluation = self._simulate_test_execution(test_case, mcp_server_name)
            
            duration = time.time() - start_time
            
            result = TestResult(
                test_name=test_case.name,
                success=success,
                score=score,
                duration=duration,
                outputs_generated=outputs,
                evaluation_details=evaluation
            )
            
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"     {status} (Score: {score:.2f}, {duration:.2f}s)")
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = TestResult(
                test_name=test_case.name,
                success=False,
                score=0.0,
                duration=duration,
                outputs_generated=[],
                evaluation_details={},
                error=str(e)
            )
            
            print(f"     ❌ EXCEPTION ({duration:.2f}s): {e}")
            return result
    
    def _simulate_test_execution(self, test_case: FunctionalTestCase, mcp_server_name: str) -> Tuple[bool, float, List[str], Dict[str, Any]]:
        """
        Simulate test execution by generating mock LLM responses and evaluating them.
        In a real implementation, this would:
        1. Send the scenario to an LLM with the MCP server
        2. Evaluate the LLM's response against expected code examples
        3. Score the quality of the generated code/configuration
        """
        
        # Simulate different quality responses based on server type
        server_quality = {
            "amplify-gen2": 0.9,
            "frontend": 0.7,
            "aws-documentation": 0.6,
            "terraform": 0.4,
            "cloudscape": 0.6
        }
        
        server_key = next((k for k in server_quality.keys() if k in mcp_server_name.lower()), "aws-documentation")
        base_quality = server_quality[server_key]
        
        # Adjust quality based on test difficulty
        difficulty_multiplier = {
            "basic": 1.0,
            "intermediate": 0.8,
            "advanced": 0.6
        }
        
        quality_score = base_quality * difficulty_multiplier[test_case.difficulty]
        
        # Simulate test execution time
        import random
        time.sleep(random.uniform(0.1, 0.5))
        
        # Generate mock LLM response based on quality
        generated_code = self._generate_mock_response(test_case, quality_score)
        
        # Evaluate the generated code against expected outputs
        evaluation_results = self._evaluate_generated_code(generated_code, test_case)
        
        success = evaluation_results['overall_score'] >= 0.6
        score = evaluation_results['overall_score']
        
        return success, score, [generated_code], evaluation_results['details']
    
    def _generate_mock_response(self, test_case: FunctionalTestCase, quality_score: float) -> str:
        """Generate a mock LLM response based on the test case and quality score."""
        
        if quality_score >= 0.8:
            # High quality: return the expected output with minor variations
            if test_case.expected_outputs:
                return test_case.expected_outputs[0]
        
        elif quality_score >= 0.6:
            # Medium quality: return partially correct code
            if test_case.category == "auth":
                return """import { defineAuth } from '@aws-amplify/backend';

export const auth = defineAuth({
  loginWith: {
    email: true,
  },
  // Missing some configuration
});"""
            
            elif test_case.category == "data":
                return """import { a, defineData } from '@aws-amplify/backend';

const schema = a.schema({
  Todo: a.model({
    content: a.string(),
    done: a.boolean(),
  }),
});

export const data = defineData({ schema });"""
            
            elif test_case.category == "functions":
                return """import { defineFunction } from '@aws-amplify/backend';

export const myFunction = defineFunction({
  name: 'my-function',
  entry: './handler.ts'
});"""
        
        else:
            # Low quality: return incorrect or incomplete code
            if test_case.category == "auth":
                return """// Incorrect import
import { Auth } from 'aws-amplify';

// Wrong syntax
const auth = Auth.configure({
  email: true
});"""
            
            elif test_case.category == "data":
                return """// Missing imports
const schema = {
  Todo: {
    content: 'string',
    done: 'boolean'
  }
};"""
            
            else:
                return "// Incomplete or incorrect code generated"
        
        return "// No code generated"
    
    def _evaluate_generated_code(self, generated_code: str, test_case: FunctionalTestCase) -> Dict[str, Any]:
        """Evaluate generated code against expected outputs and criteria."""
        
        evaluation_details = {}
        scores = []
        
        # Check each evaluation criterion
        for criterion in test_case.evaluation_criteria:
            score, notes = self._evaluate_criterion(generated_code, criterion, test_case)
            evaluation_details[criterion] = {
                "score": score,
                "notes": notes
            }
            scores.append(score)
        
        # Calculate overall score
        overall_score = sum(scores) / len(scores) if scores else 0.0
        
        return {
            "overall_score": overall_score,
            "details": evaluation_details
        }
    
    def _evaluate_criterion(self, generated_code: str, criterion: str, test_case: FunctionalTestCase) -> Tuple[float, str]:
        """Evaluate a specific criterion against the generated code."""
        
        # Simple keyword-based evaluation (in real implementation, this would be more sophisticated)
        criterion_lower = criterion.lower()
        code_lower = generated_code.lower()
        
        if "defineauth" in criterion_lower:
            if "defineauth" in code_lower and "@aws-amplify/backend" in code_lower:
                return 0.9, "Correctly uses defineAuth from @aws-amplify/backend"
            elif "defineauth" in code_lower:
                return 0.6, "Uses defineAuth but missing proper import"
            else:
                return 0.2, "Does not use defineAuth function"
        
        elif "email login" in criterion_lower:
            if "email: true" in code_lower:
                return 0.9, "Correctly configures email login"
            elif "email" in code_lower:
                return 0.5, "Mentions email but configuration unclear"
            else:
                return 0.1, "No email login configuration found"
        
        elif "user attributes" in criterion_lower:
            if "userattributes" in code_lower and ("given_name" in code_lower or "family_name" in code_lower):
                return 0.9, "Properly configures user attributes"
            elif "userattributes" in code_lower:
                return 0.6, "Has user attributes but incomplete"
            else:
                return 0.2, "Missing user attributes configuration"
        
        elif "amplify gen2 syntax" in criterion_lower:
            if "defineauth" in code_lower or "definedata" in code_lower or "definefunction" in code_lower:
                return 0.9, "Uses proper Amplify Gen2 syntax"
            elif "amplify" in code_lower:
                return 0.4, "References Amplify but may not use Gen2 syntax"
            else:
                return 0.1, "Does not appear to use Amplify Gen2 syntax"
        
        elif "google oauth" in criterion_lower:
            if "google" in code_lower and "clientid" in code_lower:
                return 0.9, "Correctly configures Google OAuth"
            elif "google" in code_lower:
                return 0.5, "Mentions Google but incomplete configuration"
            else:
                return 0.1, "No Google OAuth configuration found"
        
        elif "mfa" in criterion_lower or "multifactor" in criterion_lower:
            if "multifactor" in code_lower and ("sms" in code_lower or "totp" in code_lower):
                return 0.9, "Properly configures MFA with SMS/TOTP"
            elif "multifactor" in code_lower:
                return 0.6, "Has MFA configuration but incomplete"
            else:
                return 0.1, "No MFA configuration found"
        
        elif "a.schema" in criterion_lower or "definedata" in criterion_lower:
            if "a.schema" in code_lower and "definedata" in code_lower:
                return 0.9, "Uses correct schema and data definition"
            elif "schema" in code_lower:
                return 0.5, "Has schema but may not use proper syntax"
            else:
                return 0.2, "Missing proper schema definition"
        
        elif "field types" in criterion_lower:
            type_keywords = ["a.string", "a.boolean", "a.id", "a.datetime"]
            found_types = sum(1 for keyword in type_keywords if keyword in code_lower)
            if found_types >= 3:
                return 0.9, f"Uses proper field types ({found_types} types found)"
            elif found_types >= 1:
                return 0.6, f"Uses some proper field types ({found_types} types found)"
            else:
                return 0.2, "Missing proper field type definitions"
        
        elif "authorization" in criterion_lower:
            if "authorization" in code_lower and ("allow.owner" in code_lower or "allow.authenticated" in code_lower):
                return 0.9, "Implements proper authorization rules"
            elif "authorization" in code_lower:
                return 0.5, "Has authorization but may be incomplete"
            else:
                return 0.2, "Missing authorization configuration"
        
        elif "definefunction" in criterion_lower:
            if "definefunction" in code_lower and "@aws-amplify/backend" in code_lower:
                return 0.9, "Correctly uses defineFunction"
            elif "definefunction" in code_lower:
                return 0.6, "Uses defineFunction but missing proper import"
            else:
                return 0.2, "Does not use defineFunction"
        
        elif "environment variables" in criterion_lower:
            if "environment" in code_lower and ":" in generated_code:
                return 0.9, "Properly configures environment variables"
            elif "environment" in code_lower:
                return 0.5, "Mentions environment but configuration unclear"
            else:
                return 0.2, "No environment variables configuration"
        
        elif "generateclient" in criterion_lower:
            if "generateclient" in code_lower and "aws-amplify/data" in code_lower:
                return 0.9, "Correctly uses generateClient"
            elif "generateclient" in code_lower:
                return 0.6, "Uses generateClient but missing proper import"
            else:
                return 0.2, "Does not use generateClient"
        
        elif "crud operations" in criterion_lower:
            crud_keywords = ["create", "list", "update", "delete"]
            found_crud = sum(1 for keyword in crud_keywords if keyword in code_lower)
            if found_crud >= 3:
                return 0.9, f"Implements CRUD operations ({found_crud} operations found)"
            elif found_crud >= 1:
                return 0.6, f"Implements some CRUD operations ({found_crud} operations found)"
            else:
                return 0.2, "Missing CRUD operations"
        
        elif "error handling" in criterion_lower:
            if "try" in code_lower and "catch" in code_lower:
                return 0.9, "Includes proper error handling with try/catch"
            elif "error" in code_lower:
                return 0.5, "Mentions error handling but may be incomplete"
            else:
                return 0.2, "No error handling found"
        
        # Default evaluation for unrecognized criteria
        return 0.5, f"Criterion '{criterion}' evaluated with default scoring"
    
    def run_tests_for_server(self, server_name: str, categories: Optional[List[str]] = None, difficulties: Optional[List[str]] = None) -> List[TestResult]:
        """Run functional tests for a specific server with optional filtering."""
        
        print(f"\n🎯 Running Functional Tests for: {server_name}")
        print("=" * 60)
        
        # Filter test cases
        filtered_tests = self.test_cases
        
        if categories:
            filtered_tests = [t for t in filtered_tests if t.category in categories]
        
        if difficulties:
            filtered_tests = [t for t in filtered_tests if t.difficulty in difficulties]
        
        print(f"Running {len(filtered_tests)} functional test cases...")
        
        results = []
        for test_case in filtered_tests:
            result = self.run_functional_test(test_case, server_name)
            results.append(result)
            self.results.append(result)
        
        return results
    
    def print_detailed_results(self, results: List[TestResult]) -> None:
        """Print detailed results for a set of tests."""
        
        if not results:
            print("\n📊 No test results to display")
            return
        
        print("\n" + "=" * 80)
        print("📊 FUNCTIONAL TEST RESULTS")
        print("=" * 80)
        
        # Overall statistics
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.success)
        avg_score = sum(r.score for r in results) / total_tests if total_tests > 0 else 0
        total_duration = sum(r.duration for r in results)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {total_tests - passed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Average Score: {avg_score:.2f}/1.00")
        print(f"Total Duration: {total_duration:.2f}s")
        
        # Results by category
        categories = {}
        for result in results:
            # Find the test case to get category
            test_case = next((tc for tc in self.test_cases if tc.name == result.test_name), None)
            if test_case:
                category = test_case.category
                if category not in categories:
                    categories[category] = []
                categories[category].append(result)
        
        for category, cat_results in categories.items():
            cat_passed = sum(1 for r in cat_results if r.success)
            cat_avg_score = sum(r.score for r in cat_results) / len(cat_results)
            
            print(f"\n📋 {category.upper()} Category:")
            print(f"   Tests: {len(cat_results)}, Passed: {cat_passed}, Avg Score: {cat_avg_score:.2f}")
            
            for result in cat_results:
                status = "✅" if result.success else "❌"
                print(f"   {status} {result.test_name} (Score: {result.score:.2f}, {result.duration:.2f}s)")
                
                if result.error:
                    print(f"      Error: {result.error}")
                
                # Show evaluation details for failed tests
                if not result.success and result.evaluation_details:
                    print(f"      Evaluation Issues:")
                    for criterion, details in result.evaluation_details.items():
                        if details['score'] < 0.5:
                            print(f"        - {criterion}: {details['notes']}")
        
        print("\n" + "=" * 80)
    
    def generate_report(self, output_file: str = "amplify_functional_test_report.json") -> None:
        """Generate a detailed JSON report of all test results."""
        
        report = {
            "test_run_timestamp": time.time(),
            "total_tests": len(self.results),
            "passed_tests": sum(1 for r in self.results if r.success),
            "average_score": sum(r.score for r in self.results) / len(self.results) if self.results else 0,
            "results": []
        }
        
        for result in self.results:
            test_case = next((tc for tc in self.test_cases if tc.name == result.test_name), None)
            
            result_data = {
                "test_name": result.test_name,
                "category": test_case.category if test_case else "unknown",
                "difficulty": test_case.difficulty if test_case else "unknown",
                "success": result.success,
                "score": result.score,
                "duration": result.duration,
                "outputs_generated": result.outputs_generated,
                "evaluation_details": result.evaluation_details,
                "error": result.error
            }
            
            report["results"].append(result_data)
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {output_file}")


def main():
    """Main entry point for functional testing."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Amplify Gen2 Functional Test Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python amplify_functional_tests.py --server amplify-gen2 --category auth
  python amplify_functional_tests.py --server frontend --difficulty basic
  python amplify_functional_tests.py --server aws-docs --all
        """
    )
    
    parser.add_argument('--server', required=True, help='MCP server name to test')
    parser.add_argument('--category', choices=['auth', 'data', 'storage', 'hosting', 'functions', 'integration'], 
                       help='Test specific category only')
    parser.add_argument('--difficulty', choices=['basic', 'intermediate', 'advanced'], 
                       help='Test specific difficulty level only')
    parser.add_argument('--all', action='store_true', help='Run all functional tests')
    parser.add_argument('--report', help='Generate JSON report to specified file')
    
    args = parser.parse_args()
    
    runner = AmplifyFunctionalTestRunner()
    
    categories = [args.category] if args.category else None
    difficulties = [args.difficulty] if args.difficulty else None
    
    results = runner.run_tests_for_server(args.server, categories, difficulties)
    runner.print_detailed_results(results)
    
    if args.report:
        runner.generate_report(args.report)


if __name__ == "__main__":
    main()
