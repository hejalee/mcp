#!/usr/bin/env python3
"""
Test script to verify if the amplify-gen2-mcp-server can find the specific 
custom Python function code example when searching for custom Python functions.

The target code example includes:
- defineFunction usage
- Docker bundling for Go/Python functions
- Custom runtime (PROVIDED_AL2023)
- Resource group configuration
"""

import sys
import os
import json
import re

# Add the current directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from awslabs.amplify_gen2_mcp_server.tools import (
        search_amplify_gen2_documentation,
        search_sample_repositories,
        get_amplify_gen2_guidance,
        search_amplify_documentation,
        fetch_raw_content,
        fetch_github_content
    )
    from awslabs.amplify_gen2_mcp_server.consts import SAMPLE_REPOSITORIES, DOCUMENTATION_REPO
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running this from the amplify-gen2-mcp-server directory")
    sys.exit(1)

# Target code patterns to search for
TARGET_CODE_PATTERNS = [
    "defineFunction",
    "Runtime.PROVIDED_AL2023", 
    "DockerImage.fromRegistry",
    "execSync",
    "GOARCH=amd64 GOOS=linux",
    "bootstrap",
    "resourceGroupName",
    "Code.fromAsset",
    "bundling"
]

def test_search_for_custom_python_functions():
    """Test various search queries to find the custom Python function code example."""
    
    print("=" * 80)
    print("TESTING: Custom Python Functions Code Example Search")
    print("=" * 80)
    
    # Test queries that should find the code example
    test_queries = [
        "custom python functions",
        "defineFunction python",
        "custom runtime functions",
        "docker bundling functions",
        "PROVIDED_AL2023",
        "go build lambda functions",
        "custom functions docker",
        "amplify custom runtime",
        "bootstrap lambda function",
        "resourceGroupName functions"
    ]
    
    results_summary = {}
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"TESTING QUERY: '{query}'")
        print(f"{'='*60}")
        
        # Test 1: Search documentation
        print(f"\n1. Searching documentation for: '{query}'")
        doc_results = search_amplify_documentation(query, limit=5)
        
        doc_matches = 0
        if doc_results:
            print(f"   Found {len(doc_results)} documentation results")
            for i, result in enumerate(doc_results[:3], 1):
                print(f"   {i}. {result.get('title', 'No title')}")
                print(f"      URL: {result.get('url', 'No URL')}")
                
                # Check if we can fetch content and find target patterns
                if 'raw_url' in result:
                    content = fetch_raw_content(result['raw_url'])
                    if content:
                        matches = check_content_for_patterns(content, TARGET_CODE_PATTERNS)
                        if matches:
                            doc_matches += len(matches)
                            print(f"      ✅ Found {len(matches)} target patterns: {matches}")
                        else:
                            print(f"      ❌ No target patterns found")
        else:
            print("   No documentation results found")
        
        # Test 2: Search sample repositories
        print(f"\n2. Searching sample repositories for: '{query}'")
        sample_results = search_sample_repositories(query)
        
        sample_matches = 0
        if sample_results:
            print(f"   Found {len(sample_results)} sample results")
            for i, result in enumerate(sample_results[:3], 1):
                print(f"   {i}. {result.get('title', 'No title')}")
                print(f"      Repository: {result.get('repository', 'No repo')}")
                print(f"      Path: {result.get('path', 'No path')}")
                
                # Check if we can fetch content and find target patterns
                if 'raw_url' in result:
                    content = fetch_raw_content(result['raw_url'])
                    if content:
                        matches = check_content_for_patterns(content, TARGET_CODE_PATTERNS)
                        if matches:
                            sample_matches += len(matches)
                            print(f"      ✅ Found {len(matches)} target patterns: {matches}")
                        else:
                            print(f"      ❌ No target patterns found")
        else:
            print("   No sample repository results found")
        
        # Test 3: Get guidance
        print(f"\n3. Getting guidance for: '{query}'")
        try:
            guidance = get_amplify_gen2_guidance(None, query)
            guidance_matches = check_content_for_patterns(guidance, TARGET_CODE_PATTERNS)
            if guidance_matches:
                print(f"   ✅ Guidance contains {len(guidance_matches)} target patterns: {guidance_matches}")
            else:
                print(f"   ❌ Guidance doesn't contain target patterns")
        except Exception as e:
            print(f"   ❌ Error getting guidance: {e}")
            guidance_matches = []
        
        # Store results
        results_summary[query] = {
            'doc_matches': doc_matches,
            'sample_matches': sample_matches,
            'guidance_matches': len(guidance_matches) if guidance_matches else 0,
            'total_matches': doc_matches + sample_matches + len(guidance_matches if guidance_matches else [])
        }
    
    return results_summary

def check_content_for_patterns(content: str, patterns: list) -> list:
    """Check if content contains any of the target patterns."""
    if not content:
        return []
    
    found_patterns = []
    content_lower = content.lower()
    
    for pattern in patterns:
        # Case-insensitive search for most patterns
        if pattern.lower() in content_lower:
            found_patterns.append(pattern)
        # Also check for exact case matches for code-specific patterns
        elif pattern in content:
            found_patterns.append(pattern)
    
    return found_patterns

def test_direct_repository_search():
    """Directly search known repositories for the target code example."""
    
    print(f"\n{'='*80}")
    print("TESTING: Direct Repository Search")
    print(f"{'='*80}")
    
    # Search through all sample repositories
    for framework, repo in SAMPLE_REPOSITORIES.items():
        print(f"\n--- Searching {framework.upper()} repository: {repo} ---")
        
        # Common paths where custom functions might be found
        search_paths = [
            "amplify/functions",
            "amplify/backend",
            "src/amplify",
            "examples",
            "samples",
            "functions"
        ]
        
        for search_path in search_paths:
            try:
                # This is a simplified search - in reality we'd need to traverse the repo structure
                print(f"   Checking path: {search_path}")
                # Note: This would require implementing repository tree traversal
                # For now, we'll just note that this is where we'd search
            except Exception as e:
                print(f"   Error searching {search_path}: {e}")

def test_specific_documentation_paths():
    """Test specific documentation paths that might contain the code example."""
    
    print(f"\n{'='*80}")
    print("TESTING: Specific Documentation Paths")
    print(f"{'='*80}")
    
    # Specific paths that might contain custom function examples
    test_paths = [
        "src/pages/nextjs/build-a-backend/functions/custom-functions/index.mdx",
        "src/pages/react/build-a-backend/functions/custom-functions/index.mdx",
        "src/pages/nextjs/build-a-backend/functions/index.mdx",
        "src/pages/nextjs/build-a-backend/functions/configure-functions/index.mdx",
        "src/pages/gen2/nextjs/build-a-backend/functions/custom-functions/index.mdx"
    ]
    
    for path in test_paths:
        print(f"\n--- Testing path: {path} ---")
        try:
            content = fetch_github_content(DOCUMENTATION_REPO, path)
            if content:
                matches = check_content_for_patterns(content, TARGET_CODE_PATTERNS)
                if matches:
                    print(f"   ✅ Found {len(matches)} target patterns: {matches}")
                    print(f"   Content length: {len(content)} characters")
                    
                    # Show a snippet of the content around matches
                    for pattern in matches[:2]:  # Show first 2 matches
                        pattern_index = content.lower().find(pattern.lower())
                        if pattern_index != -1:
                            start = max(0, pattern_index - 100)
                            end = min(len(content), pattern_index + 200)
                            snippet = content[start:end].replace('\n', ' ')
                            print(f"   Snippet around '{pattern}': ...{snippet}...")
                else:
                    print(f"   ❌ No target patterns found (content length: {len(content)})")
            else:
                print(f"   ❌ Could not fetch content from path")
        except Exception as e:
            print(f"   ❌ Error fetching {path}: {e}")

def print_results_summary(results_summary):
    """Print a summary of all test results."""
    
    print(f"\n{'='*80}")
    print("RESULTS SUMMARY")
    print(f"{'='*80}")
    
    total_queries = len(results_summary)
    queries_with_matches = sum(1 for r in results_summary.values() if r['total_matches'] > 0)
    
    print(f"Total queries tested: {total_queries}")
    print(f"Queries with matches: {queries_with_matches}")
    print(f"Success rate: {(queries_with_matches/total_queries)*100:.1f}%")
    
    print(f"\nDetailed Results:")
    print(f"{'Query':<25} {'Doc':<5} {'Sample':<7} {'Guide':<7} {'Total':<7}")
    print("-" * 55)
    
    for query, results in results_summary.items():
        print(f"{query:<25} {results['doc_matches']:<5} {results['sample_matches']:<7} {results['guidance_matches']:<7} {results['total_matches']:<7}")
    
    # Recommendations
    print(f"\n{'='*80}")
    print("RECOMMENDATIONS")
    print(f"{'='*80}")
    
    if queries_with_matches == 0:
        print("❌ NO MATCHES FOUND - The target code example is not discoverable")
        print("\nRecommended actions:")
        print("1. Add the code example to official documentation")
        print("2. Include it in sample repositories")
        print("3. Update search indexing to include custom runtime examples")
        print("4. Add specific documentation for Go/Python custom functions")
    elif queries_with_matches < total_queries / 2:
        print("⚠️  LIMITED DISCOVERABILITY - Some queries find the code, others don't")
        print("\nRecommended actions:")
        print("1. Improve search relevance scoring")
        print("2. Add more comprehensive examples")
        print("3. Cross-reference related documentation")
    else:
        print("✅ GOOD DISCOVERABILITY - Most queries can find the target code")
        print("\nOptional improvements:")
        print("1. Ensure all query variations work")
        print("2. Add more detailed explanations")

def main():
    """Run all tests."""
    print("Starting Custom Python Functions Code Example Search Test")
    print(f"Target patterns: {TARGET_CODE_PATTERNS}")
    
    # Run the main search tests
    results_summary = test_search_for_custom_python_functions()
    
    # Run direct repository search
    test_direct_repository_search()
    
    # Test specific documentation paths
    test_specific_documentation_paths()
    
    # Print summary
    print_results_summary(results_summary)

if __name__ == "__main__":
    main()
