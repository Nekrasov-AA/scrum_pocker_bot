#!/usr/bin/env python3
"""
Test runner for Scrum Poker Bot

This script runs all available tests in the correct order.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_test(test_file, description):
    """Run a single test file and report results"""
    print(f"\n{'='*60}")
    print(f"🧪 Running: {description}")
    print(f"📁 File: {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=False, 
                              text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    """Main test runner function"""
    print("🚀 Scrum Poker Bot - Test Suite Runner")
    print("=====================================")
    
    # Get tests directory
    tests_dir = Path(__file__).parent
    
    # List of tests to run
    tests = [
        ("tests/test_demo.py", "Function Demo Test - Basic functionality showcase"),
        ("tests/test_async.py", "Async Handlers Test - Bot handlers and async operations")
    ]
    
    results = []
    
    # Run each test
    for test_file, description in tests:
        test_path = tests_dir / test_file.split('/')[-1]  # Get just the filename
        success = run_test(str(test_path), description)
        results.append((description, success))
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print('='*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {description}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed successfully!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    exit(main())