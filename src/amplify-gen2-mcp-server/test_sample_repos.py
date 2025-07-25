#!/usr/bin/env python3
"""Test script to explore what we're finding in the sample repositories."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from awslabs.amplify_gen2_mcp_server.tools import (
    search_sample_repositories,
    fetch_github_content,
    SAMPLE_REPOSITORIES
)

def test_sample_repo_structure():
    """Test what we can find in each sample repository."""
    print("🔍 Exploring Sample Repository Structure")
    print("=" * 50)
    
    for framework, repo in SAMPLE_REPOSITORIES.items():
        print(f"\n📁 {framework.upper()} - {repo}")
        print("-" * 40)
        
        # Search for common project files
        common_queries = ["package.json", "README", "amplify", "auth", "data"]
        
        for query in common_queries:
            try:
                results = search_sample_repositories(query, framework)
                framework_results = [r for r in results if r['framework'] == framework]
                
                if framework_results:
                    print(f"  🔎 '{query}' found {len(framework_results)} files:")
                    for result in framework_results[:3]:  # Show first 3
                        print(f"    - {result['path']}")
                else:
                    print(f"  🔎 '{query}' - no results")
            except Exception as e:
                print(f"  ❌ Error searching for '{query}': {e}")

def test_project_template_discovery():
    """Test discovering project templates and starter files."""
    print("\n\n🚀 Project Template Discovery")
    print("=" * 50)
    
    for framework, repo in SAMPLE_REPOSITORIES.items():
        print(f"\n📋 {framework.upper()} Template Analysis")
        print("-" * 30)
        
        # Look for key project files
        key_files = ["package.json", "README.md", "amplify/backend.ts", "amplify/auth/resource.ts"]
        
        for file_path in key_files:
            try:
                content = fetch_github_content(repo, file_path)
                if content:
                    print(f"  ✅ {file_path} - {len(content)} chars")
                    # Show first few lines for package.json and README
                    if file_path in ["package.json", "README.md"]:
                        lines = content.split('\n')[:5]
                        for line in lines:
                            if line.strip():
                                print(f"    {line[:60]}...")
                                break
                else:
                    print(f"  ❌ {file_path} - not found")
            except Exception as e:
                print(f"  ❌ {file_path} - error: {e}")

def main():
    """Run all tests."""
    test_sample_repo_structure()
    test_project_template_discovery()
    print("\n✅ Sample repository exploration completed!")

if __name__ == "__main__":
    main()
