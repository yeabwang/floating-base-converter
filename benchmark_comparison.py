#!/usr/bin/env python3
"""
Comprehensive benchmarking script to compare decimal vs float implementations
for base conversion performance and memory usage.
"""

import time
import tracemalloc
import statistics
from typing import List, Dict, Any
from decimal import Decimal, getcontext
import sys

# Set precision to match library's maximum supported precision
getcontext().prec = 100


class FloatBaseConverter:
    """Float-based implementation for comparison"""
    
    def __init__(self):
        self.hex_digits = "0123456789ABCDEF"
    
    def decimal_to_hex_float(self, number: float, precision: int = 10) -> str:
        """Convert decimal to hex using float arithmetic"""
        if number < 0:
            return "-" + self.decimal_to_hex_float(-number, precision)
        
        # Split into integer and fractional parts
        integer_part = int(number)
        fractional_part = number - integer_part
        
        # Convert integer part
        if integer_part == 0:
            int_result = "0"
        else:
            int_result = hex(integer_part)[2:].upper()
        
        # Convert fractional part
        if fractional_part == 0 or precision == 0:
            return int_result
        
        frac_result = []
        current = fractional_part
        
        for _ in range(precision):
            current *= 16
            digit = int(current)
            frac_result.append(self.hex_digits[digit])
            current -= digit
            
            if current == 0:
                break
        
        result = int_result + "." + "".join(frac_result)
        return result
    
    def decimal_to_binary_float(self, number: float, precision: int = 10) -> str:
        """Convert decimal to binary using float arithmetic"""
        if number < 0:
            return "-" + self.decimal_to_binary_float(-number, precision)
        
        # Split into integer and fractional parts
        integer_part = int(number)
        fractional_part = number - integer_part
        
        # Convert integer part
        if integer_part == 0:
            int_result = "0"
        else:
            int_result = bin(integer_part)[2:]
        
        # Convert fractional part
        if fractional_part == 0 or precision == 0:
            return int_result
        
        frac_result = []
        current = fractional_part
        
        for _ in range(precision):
            current *= 2
            digit = int(current)
            frac_result.append(str(digit))
            current -= digit
            
            if current == 0:
                break
        
        result = int_result + "." + "".join(frac_result)
        return result


class DecimalBaseConverter:
    """Decimal-based implementation (our current implementation)"""
    
    def __init__(self):
        self.hex_digits = "0123456789ABCDEF"
    
    def decimal_to_hex_decimal(self, number_str: str, precision: int = 10) -> str:
        """Convert decimal to hex using Decimal arithmetic"""
        number = Decimal(str(number_str))
        
        if number < 0:
            return "-" + self.decimal_to_hex_decimal(str(-number), precision)
        
        # Split into integer and fractional parts
        integer_part = int(number)
        fractional_part = number - integer_part
        
        # Convert integer part
        if integer_part == 0:
            int_result = "0"
        else:
            int_result = hex(integer_part)[2:].upper()
        
        # Convert fractional part
        if fractional_part == 0 or precision == 0:
            return int_result
        
        frac_result = []
        current = fractional_part
        
        for _ in range(precision):
            current *= 16
            digit = int(current)
            frac_result.append(self.hex_digits[digit])
            current -= digit
            
            if current == 0:
                break
        
        result = int_result + "." + "".join(frac_result)
        return result
    
    def decimal_to_binary_decimal(self, number_str: str, precision: int = 10) -> str:
        """Convert decimal to binary using Decimal arithmetic"""
        number = Decimal(str(number_str))
        
        if number < 0:
            return "-" + self.decimal_to_binary_decimal(str(-number), precision)
        
        # Split into integer and fractional parts
        integer_part = int(number)
        fractional_part = number - integer_part
        
        # Convert integer part
        if integer_part == 0:
            int_result = "0"
        else:
            int_result = bin(integer_part)[2:]
        
        # Convert fractional part
        if fractional_part == 0 or precision == 0:
            return int_result
        
        frac_result = []
        current = fractional_part
        
        for _ in range(precision):
            current *= 2
            digit = int(current)
            frac_result.append(str(digit))
            current -= digit
            
            if current == 0:
                break
        
        result = int_result + "." + "".join(frac_result)
        return result


def benchmark_performance(test_values: List[str], precisions: List[int], iterations: int = 1000) -> Dict[str, Any]:
    """Benchmark performance comparison between float and decimal implementations"""
    
    float_converter = FloatBaseConverter()
    decimal_converter = DecimalBaseConverter()
    
    results = {
        'float_times': {},
        'decimal_times': {},
        'speedup_ratios': {},
        'test_values': test_values,
        'precisions': precisions,
        'iterations': iterations
    }
    
    print(f"Running performance benchmarks with {iterations} iterations...")
    print("=" * 80)
    
    for precision in precisions:
        print(f"\nTesting precision: {precision} digits")
        
        float_times = []
        decimal_times = []
        
        for test_value in test_values:
            # Convert string to float for float implementation
            try:
                float_value = float(test_value)
            except (ValueError, OverflowError):
                # Skip values that can't be represented as float
                continue
            
            # Benchmark float implementation
            start_time = time.perf_counter()
            for _ in range(iterations):
                _ = float_converter.decimal_to_hex_float(float_value, precision)
            float_time = time.perf_counter() - start_time
            
            # Benchmark decimal implementation
            start_time = time.perf_counter()
            for _ in range(iterations):
                _ = decimal_converter.decimal_to_hex_decimal(test_value, precision)
            decimal_time = time.perf_counter() - start_time
            
            float_times.append(float_time)
            decimal_times.append(decimal_time)
            
            # Calculate speedup ratio
            speedup = float_time / decimal_time if decimal_time > 0 else float('inf')
            
            print(f"  {test_value:>15}: Float={float_time*1000:.3f}ms, Decimal={decimal_time*1000:.3f}ms, Ratio={speedup:.2f}x")
        
        # Store average times
        avg_float_time = statistics.mean(float_times) if float_times else 0
        avg_decimal_time = statistics.mean(decimal_times) if decimal_times else 0
        avg_speedup = avg_float_time / avg_decimal_time if avg_decimal_time > 0 else float('inf')
        
        results['float_times'][precision] = avg_float_time
        results['decimal_times'][precision] = avg_decimal_time
        results['speedup_ratios'][precision] = avg_speedup
        
        print(f"  Average speedup: {avg_speedup:.2f}x ({'Decimal faster' if avg_speedup > 1 else 'Float faster'})")
    
    return results


def benchmark_memory(test_values: List[str], precisions: List[int], iterations: int = 100) -> Dict[str, Any]:
    """Benchmark memory usage comparison between float and decimal implementations"""
    
    float_converter = FloatBaseConverter()
    decimal_converter = DecimalBaseConverter()
    
    results = {
        'float_memory': {},
        'decimal_memory': {},
        'memory_ratios': {},
        'test_values': test_values,
        'precisions': precisions,
        'iterations': iterations
    }
    
    print(f"\nRunning memory benchmarks with {iterations} iterations...")
    print("=" * 80)
    
    for precision in precisions:
        print(f"\nTesting precision: {precision} digits")
        
        float_memories = []
        decimal_memories = []
        
        for test_value in test_values:
            # Convert string to float for float implementation
            try:
                float_value = float(test_value)
            except (ValueError, OverflowError):
                continue
            
            # Benchmark float memory usage
            tracemalloc.start()
            for _ in range(iterations):
                _ = float_converter.decimal_to_hex_float(float_value, precision)
            _, float_peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            # Benchmark decimal memory usage
            tracemalloc.start()
            for _ in range(iterations):
                _ = decimal_converter.decimal_to_hex_decimal(test_value, precision)
            _, decimal_peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            float_memories.append(float_peak)
            decimal_memories.append(decimal_peak)
            
            memory_ratio = float_peak / decimal_peak if decimal_peak > 0 else float('inf')
            
            print(f"  {test_value:>15}: Float={float_peak/1024:.1f}KB, Decimal={decimal_peak/1024:.1f}KB, Ratio={memory_ratio:.2f}x")
        
        # Store average memory usage
        avg_float_memory = statistics.mean(float_memories) if float_memories else 0
        avg_decimal_memory = statistics.mean(decimal_memories) if decimal_memories else 0
        avg_memory_ratio = avg_float_memory / avg_decimal_memory if avg_decimal_memory > 0 else float('inf')
        
        results['float_memory'][precision] = avg_float_memory
        results['decimal_memory'][precision] = avg_decimal_memory
        results['memory_ratios'][precision] = avg_memory_ratio
        
        savings_percent = (1 - avg_memory_ratio) * 100 if avg_memory_ratio < 1 else (avg_memory_ratio - 1) * 100
        comparison = "less" if avg_memory_ratio < 1 else "more"
        
        print(f"  Average: Decimal uses {abs(savings_percent):.1f}% {comparison} memory than float")
    
    return results


def main():
    """Run comprehensive benchmarks"""
    print("🚀 Decimal vs Float Base Conversion Benchmark")
    print("=" * 80)
    print(f"Python version: {sys.version}")
    print(f"Decimal precision: {getcontext().prec}")
    
    # Test values representing different number types
    test_values = [
        "3.14159",           # Small decimal
        "255.5",             # Medium integer with fraction
        "1234.5678",         # Medium precision
        "999999.123456",     # Large number with precision
        "0.000123456",       # Small fractional
        "123456789.987654"   # Large number with many decimal places
    ]
    
    # Test different precision levels
    precisions = [5, 10, 20, 30, 50]
    
    # Run performance benchmarks
    perf_results = benchmark_performance(test_values, precisions, iterations=1000)
    
    # Run memory benchmarks
    memory_results = benchmark_memory(test_values, precisions, iterations=100)
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 BENCHMARK SUMMARY")
    print("=" * 80)
    
    print("\n🏃 Performance Summary:")
    for precision in precisions:
        speedup = perf_results['speedup_ratios'].get(precision, 0)
        if speedup > 1:
            print(f"  {precision:2d} digits: Decimal is {speedup:.2f}x FASTER than float")
        else:
            print(f"  {precision:2d} digits: Float is {1/speedup:.2f}x FASTER than decimal")
    
    print("\n💾 Memory Summary:")
    for precision in precisions:
        ratio = memory_results['memory_ratios'].get(precision, 0)
        if ratio < 1:
            savings = (1 - ratio) * 100
            print(f"  {precision:2d} digits: Decimal uses {savings:.1f}% LESS memory than float")
        else:
            overhead = (ratio - 1) * 100
            print(f"  {precision:2d} digits: Decimal uses {overhead:.1f}% MORE memory than float")
    
    # Overall conclusions
    print("\n🎯 CONCLUSIONS:")
    avg_speedup = statistics.mean(perf_results['speedup_ratios'].values())
    avg_memory_ratio = statistics.mean(memory_results['memory_ratios'].values())
    
    if avg_speedup > 1:
        print(f"✅ Performance: Decimal is on average {avg_speedup:.2f}x faster than float")
    else:
        print(f"❌ Performance: Float is on average {1/avg_speedup:.2f}x faster than decimal")
    
    if avg_memory_ratio < 1:
        savings = (1 - avg_memory_ratio) * 100
        print(f"✅ Memory: Decimal uses {savings:.1f}% less memory than float")
    else:
        overhead = (avg_memory_ratio - 1) * 100
        print(f"❌ Memory: Decimal uses {overhead:.1f}% more memory than float")
    

if __name__ == "__main__":
    main()
