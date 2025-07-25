#!/usr/bin/env python3
"""Test the enhanced sample repository functionality."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from awslabs.amplify_gen2_mcp_server.tools import (
    discover_project_templates,
    discover_amplify_project_templates,
    search_sample_repositories
)

def test_template_discovery():
    """Test the project template discovery functionality."""
    print("🚀 Testing Project Template Discovery")
    print("=" * 50)
    
    try:
        templates = discover_project_templates()
        
        print(f"Found {len(templates)} templates:")
        for framework, template_info in templates.items():
            print(f"\n📋 {framework.upper()}")
            print(f"  Repository: {template_info['repository']}")
            print(f"  Available files: {len(template_info['available_files'])}")
            print(f"  Key features: {', '.join(template_info['key_features']) if template_info['key_features'] else 'None detected'}")
            
            # Show some key files
            key_files = ['package.json', 'README.md', 'amplify/backend.ts']
            for file_path in key_files:
                if file_path in template_info['available_files']:
                    file_info = template_info['available_files'][file_path]
                    print(f"    ✅ {file_path} ({file_info['size']} bytes)")
                else:
                    print(f"    ❌ {file_path}")
        
        return len(templates) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_framework_specific_discovery():
    """Test framework-specific template discovery."""
    print("\n\n🎯 Testing Framework-Specific Discovery")
    print("=" * 50)
    
    frameworks = ['react', 'next', 'vue']
    success_count = 0
    
    for framework in frameworks:
        print(f"\n🔍 Testing {framework.upper()} template...")
        try:
            templates = discover_project_templates(framework)
            
            if framework in templates:
                template = templates[framework]
                print(f"  ✅ Found {framework} template")
                print(f"  📁 Files: {len(template['available_files'])}")
                print(f"  🎨 Features: {', '.join(template['key_features'])}")
                success_count += 1
            else:
                print(f"  ❌ No {framework} template found")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    return success_count == len(frameworks)

def test_mcp_tool():
    """Test the MCP tool function."""
    print("\n\n🛠️ Testing MCP Tool Function")
    print("=" * 50)
    
    try:
        result = discover_amplify_project_templates(None, "react")
        
        print("MCP Tool Result Preview:")
        print(result[:500] + "..." if len(result) > 500 else result)
        
        return "Amplify Gen2 Project Templates" in result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_enhanced_search():
    """Test the enhanced sample repository search."""
    print("\n\n🔎 Testing Enhanced Sample Search")
    print("=" * 50)
    
    queries = ["package", "amplify", "auth", "react"]
    success_count = 0
    
    for query in queries:
        print(f"\n🔍 Searching for '{query}'...")
        try:
            results = search_sample_repositories(query)
            print(f"  Found {len(results)} results")
            
            if len(results) > 0:
                success_count += 1
                for result in results[:2]:  # Show first 2
                    print(f"    - {result['framework']}: {result['path']} (score: {result['relevance_score']:.1f})")
            else:
                print("  No results found")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    return success_count >= 3  # At least 3 out of 4 queries should return results

def main():
    """Run all tests."""
    print("🚀 Starting Enhanced Sample Repository Tests\n")
    
    tests = [
        ("Template Discovery", test_template_discovery),
        ("Framework-Specific Discovery", test_framework_specific_discovery),
        ("MCP Tool Function", test_mcp_tool),
        ("Enhanced Search", test_enhanced_search)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All enhanced sample repository features working!")
        return 0
    else:
        print("⚠️ Some features need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())
