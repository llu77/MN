#!/usr/bin/env python3
"""
Test status report generator
"""

import os
import sys
import ast
from pathlib import Path

def analyze_test_file(file_path):
    """Analyze a test file and return its status"""
    result = {
        'file': file_path.name,
        'syntax_valid': False,
        'imports_work': False,
        'has_test_functions': False,
        'test_functions': [],
        'issues': []
    }

    try:
        # Check syntax
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        try:
            ast.parse(content)
            result['syntax_valid'] = True
        except SyntaxError as e:
            result['issues'].append(f"Syntax error: {e}")
            return result

        # Check for test functions
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                result['test_functions'].append(node.name)
                result['has_test_functions'] = True
            elif isinstance(node, ast.ClassDef) and node.name.startswith('Test'):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name.startswith('test_'):
                        result['test_functions'].append(f'{node.name}.{item.name}')
                        result['has_test_functions'] = True

        if result['test_functions']:
            result['has_test_functions'] = True

    except Exception as e:
        result['issues'].append(f"File read error: {e}")

    return result

def main():
    """Generate test status report"""
    test_dir = Path(__file__).parent
    python_files = [f for f in test_dir.glob('*.py')
                   if not f.name.startswith('test_status') and
                   not f.name.startswith('simple_test') and
                   not f.name.startswith('test_runner')]

    print("=" * 80)
    print("TEST FILES STATUS REPORT")
    print("=" * 80)

    results = []
    for file_path in python_files:
        result = analyze_test_file(file_path)
        results.append(result)

    # Summary
    total_files = len(results)
    syntax_valid = sum(1 for r in results if r['syntax_valid'])
    has_tests = sum(1 for r in results if r['has_test_functions'])

    print(f"\nSUMMARY:")
    print(f"Total Python files: {total_files}")
    print(f"Valid syntax: {syntax_valid}/{total_files}")
    print(f"Files with test functions: {has_tests}/{total_files}")

    print(f"\nDETAILED RESULTS:")
    print("-" * 80)

    for result in results:
        status_icon = "[OK]" if result['syntax_valid'] else "[FAIL]"
        test_icon = "[TEST]" if result['has_test_functions'] else "[FILE]"

        print(f"{status_icon} {test_icon} {result['file']}")

        if result['test_functions']:
            print(f"    Test functions ({len(result['test_functions'])}):")
            for test in result['test_functions'][:3]:  # Show first 3
                print(f"      - {test}")
            if len(result['test_functions']) > 3:
                print(f"      ... and {len(result['test_functions']) - 3} more")

        if result['issues']:
            print(f"    Issues:")
            for issue in result['issues']:
                print(f"      ! {issue}")

        print()

    # Recommendations
    print("RECOMMENDATIONS:")
    print("-" * 80)

    if has_tests == 0:
        print("[FAIL] No actual test functions found in any files")
        print("   Consider adding proper test functions with 'test_' prefix")

    syntax_issues = total_files - syntax_valid
    if syntax_issues > 0:
        print(f"[FAIL] {syntax_issues} files have syntax errors that need to be fixed")

    if has_tests > 0:
        print(f"[OK] {has_tests} files contain test functions and can be executed")
        print("   Run: python -m pytest <filename> to execute tests")

    return 0

if __name__ == '__main__':
    sys.exit(main())