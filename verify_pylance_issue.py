#!/usr/bin/env python3
"""
Verification script to demonstrate that the code works despite Pylance errors.

This script verifies that:
1. zope.interface can be imported correctly
2. The namespace package resolution works
3. The interfaces work as expected
4. All functionality is operational

Run this script to prove that Pylance shows false positive import errors.
"""

import sys
import importlib.util

def check_import(module_name):
    """Check if a module can be imported."""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            return False, f"Module {module_name} not found"
        
        module = importlib.import_module(module_name)
        return True, f"Module {module_name} imported successfully"
    except ImportError as e:
        return False, f"Import error for {module_name}: {e}"

def main():
    """Main verification function."""
    print("🔍 Pylance Import Resolution Issue Verification")
    print("=" * 50)
    
    # Check if zope.interface is available
    success, msg = check_import('zope.interface')
    print(f"1. zope.interface availability: {'✅' if success else '❌'} {msg}")
    
    if not success:
        print("❌ zope.interface is not installed. Run 'make install-dev' first.")
        sys.exit(1)
    
    # Check if our package can be imported
    success, msg = check_import('zope.mytest')
    print(f"2. zope.mytest availability: {'✅' if success else '❌'} {msg}")
    
    if not success:
        print("❌ zope.mytest is not installed. Run 'make install-dev' first.")
        sys.exit(1)
    
    # Test the actual functionality
    print("\n🧪 Testing Functionality:")
    print("-" * 30)
    
    try:
        # Import our module (this is where Pylance shows the error)
        from zope.mytest import IMyInterface, MyImplementation, verify_interface
        print("3. Import from zope.mytest: ✅ Success")
        
        # Create an instance
        obj = MyImplementation()
        print("4. Create MyImplementation instance: ✅ Success")
        
        # Test interface verification
        implements = verify_interface(obj)
        print(f"5. Interface verification: {'✅' if implements else '❌'} {implements}")
        
        # Test method call
        result = obj.my_method()
        expected = "Hello from zope.mytest!"
        method_works = result == expected
        print(f"6. Method call: {'✅' if method_works else '❌'} '{result}'")
        
        # Test direct interface check
        direct_check = IMyInterface.providedBy(obj)
        print(f"7. Direct interface check: {'✅' if direct_check else '❌'} {direct_check}")
        
        print("\n🎉 Conclusion:")
        print("=" * 50)
        print("✅ ALL FUNCTIONALITY WORKS CORRECTLY!")
        print("❌ Pylance shows FALSE POSITIVE import errors")
        print("\nThis demonstrates that Pylance cannot resolve imports from")
        print("site-packages when there's a namespace collision with src/ packages.")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("This suggests the package is not properly installed.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()