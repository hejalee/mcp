#!/usr/bin/env python3
"""
Enhanced AWS Strands Test Script for MCP Servers

This enhanced version includes both technical server tests and functional
LLM evaluation tests for Amplify Gen2 development scenarios.
"""

import json
import os
import sys
import subprocess
import time
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

# Import the original test runner
from aws_strands_test import AWSStrandsTestRunner, TestResult as TechnicalTestResult

# Import the functional test runner
from amplify_functional_tests import AmplifyFunctionalTestRunner, TestResult as FunctionalTestResult


class EnhancedAWSStrandsTestRunner:
    """Enhanced test runner that combines technical and functional testing."""
    
    def __init__(self, mcp_config_path: str = "/Users/hejalee/.aws/amazonq/mcp.json.backup"):
        """Initialize the enhanced test runner."""
        self.technical_runner = AWSStrandsTestRunner(mcp_config_path)
        self.functional_runner = AmplifyFunctionalTestRunner()
        self.all_results = []
    
    def run_comprehensive_tests(self, server_name: str, test_types: List[str] = None) -> Dict[str, Any]:
        """
        Run comprehensive tests for a server including both technical and functional tests.
        
        Args:
            server_name: Name of the MCP server to test
            test_types: List of test types to run ['technical', 'functional', 'basic', 'intermediate', 'advanced']
        """
        
        if test_types is None:
            test_types = ['technical', 'functional']
        
        results = {
            'server_name': server_name,
            'technical_results': [],
            'functional_results': [],
            'summary': {}
        }
        
        print(f"\n🚀 Comprehensive Testing: {server_name}")
        print("=" * 80)
        
        # Run technical tests
        if 'technical' in test_types:
            print("\n🔧 TECHNICAL TESTS")
            print("-" * 40)
            technical_results = self.technical_runner.run_tests_for_server(server_name)
            results['technical_results'] = technical_results
        
        # Run functional tests
        if any(t in test_types for t in ['functional', 'basic', 'intermediate', 'advanced']):
            print("\n🎯 FUNCTIONAL TESTS")
            print("-" * 40)
            
            # Filter by difficulty if specified
            difficulties = []
            if 'basic' in test_types:
                difficulties.append('basic')
            if 'intermediate' in test_types:
                difficulties.append('intermediate')
            if 'advanced' in test_types:
                difficulties.append('advanced')
            
            # If no specific difficulty, run all
            if not difficulties and 'functional' in test_types:
                difficulties = None
            
            functional_results = self.functional_runner.run_tests_for_server(
                server_name, 
                categories=None, 
                difficulties=difficulties
            )
            results['functional_results'] = functional_results
        
        # Generate summary
        results['summary'] = self._generate_summary(results)
        
        return results
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive summary of all test results."""
        
        summary = {
            'technical': {
                'total': 0,
                'passed': 0,
                'success_rate': 0.0,
                'avg_duration': 0.0
            },
            'functional': {
                'total': 0,
                'passed': 0,
                'success_rate': 0.0,
                'avg_score': 0.0,
                'avg_duration': 0.0
            },
            'overall': {
                'total_tests': 0,
                'total_passed': 0,
                'overall_success_rate': 0.0,
                'recommendation': ''
            }
        }
        
        # Technical summary
        tech_results = results.get('technical_results', [])
        if tech_results:
            summary['technical']['total'] = len(tech_results)
            summary['technical']['passed'] = sum(1 for r in tech_results if r.success)
            summary['technical']['success_rate'] = summary['technical']['passed'] / summary['technical']['total']
            summary['technical']['avg_duration'] = sum(r.duration for r in tech_results) / len(tech_results)
        
        # Functional summary
        func_results = results.get('functional_results', [])
        if func_results:
            summary['functional']['total'] = len(func_results)
            summary['functional']['passed'] = sum(1 for r in func_results if r.success)
            summary['functional']['success_rate'] = summary['functional']['passed'] / summary['functional']['total']
            summary['functional']['avg_score'] = sum(r.score for r in func_results) / len(func_results)
            summary['functional']['avg_duration'] = sum(r.duration for r in func_results) / len(func_results)
        
        # Overall summary
        summary['overall']['total_tests'] = summary['technical']['total'] + summary['functional']['total']
        summary['overall']['total_passed'] = summary['technical']['passed'] + summary['functional']['passed']
        
        if summary['overall']['total_tests'] > 0:
            summary['overall']['overall_success_rate'] = summary['overall']['total_passed'] / summary['overall']['total_tests']
        
        # Generate recommendation
        summary['overall']['recommendation'] = self._generate_recommendation(summary)
        
        return summary
    
    def _generate_recommendation(self, summary: Dict[str, Any]) -> str:
        """Generate a recommendation based on test results."""
        
        tech_rate = summary['technical']['success_rate']
        func_rate = summary['functional']['success_rate']
        func_score = summary['functional']['avg_score']
        overall_rate = summary['overall']['overall_success_rate']
        
        if overall_rate >= 0.9:
            return "🌟 EXCELLENT: This MCP server is highly effective for Amplify Gen2 development"
        elif overall_rate >= 0.7:
            if func_score >= 0.8:
                return "✅ GOOD: This MCP server works well for most Amplify Gen2 tasks"
            else:
                return "⚠️ FAIR: Server works but may need guidance for complex tasks"
        elif overall_rate >= 0.5:
            return "🔄 NEEDS IMPROVEMENT: Consider using with additional documentation or examples"
        else:
            return "❌ NOT RECOMMENDED: This server may not be suitable for Amplify Gen2 development"
    
    def print_comprehensive_summary(self, results: Dict[str, Any]) -> None:
        """Print a comprehensive summary of all test results."""
        
        summary = results['summary']
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        
        print(f"Server: {results['server_name']}")
        print()
        
        # Technical Tests Summary
        if summary['technical']['total'] > 0:
            print("🔧 Technical Tests:")
            print(f"   Total: {summary['technical']['total']}")
            print(f"   Passed: {summary['technical']['passed']}")
            print(f"   Success Rate: {summary['technical']['success_rate']:.1%}")
            print(f"   Avg Duration: {summary['technical']['avg_duration']:.2f}s")
            print()
        
        # Functional Tests Summary
        if summary['functional']['total'] > 0:
            print("🎯 Functional Tests:")
            print(f"   Total: {summary['functional']['total']}")
            print(f"   Passed: {summary['functional']['passed']}")
            print(f"   Success Rate: {summary['functional']['success_rate']:.1%}")
            print(f"   Avg Score: {summary['functional']['avg_score']:.2f}/1.00")
            print(f"   Avg Duration: {summary['functional']['avg_duration']:.2f}s")
            print()
        
        # Overall Summary
        print("🎖️ Overall Assessment:")
        print(f"   Total Tests: {summary['overall']['total_tests']}")
        print(f"   Total Passed: {summary['overall']['total_passed']}")
        print(f"   Overall Success Rate: {summary['overall']['overall_success_rate']:.1%}")
        print()
        print(f"📋 Recommendation: {summary['overall']['recommendation']}")
        
        print("\n" + "=" * 80)
    
    def run_server_comparison(self, server_names: List[str], test_types: List[str] = None) -> Dict[str, Any]:
        """Run tests on multiple servers and compare results."""
        
        print(f"\n🏆 SERVER COMPARISON")
        print("=" * 80)
        print(f"Testing {len(server_names)} servers: {', '.join(server_names)}")
        
        comparison_results = {
            'servers': {},
            'rankings': {}
        }
        
        # Test each server
        for server_name in server_names:
            results = self.run_comprehensive_tests(server_name, test_types)
            comparison_results['servers'][server_name] = results
        
        # Generate rankings
        comparison_results['rankings'] = self._generate_rankings(comparison_results['servers'])
        
        # Print comparison summary
        self._print_comparison_summary(comparison_results)
        
        return comparison_results
    
    def _generate_rankings(self, server_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate rankings based on test results."""
        
        rankings = {
            'by_overall_success': [],
            'by_functional_score': [],
            'by_technical_success': [],
            'recommendations': {}
        }
        
        # Collect data for ranking
        server_data = []
        for server_name, results in server_results.items():
            summary = results['summary']
            server_data.append({
                'name': server_name,
                'overall_success': summary['overall']['overall_success_rate'],
                'functional_score': summary['functional']['avg_score'],
                'technical_success': summary['technical']['success_rate'],
                'recommendation': summary['overall']['recommendation']
            })
        
        # Sort by different criteria
        rankings['by_overall_success'] = sorted(server_data, key=lambda x: x['overall_success'], reverse=True)
        rankings['by_functional_score'] = sorted(server_data, key=lambda x: x['functional_score'], reverse=True)
        rankings['by_technical_success'] = sorted(server_data, key=lambda x: x['technical_success'], reverse=True)
        
        # Generate use case recommendations
        rankings['recommendations'] = {
            'best_overall': rankings['by_overall_success'][0]['name'] if server_data else None,
            'best_for_beginners': next((s['name'] for s in rankings['by_functional_score'] if 'EXCELLENT' in s['recommendation'] or 'GOOD' in s['recommendation']), None),
            'most_reliable': rankings['by_technical_success'][0]['name'] if server_data else None
        }
        
        return rankings
    
    def _print_comparison_summary(self, comparison_results: Dict[str, Any]) -> None:
        """Print a summary comparing multiple servers."""
        
        rankings = comparison_results['rankings']
        
        print("\n🏆 SERVER RANKINGS")
        print("-" * 40)
        
        print("\n📊 Overall Success Rate:")
        for i, server in enumerate(rankings['by_overall_success'], 1):
            print(f"   {i}. {server['name']}: {server['overall_success']:.1%}")
        
        print("\n🎯 Functional Performance (LLM Effectiveness):")
        for i, server in enumerate(rankings['by_functional_score'], 1):
            print(f"   {i}. {server['name']}: {server['functional_score']:.2f}/1.00")
        
        print("\n🔧 Technical Reliability:")
        for i, server in enumerate(rankings['by_technical_success'], 1):
            print(f"   {i}. {server['name']}: {server['technical_success']:.1%}")
        
        print("\n💡 RECOMMENDATIONS:")
        recs = rankings['recommendations']
        if recs['best_overall']:
            print(f"   🌟 Best Overall: {recs['best_overall']}")
        if recs['best_for_beginners']:
            print(f"   🎓 Best for Beginners: {recs['best_for_beginners']}")
        if recs['most_reliable']:
            print(f"   🛡️ Most Reliable: {recs['most_reliable']}")


def main():
    """Main entry point for enhanced testing."""
    
    parser = argparse.ArgumentParser(
        description="Enhanced AWS Strands Test Suite with Functional LLM Evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test single server with all test types
  python aws_strands_test_enhanced.py --server amplify-gen2 --all
  
  # Test functional capabilities only
  python aws_strands_test_enhanced.py --server frontend --functional
  
  # Test basic functional tests only
  python aws_strands_test_enhanced.py --server aws-docs --basic
  
  # Compare multiple servers
  python aws_strands_test_enhanced.py --compare amplify-gen2,frontend,aws-docs --functional
        """
    )
    
    parser.add_argument('--server', help='Single MCP server to test')
    parser.add_argument('--compare', help='Comma-separated list of servers to compare')
    parser.add_argument('--all', action='store_true', help='Run all test types')
    parser.add_argument('--technical', action='store_true', help='Run technical tests only')
    parser.add_argument('--functional', action='store_true', help='Run functional tests only')
    parser.add_argument('--basic', action='store_true', help='Run basic functional tests only')
    parser.add_argument('--intermediate', action='store_true', help='Run intermediate functional tests only')
    parser.add_argument('--advanced', action='store_true', help='Run advanced functional tests only')
    parser.add_argument('--config', default='/Users/hejalee/.aws/amazonq/mcp.json.backup', 
                       help='Path to MCP configuration file')
    
    args = parser.parse_args()
    
    # Determine test types
    test_types = []
    if args.all:
        test_types = ['technical', 'functional']
    else:
        if args.technical:
            test_types.append('technical')
        if args.functional:
            test_types.append('functional')
        if args.basic:
            test_types.append('basic')
        if args.intermediate:
            test_types.append('intermediate')
        if args.advanced:
            test_types.append('advanced')
    
    # Default to all if none specified
    if not test_types:
        test_types = ['technical', 'functional']
    
    # Initialize runner
    runner = EnhancedAWSStrandsTestRunner(args.config)
    
    if args.compare:
        # Compare multiple servers
        server_names = [s.strip() for s in args.compare.split(',')]
        
        # Find matching servers
        available_servers = list(runner.technical_runner.servers.keys())
        matched_servers = []
        
        for requested in server_names:
            matches = [name for name in available_servers if requested.lower() in name.lower()]
            if matches:
                matched_servers.extend(matches)
            else:
                print(f"⚠️ No server found matching '{requested}'")
        
        if matched_servers:
            matched_servers = list(dict.fromkeys(matched_servers))  # Remove duplicates
            runner.run_server_comparison(matched_servers, test_types)
        else:
            print("❌ No valid servers found for comparison")
    
    elif args.server:
        # Test single server
        available_servers = list(runner.technical_runner.servers.keys())
        matches = [name for name in available_servers if args.server.lower() in name.lower()]
        
        if matches:
            server_name = matches[0]  # Use first match
            results = runner.run_comprehensive_tests(server_name, test_types)
            runner.print_comprehensive_summary(results)
        else:
            print(f"❌ No server found matching '{args.server}'")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
