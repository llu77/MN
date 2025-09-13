#!/usr/bin/env python3
"""
Comprehensive test runner for the mn directory
Handles various test file formats and skips problematic ones
"""

import sys
import os
import traceback
import subprocess
from pathlib import Path

def check_file_syntax(filepath):
    """Check if a Python file has valid syntax"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        compile(source, str(filepath), 'exec')
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"

def run_test_file(filepath):
    """Run a single test file"""
    print(f"\n{'='*50}")
    print(f"Running tests in: {filepath.name}")
    print(f"{'='*50}")

    # Check syntax first
    valid, error = check_file_syntax(filepath)
    if not valid:
        print(f"[FAIL] SKIPPED - {error}")
        return False

    try:
        # Try to run with pytest
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            str(filepath), '-v', '--tb=short'
        ], capture_output=True, text=True, cwd=filepath.parent)

        if result.returncode == 0:
            print("[PASS] PASSED")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("[FAIL] FAILED")
            if result.stdout:
                print("STDOUT:", result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return False

    except Exception as e:
        print(f"[FAIL] ERROR - Failed to run test: {e}")
        return False

def main():
    """Main test runner function"""
    test_dir = Path(__file__).parent
    python_files = list(test_dir.glob('*.py'))

    # Filter out files that are obviously not test files
    test_files = []
    for file in python_files:
        if file.name.startswith('test_') or 'test' in file.name.lower():
            test_files.append(file)

    if not test_files:
        print("No test files found with 'test' in the name")
        # Look for any Python files that might contain test functions
        for file in python_files:
            if file.name not in ['__init__.py']:
                test_files.append(file)

    print(f"Found {len(test_files)} potential test files")

    passed = 0
    failed = 0
    skipped = 0

    for test_file in test_files:
        if test_file.name == 'run_all_tests.py':  # Skip this runner
            continue

        success = run_test_file(test_file)
        if success:
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")

    if failed > 0:
        print(f"\n[FAIL] Some tests failed")
        return 1
    else:
        print(f"\n[PASS] All tests passed!")
        return 0

if __name__ == '__main__':
    sys.exit(main())