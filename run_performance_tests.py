"""
Performance tests for سهل system
"""

import asyncio
from performance_test_suite import PerformanceTestSuite

async def run_performance_tests():
    """Run performance tests"""
    print("Starting سهل Performance Tests")
    print("=" * 50)

    performance_tester = PerformanceTestSuite()

    try:
        results = await performance_tester.run_performance_tests()

        print(f"\nPerformance Score: {results['score']:.1f}/100")
        print(f"Performance Status: {'Excellent' if results['score'] >= 90 else 'Good' if results['score'] >= 70 else 'Needs Improvement'}")

        print(f"\nFull report available at: test_results/performance_test_report.txt")
        print("Charts available at: test_results/charts/")

        return results

    except Exception as e:
        print(f"Performance test execution failed: {str(e)}")
        return None

if __name__ == "__main__":
    asyncio.run(run_performance_tests())