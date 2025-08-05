#!/usr/bin/env python3
"""
All-in-One Test Runner
======================

This script runs all available tests, benchmarks, and validations in sequence.
Use this for comprehensive verification of the floating-base-converter library.
"""

import subprocess
import sys
import time
from pathlib import Path


def run_command(command, description):
    """Run a command and capture its output."""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"Command: {command}")
    print()
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=Path(__file__).parent
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        success = result.returncode == 0
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n{status} ({duration:.1f}s)")
        
        return success
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Run all tests and generate summary report."""
    print("🚀 COMPREHENSIVE TEST RUNNER")
    print("=" * 60)
    print("Running all tests, benchmarks, and validations...")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Track results
    results = {}
    
    # 1. Unit Tests
    results['Unit Tests'] = run_command(
        "python -m pytest tests/ -v --tb=short",
        "UNIT TESTS - Core Functionality"
    )
    
    # 2. Code Quality (if tools are available)
    try:
        results['Code Quality (MyPy)'] = run_command(
            "python -m mypy base_converter/ --ignore-missing-imports",
            "CODE QUALITY - Type Checking"
        )
    except:
        print("\nℹ️  MyPy not available, skipping type checking")
        results['Code Quality (MyPy)'] = None
    
    try:
        results['Code Quality (Flake8)'] = run_command(
            "python -m flake8 base_converter/ --max-line-length=88 --extend-ignore=E203",
            "CODE QUALITY - Style Checking"
        )
    except:
        print("\nℹ️  Flake8 not available, skipping style checking")
        results['Code Quality (Flake8)'] = None
    
    # 3. Performance Benchmarks
    results['Performance Benchmarks'] = run_command(
        "python benchmarks/performance_benchmark.py",
        "PERFORMANCE BENCHMARKS - Speed & Memory"
    )
    
    # 4. Validation Suite
    results['Validation Suite'] = run_command(
        "python validation/validation_suite.py",
        "VALIDATION SUITE - Documentation Claims"
    )
    
    # 5. Coverage Report (if available)
    try:
        results['Coverage Report'] = run_command(
            "python -m pytest tests/ --cov=base_converter --cov-report=term-missing",
            "COVERAGE REPORT - Test Coverage Analysis"
        )
    except:
        print("\nℹ️  Coverage not available, skipping coverage report")
        results['Coverage Report'] = None
    
    # Generate summary report
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY REPORT")
    print(f"{'='*60}")
    
    passed_count = 0
    total_count = 0
    
    for test_name, result in results.items():
        if result is not None:
            total_count += 1
            if result:
                passed_count += 1
                status = "✅ PASSED"
            else:
                status = "❌ FAILED"
        else:
            status = "⚠️  SKIPPED"
        
        print(f"{test_name:25} {status}")
    
    print(f"\n📈 OVERALL RESULTS:")
    if total_count > 0:
        success_rate = (passed_count / total_count) * 100
        print(f"Tests passed: {passed_count}/{total_count} ({success_rate:.1f}%)")
        
        if success_rate == 100:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ The floating-base-converter library is fully verified.")
            print("✅ All functionality, performance, and documentation claims confirmed.")
        elif success_rate >= 90:
            print("\n🟡 MOSTLY SUCCESSFUL")
            print("⚠️  Minor issues detected - review failed tests above.")
        else:
            print("\n🔴 SIGNIFICANT ISSUES DETECTED")
            print("❌ Multiple test failures - library may need attention.")
    else:
        print("No tests were executed successfully.")
    
    # Additional recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    
    if results.get('Unit Tests', False):
        print("✅ Core functionality is working correctly")
    else:
        print("❌ Fix unit test failures before proceeding")
    
    if results.get('Performance Benchmarks', False):
        print("✅ Performance meets documented specifications")
    else:
        print("⚠️  Review performance benchmark results")
    
    if results.get('Validation Suite', False):
        print("✅ All documentation claims are verified")
    else:
        print("⚠️  Some documentation claims may need updates")
    
    # Next steps
    print(f"\n🔧 NEXT STEPS:")
    print("• Review any failed tests above")
    print("• Run individual test suites for detailed analysis:")
    print("  - pytest tests/ -v (detailed unit test output)")
    print("  - python benchmarks/performance_benchmark.py")
    print("  - python validation/validation_suite.py")
    print("• Try the interactive demo: python demos/interactive_demo.py")
    
    print(f"\n📚 DOCUMENTATION:")
    print("• See TESTING_GUIDE.md for detailed testing instructions")
    print("• See README.md for usage examples")
    print("• See docs/ folder for technical documentation")
    
    # Exit with appropriate code
    if total_count > 0 and passed_count == total_count:
        sys.exit(0)  # All tests passed
    else:
        sys.exit(1)  # Some tests failed


if __name__ == "__main__":
    main()
