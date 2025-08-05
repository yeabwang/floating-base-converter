# Testing and Verification Guide

This guide explains how to run comprehensive tests to verify all claims and functionality of the floating-base-converter library.

## Overview

The floating-base-converter includes three types of verification tools:

1. **🧪 Unit Tests** - Core functionality testing (in `tests/` folder)
2. **📊 Benchmarks** - Performance verification (in `benchmarks/` folder)  
3. **🔍 Validation** - Documentation claims verification (in `validation/` folder)
4. **🎮 Demos** - Interactive demonstrations (in `demos/` folder)

## Quick Start - Run All Tests

```bash
# Run everything at once
python -m pytest tests/ -v                    # Unit tests
python benchmarks/performance_benchmark.py    # Performance benchmarks
python validation/validation_suite.py         # Validation tests
python demos/interactive_demo.py              # Interactive demo
```

## Detailed Testing Instructions

### 1. Unit Tests (Core Functionality)

**Purpose**: Verify core conversion functionality, error handling, and edge cases.

```bash
# Basic test run
pytest tests/

# With coverage report
pytest tests/ --cov=base_converter --cov-report=html

# Verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_converter.py -v
```

**Expected Results**:
- ✅ 30/30 tests should pass
- ✅ 91%+ code coverage
- ✅ Zero failures or errors

### 2. Performance Benchmarks

**Purpose**: Verify performance claims in documentation and measure actual execution times.

```bash
# Run comprehensive performance benchmark
python benchmarks/performance_benchmark.py
```

**What it tests**:
- Precision scaling (10-100 digits)
- Memory usage patterns
- Cross-base conversion performance
- Scientific notation overhead
- Decimal vs Float comparison

**Expected Results**:
- ✅ Sub-millisecond to few-millisecond conversions
- ✅ Linear precision scaling (better than expected)
- ✅ Constant memory usage (~2-7KB)
- ✅ Minimal scientific notation overhead

**Sample Output**:
```
🔍 PRECISION SCALING BENCHMARK
==================================================

| Precision | Avg Time (ms) | Std Dev | Min Time | Max Time | Memory (KB) |
|-----------|---------------|---------|----------|----------|-------------|
| 10 digits |     0.52      |  0.15   |   0.35   |   0.89   |     2.7     |
| 25 digits |     0.79      |  0.18   |   0.58   |   1.15   |     2.7     |
| 50 digits |     1.14      |  0.22   |   0.86   |   1.67   |     3.9     |
| 75 digits |     1.70      |  0.28   |   1.25   |   2.34   |     5.3     |
|100 digits |     2.20      |  0.35   |   1.78   |   3.12   |     6.7     |
```

### 3. Validation Suite

**Purpose**: Verify all documentation examples and claims work correctly.

```bash
# Run comprehensive validation
python validation/validation_suite.py
```

**What it validates**:
- All examples from README.md and documentation
- Mathematical constant conversions (π, e, φ, √2)
- Round-trip conversion accuracy
- Precision boundary conditions
- Scientific notation support
- Error handling for invalid inputs
- Performance claims verification

**Expected Results**:
- ✅ 95%+ test success rate
- ✅ All documentation examples work
- ✅ Mathematical constants convert accurately
- ✅ Error handling works as documented

**Sample Output**:
```
📊 VALIDATION RESULTS
==================================================

Total tests run: 47
Tests passed: 46
Tests failed: 1
Success rate: 97.9%

🎉 VALIDATION SUCCESSFUL!
✅ All documentation claims are verified.
```

### 4. Interactive Demo

**Purpose**: Demonstrate capabilities and allow hands-on testing.

```bash
# Run interactive demo
python demos/interactive_demo.py
```

**What it demonstrates**:
- Basic decimal to base conversions
- Scientific notation support
- High precision calculations
- Real-world application scenarios
- Performance characteristics
- Edge case handling
- Interactive conversion tool

## Interpreting Results

### Unit Test Results

```bash
# Successful run should show:
============================== test session starts ==============================
platform win32 -- Python 3.x.x
collected 30 items

tests/test_converter.py::test_decimal_to_binary ✅ PASSED
tests/test_converter.py::test_decimal_to_octal ✅ PASSED
tests/test_converter.py::test_decimal_to_hex ✅ PASSED
...
============================== 30 passed in 2.15s ==============================
```

### Benchmark Results

Look for these key metrics:
- **Time scaling**: Should be sub-linear (better than expected O(n))
- **Memory usage**: Should be constant (~2-7KB regardless of precision)
- **Performance**: Should complete in milliseconds, not seconds

### Validation Results

Success criteria:
- **Success rate > 95%**: All major functionality verified
- **Documentation examples work**: All examples in docs are accurate
- **Mathematical accuracy**: Known constants convert correctly

## Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Make sure you're in the project root directory
   cd floating-base-converter
   
   # Install in development mode
   pip install -e .
   ```

2. **Slow Performance**:
   ```bash
   # Check Python version (3.8+ recommended)
   python --version
   
   # Ensure you're not in debug mode
   python -O benchmarks/performance_benchmark.py
   ```

3. **Test Failures**:
   ```bash
   # Run with verbose output to see details
   pytest tests/ -v -s
   
   # Check specific failing test
   pytest tests/test_converter.py::test_specific_function -v
   ```

### Environment Requirements

- **Python**: 3.8+ (3.11+ recommended for best performance)
- **Dependencies**: All listed in `requirements.txt`
- **Memory**: At least 100MB available
- **Disk**: Minimal space required

## Continuous Integration

For automated testing in CI/CD:

```yaml
# Example GitHub Actions workflow
name: Test and Validate
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -e .
    - name: Run unit tests
      run: pytest tests/ -v
    - name: Run benchmarks
      run: python benchmarks/performance_benchmark.py
    - name: Run validation
      run: python validation/validation_suite.py
```

## Custom Testing

### Running Specific Benchmark Components

```bash
# Test only precision scaling
python -c "
from benchmarks.performance_benchmark import PerformanceBenchmark
benchmark = PerformanceBenchmark(iterations=10)
benchmark.test_precision_scaling()
"

# Test only memory efficiency
python -c "
from benchmarks.performance_benchmark import PerformanceBenchmark
benchmark = PerformanceBenchmark()
benchmark.test_memory_efficiency()
"
```

### Custom Validation Tests

```bash
# Test specific mathematical constant
python -c "
from validation.validation_suite import ValidationSuite
validator = ValidationSuite()
validator.test_mathematical_constants()
"

# Test only documentation examples
python -c "
from validation.validation_suite import ValidationSuite
validator = ValidationSuite()
validator.test_documentation_examples()
"
```

## Performance Baselines

### Expected Performance Ranges

| Precision | Time Range | Memory Range | Status |
|-----------|------------|--------------|--------|
| 10 digits | 0.3-1.0ms  | 2.5-3.0KB   | ✅ Excellent |
| 25 digits | 0.5-1.5ms  | 2.5-3.0KB   | ✅ Good |
| 50 digits | 0.8-2.5ms  | 3.0-5.0KB   | ✅ Good |
| 100 digits| 1.5-4.0ms  | 5.0-8.0KB   | ✅ Acceptable |

### Accuracy Standards

- **Mathematical constants**: Must match known values to 15+ decimal places
- **Round-trip accuracy**: Must maintain precision within rounding errors
- **Scientific notation**: Must handle all valid exponential formats
- **Edge cases**: Must handle zero, very small, and very large numbers

## Reporting Issues

If tests fail or performance is below expectations:

1. **Check environment**: Python version, dependencies, available memory
2. **Run isolated tests**: Test individual components to isolate issues
3. **Collect diagnostics**: Run with verbose output and capture full logs
4. **Compare baselines**: Check if performance is within expected ranges
5. **Report with details**: Include system info, test output, and error messages

## Verification Checklist

Before considering the library verified:

- [ ] ✅ All unit tests pass (30/30)
- [ ] ✅ Code coverage > 90%
- [ ] ✅ Benchmark performance within expected ranges
- [ ] ✅ Validation success rate > 95%
- [ ] ✅ All documentation examples work
- [ ] ✅ Interactive demo runs without errors
- [ ] ✅ Memory usage remains reasonable
- [ ] ✅ No obvious performance regressions

---

## Summary

This comprehensive testing suite ensures that:

1. **Core functionality works correctly** (unit tests)
2. **Performance meets documented claims** (benchmarks)
3. **Documentation is accurate and complete** (validation)
4. **Real-world usage scenarios function properly** (demos)

Run all tests regularly to maintain confidence in the library's reliability and accuracy.
