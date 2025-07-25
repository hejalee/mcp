#!/usr/bin/env python3
"""Test just the search functionality that we know works."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from awslabs.amplify_gen2_mcp_server.tools import search_amplify_gen2_documentation

def main():
    """Test the search functionality."""
    print("🔍 Testing Amplify Gen2 Documentation Search")
    print("=" * 50)
    
    # Test different search queries
    queries = [
        "authentication",
        "data modeling", 
        "storage",
        "deployment",
        "react"
    ]
    
    for query in queries:
        print(f"\n🔎 Searching for: '{query}'")
        print("-" * 30)
        
        try:
            result = search_amplify_gen2_documentation(None, query, limit=3)
            
            # Extract key information from the result
            lines = result.split('\n')
            found_line = [line for line in lines if line.startswith('**Found:**')]
            if found_line:
                print(found_line[0])
            
            # Show first few documentation results
            in_docs_section = False
            doc_count = 0
            for line in lines:
                if line.startswith('## Official Documentation'):
                    in_docs_section = True
                    continue
                elif line.startswith('## Code Examples'):
                    break
                elif in_docs_section and line.startswith('### '):
                    doc_count += 1
                    if doc_count <= 2:  # Show first 2 results
                        print(f"  {line}")
                elif in_docs_section and line.startswith('**URL:**') and doc_count <= 2:
                    print(f"  {line}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n✅ Search functionality test completed!")

if __name__ == "__main__":
    main()
