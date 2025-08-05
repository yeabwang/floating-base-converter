#!/usr/bin/env python3
"""
Performance benchmarks for floating-base-converter
Verifies O(n) time complexity and O(1) memory overhead claims
"""

import time
import tracemalloc
import statistics
from typing import List, Tuple
from base_converter import BaseConverter


def measure_time_and_memory(func, *args, **kwargs) -> Tuple[float, float]:
    """Measure execution time and peak memory usage of a function."""
    # Start memory tracing
    tracemalloc.start()
    
    # Measure time
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    
    # Get peak memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    execution_time = end_time - start_time
    peak_memory_kb = peak / 1024  # Convert to KB
    
    return execution_time, peak_memory_kb


def benchmark_conversion_time_complexity():
    """Test if conversion time scales linearly with input size (O(n))."""
    print("🔍 Testing Time Complexity (should be O(n))")
    print("=" * 50)
    
    converter = BaseConverter()
    input_sizes = [5, 10, 15, 20, 25, 30]  # Smaller sizes to stay within precision limits
    times = []
    
    for size in input_sizes:
        # Create decimal number with 'size' digits, but limit precision to max 50
        test_number = "3." + "1" * size
        precision = min(size, 50)  # Respect precision limit
        
        # Run multiple times and take average
        run_times = []
        result = ""  # Initialize result variable
        for _ in range(10):  # More runs for better average
            start = time.perf_counter()
            result = converter.decimal_to_hex(test_number, precision=precision)
            end = time.perf_counter()
            run_times.append(end - start)
        
        avg_time = statistics.mean(run_times)
        times.append(avg_time)
        
        print(f"Input size: {size:2d} digits | Precision: {precision:2d} | Time: {avg_time*1000:6.3f}ms | Result length: {len(result)}")
    
    # Check if time scales roughly linearly
    print(f"\n📊 Time Complexity Analysis:")
    for i in range(1, len(input_sizes)):
        size_ratio = input_sizes[i] / input_sizes[i-1]
        time_ratio = times[i] / times[i-1] if times[i-1] > 0 else 1
        print(f"Size ratio: {size_ratio:4.1f}x | Time ratio: {time_ratio:4.1f}x")
    
    return input_sizes, times


def benchmark_memory_usage():
    """Test if memory usage is constant (O(1) overhead)."""
    print("\n\n🧠 Testing Memory Usage (should be O(1) overhead)")
    print("=" * 50)
    
    converter = BaseConverter()
    input_sizes = [5, 10, 15, 20, 25, 30]  # Smaller sizes
    memory_usages = []
    
    for size in input_sizes:
        # Create test number with limited precision
        test_number = "3." + "1" * size
        precision = min(size, 50)  # Respect precision limit
        
        # Measure memory
        execution_time, peak_memory = measure_time_and_memory(
            converter.decimal_to_hex, test_number, precision=precision
        )
        
        memory_usages.append(peak_memory)
        print(f"Input size: {size:2d} digits | Peak memory: {peak_memory:6.1f} KB | Time: {execution_time*1000:6.3f}ms")
    
    # Analyze memory growth
    print(f"\n📊 Memory Usage Analysis:")
    base_memory = memory_usages[0]
    for i, (size, memory) in enumerate(zip(input_sizes, memory_usages)):
        overhead = memory - base_memory
        print(f"Size: {size:2d} | Memory: {memory:6.1f} KB | Overhead: {overhead:+6.1f} KB")
    
    return input_sizes, memory_usages


def benchmark_different_operations():
    """Compare performance across different conversion operations."""
    print("\n\n⚡ Performance Comparison Across Operations")
    print("=" * 50)
    
    converter = BaseConverter()
    test_number = "3." + "14159" * 10  # ~50 digit number (within limits)
    operations = [
        ("decimal_to_binary", lambda: converter.decimal_to_binary(test_number, precision=25)),
        ("decimal_to_hex", lambda: converter.decimal_to_hex(test_number, precision=25)),
        ("binary_to_decimal", lambda: converter.binary_to_decimal("11.001001", precision=25)),
        ("hex_to_decimal", lambda: converter.hex_to_decimal("3.243F", precision=25)),
    ]
    
    for name, operation in operations:
        times = []
        for _ in range(20):  # More runs for better statistics
            start = time.perf_counter()
            result = operation()
            end = time.perf_counter()
            times.append(end - start)
        
        avg_time = statistics.mean(times)
        std_time = statistics.stdev(times) if len(times) > 1 else 0
        print(f"{name:18s} | Avg: {avg_time*1000:6.3f}ms ± {std_time*1000:4.3f}ms")


def verify_accuracy_with_precision():
    """Test conversion accuracy with different precision levels."""
    print("\n\n🎯 Accuracy Testing with Different Precision Levels")
    print("=" * 50)
    
    converter = BaseConverter()
    test_number = 3.14159265359
    
    for precision in [1, 5, 10, 20]:
        binary_result = converter.decimal_to_binary(test_number, precision=precision)
        hex_result = converter.decimal_to_hex(test_number, precision=precision)
        
        # Convert back to verify accuracy
        back_to_decimal = float(converter.binary_to_decimal(binary_result))
        accuracy = abs(test_number - back_to_decimal)
        
        print(f"Precision: {precision:2d} | Binary: {binary_result:25s} | Accuracy: {accuracy:.2e}")


def main():
    """Run all performance benchmarks."""
    print("🚀 Floating-Base-Converter Performance Benchmarks")
    print("=" * 60)
    
    # Time complexity test
    input_sizes, times = benchmark_conversion_time_complexity()
    
    # Memory usage test  
    memory_sizes, memory_usages = benchmark_memory_usage()
    
    # Operation comparison
    benchmark_different_operations()
    
    # Accuracy testing
    verify_accuracy_with_precision()
    
    # Summary
    print("\n\n📋 Performance Summary")
    print("=" * 50)
    
    # Calculate time complexity factor
    size_growth = input_sizes[-1] / input_sizes[0] 
    time_growth = times[-1] / times[0]
    complexity_factor = time_growth / size_growth
    
    print(f"Time Complexity Factor: {complexity_factor:.2f}")
    if complexity_factor < 2.0:
        print("✅ Time complexity appears to be O(n) or better")
    else:
        print("❌ Time complexity may be worse than O(n)")
    
    # Calculate memory overhead
    memory_growth = max(memory_usages) - min(memory_usages)
    print(f"Memory Overhead Range: {memory_growth:.1f} KB")
    if memory_growth < 100:  # Less than 100KB variation
        print("✅ Memory usage appears to be O(1) overhead")
    else:
        print("❌ Memory usage may have significant overhead")


if __name__ == "__main__":
    main()
