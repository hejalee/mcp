#!/usr/bin/env python3
"""Demo script showing the enhanced sample repository features."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from awslabs.amplify_gen2_mcp_server.tools import (
    search_amplify_gen2_documentation,
    discover_amplify_project_templates
)

def demo_documentation_search():
    """Demo the enhanced documentation search with sample repositories."""
    print("🔍 DEMO: Enhanced Documentation Search")
    print("=" * 60)
    
    # Search for authentication - should find both docs and sample code
    result = search_amplify_gen2_documentation(None, "authentication", limit=3)
    
    print("Search Query: 'authentication'")
    print("-" * 30)
    
    # Extract and display key information
    lines = result.split('\n')
    
    # Find documentation results
    in_docs = False
    in_examples = False
    doc_count = 0
    example_count = 0
    
    for line in lines:
        if line.startswith('**Found:**'):
            print(f"📊 {line}")
        elif line.startswith('## Official Documentation'):
            in_docs = True
            in_examples = False
            print(f"\n📚 {line}")
        elif line.startswith('## Code Examples'):
            in_docs = False
            in_examples = True
            print(f"\n💻 {line}")
        elif in_docs and line.startswith('### '):
            doc_count += 1
            if doc_count <= 2:
                print(f"  {line}")
        elif in_examples and line.startswith('### '):
            example_count += 1
            if example_count <= 3:
                print(f"  {line}")
        elif (in_docs or in_examples) and line.startswith('**URL:**') and (doc_count <= 2 or example_count <= 3):
            print(f"  {line}")

def demo_template_discovery():
    """Demo the project template discovery feature."""
    print("\n\n🚀 DEMO: Project Template Discovery")
    print("=" * 60)
    
    # Show all available templates
    result = discover_amplify_project_templates(None)
    
    print("Available Amplify Gen2 Project Templates:")
    print("-" * 40)
    
    # Extract template information
    lines = result.split('\n')
    
    current_template = None
    for line in lines:
        if line.startswith('## ') and 'Template' in line:
            current_template = line.replace('## ', '').replace(' Template', '')
            print(f"\n🎯 {current_template}")
        elif line.startswith('**Repository:**'):
            repo_info = line.replace('**Repository:** [', '').replace('](', ' - ').replace(')', '')
            print(f"   📁 {repo_info}")
        elif line.startswith('**Key Features:**'):
            features = line.replace('**Key Features:** ', '')
            print(f"   ✨ {features}")
        elif line.startswith('### Available Files ('):
            file_count = line.replace('### Available Files (', '').replace(')', '')
            print(f"   📄 Files: {file_count}")

def demo_framework_specific():
    """Demo framework-specific template discovery."""
    print("\n\n🎯 DEMO: Framework-Specific Templates")
    print("=" * 60)
    
    frameworks = ['react', 'next', 'vue']
    
    for framework in frameworks:
        print(f"\n🔍 {framework.upper()} Template:")
        print("-" * 20)
        
        result = discover_amplify_project_templates(None, framework)
        
        # Extract key information
        lines = result.split('\n')
        
        for line in lines:
            if line.startswith('**Repository:**'):
                repo_info = line.replace('**Repository:** [', '').replace('](', ' - ').replace(')', '')
                print(f"  📁 {repo_info}")
            elif line.startswith('**Key Features:**'):
                features = line.replace('**Key Features:** ', '')
                print(f"  ✨ {features}")
                break

def demo_quick_start_info():
    """Demo the quick start information extraction."""
    print("\n\n⚡ DEMO: Quick Start Information")
    print("=" * 60)
    
    # Get React template info
    result = discover_amplify_project_templates(None, "react")
    
    print("React Template Quick Start:")
    print("-" * 30)
    
    lines = result.split('\n')
    in_quick_start = False
    
    for line in lines:
        if line.startswith('### Quick Start'):
            in_quick_start = True
            print("📋 Setup Commands:")
        elif in_quick_start and line.startswith('```bash'):
            continue
        elif in_quick_start and line.startswith('```'):
            break
        elif in_quick_start and line.startswith('#'):
            print(f"  {line}")
        elif in_quick_start and line.strip() and not line.startswith('**'):
            print(f"  {line}")

def main():
    """Run all demos."""
    print("🎉 AMPLIFY GEN2 MCP SERVER - ENHANCED FEATURES DEMO")
    print("=" * 70)
    print("This demo shows the enhanced sample repository features that help")
    print("developers find project templates and reduce setup time.")
    print("=" * 70)
    
    try:
        demo_documentation_search()
        demo_template_discovery()
        demo_framework_specific()
        demo_quick_start_info()
        
        print("\n\n🎊 DEMO COMPLETE!")
        print("=" * 60)
        print("✅ Enhanced documentation search with sample code")
        print("✅ Project template discovery across all frameworks")
        print("✅ Framework-specific template filtering")
        print("✅ Quick start instructions for rapid development")
        print("✅ Direct links to all AWS sample repositories")
        print("\n🚀 Ready to help developers get started faster with Amplify Gen2!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
