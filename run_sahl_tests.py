"""
Main execution script for سهل testing system
مطور: Full-stack Testing Engineer
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

async def run_sahl_tests():
    """Run all سهل tests"""
    print("Starting سهل Testing System")
    print("=" * 50)

    # Test results
    results = {}

    # 1. Run Logo Integration
    print("\nRunning Logo Integration...")
    try:
        from simple_logo_integration import main as logo_main
        await logo_main()
        results['logo_integration'] = 'Completed'
    except Exception as e:
        print(f"Logo Integration Error: {e}")
        results['logo_integration'] = f'Error: {e}'

    # 2. Run Performance Tests
    print("\nRunning Performance Tests...")
    try:
        from performance_test_suite import main as perf_main
        perf_results = await perf_main()
        results['performance_tests'] = f'Score: {perf_results.get("score", "N/A")}/100'
    except Exception as e:
        print(f"Performance Tests Error: {e}")
        results['performance_tests'] = f'Error: {e}'

    # 3. Run Security Tests
    print("\nRunning Security Tests...")
    try:
        from security_test_suite import main as sec_main
        sec_results = await sec_main()
        results['security_tests'] = f'Score: {sec_results.get("score", "N/A")}/100'
    except Exception as e:
        print(f"Security Tests Error: {e}")
        results['security_tests'] = f'Error: {e}'

    # Summary
    print("\n" + "=" * 50)
    print("سهل Test Results Summary")
    print("=" * 50)

    for test_name, result in results.items():
        print(f"{test_name.replace('_', ' ').title()}: {result}")

    print("\nAll tests completed!")
    print("Check the following files for detailed results:")
    print("   - logo_test_page.html")
    print("   - test_results/performance_test_report.txt")
    print("   - test_results/security_test_report.txt")
    print("   - test_results/charts/")

if __name__ == "__main__":
    asyncio.run(run_sahl_tests())