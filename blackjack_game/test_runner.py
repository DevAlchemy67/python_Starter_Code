#!/usr/bin/env python3
"""
Simple test runner for blackjack game (no pytest required)
"""

import sys
import traceback


def run_tests():
    """Run all tests"""
    test_modules = [
        'tests.test_core',
        'tests.test_strategy',
    ]
    
    passed = 0
    failed = 0
    
    for module_name in test_modules:
        try:
            module = __import__(module_name, fromlist=[''])
            
            # Find and run test classes
            for name in dir(module):
                obj = getattr(module, name)
                if name.startswith('Test') and hasattr(obj, '__bases__'):
                    # This is a test class
                    test_class = obj()
                    
                    # Find and run test methods
                    for method_name in dir(test_class):
                        if method_name.startswith('test_'):
                            try:
                                method = getattr(test_class, method_name)
                                method()
                                print(f"✓ {module_name}.{name}.{method_name}")
                                passed += 1
                            except Exception as e:
                                print(f"✗ {module_name}.{name}.{method_name}")
                                print(f"  Error: {e}")
                                traceback.print_exc()
                                failed += 1
        
        except Exception as e:
            print(f"✗ Failed to load {module_name}: {e}")
            traceback.print_exc()
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
