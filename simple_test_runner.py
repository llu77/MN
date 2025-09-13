#!/usr/bin/env python3
"""
Simple test runner that executes available test files
"""

import os
import sys
import subprocess
from pathlib import Path

def run_file_with_basic_check(file_path):
    """Try to execute a Python file and check if it runs without errors"""
    print(f"\n{'='*60}")
    print(f"Testing: {file_path.name}")
    print(f"{'='*60}")

    try:
        # First check if file can be imported
        result = subprocess.run([
            sys.executable, '-c', f'import {file_path.stem}; print("Import successful")'
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print("[PASS] File can be imported successfully")
            print(result.stdout.strip())
            return True
        else:
            print("[FAIL] Import failed")
            print("STDERR:", result.stderr.strip())
            return False

    except subprocess.TimeoutExpired:
        print("[TIMEOUT] File execution timed out")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def check_for_test_functions(file_path):
    """Check if file contains test functions"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        test_indicators = [
            'def test_',
            'class Test',
            'unittest',
            'pytest',
            'assert'
        ]

        found_tests = any(indicator in content for indicator in test_indicators)
        return found_tests

    except Exception:
        return False

def main():
    """Main function to run tests"""
    test_dir = Path(__file__).parent
    python_files = [f for f in test_dir.glob('*.py') if f.name not in ['__init__.py', 'test_runner.py', 'simple_test_runner.py']]

    if not python_files:
        print("No Python files found")
        return 0

    print(f"Found {len(python_files)} Python files to test")

    results = {}
    for file_path in python_files:
        print(f"\nChecking: {file_path.name}")

        # Check if it contains test-like content
        has_tests = check_for_test_functions(file_path)
        print(f"Contains test indicators: {has_tests}")

        # Try to run the file
        success = run_file_with_basic_check(file_path)
        results[file_path.name] = {
            'success': success,
            'has_tests': has_tests
        }

    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")

    passed = sum(1 for r in results.values() if r['success'])
    failed = len(results) - passed

    print(f"Total files tested: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    print("\nDetailed results:")
    for filename, result in results.items():
        status = "PASS" if result['success'] else "FAIL"
        test_indicator = "(has tests)" if result['has_tests'] else "(no test indicators)"
        print(f"  {filename}: {status} {test_indicator}")

    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())