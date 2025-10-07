"""
zope.mytest - An example package using zope.interface

This module demonstrates how to use Zope interfaces to define
contracts and implementations in Python.

PYLANCE IMPORT ISSUE DEMONSTRATION:
===================================
The import below will show a Pylance error:
"Não foi possível resolver a importação 'zope.interface'"

This happens because:
1. We have a local src/zope/ namespace directory
2. Pylance tries to resolve zope.interface within the local namespace
3. It fails to fall back to site-packages where zope.interface is installed
4. The code runs perfectly fine despite the Pylance error

This is a known limitation of Pylance's import resolution with namespace packages.
"""

# This import will show a Pylance error but works correctly at runtime
from zope.interface import Interface, implementer


class IMyInterface(Interface):
    """Example interface that defines a basic contract."""
    
    def my_method():
        """Method that must be implemented by classes implementing this interface.
        
        Returns:
            str: An example string
        """


@implementer(IMyInterface)
class MyImplementation:
    """Example implementation of IMyInterface."""
    
    def my_method(self):
        """Implementation of the method defined in the interface.
        
        Returns:
            str: An example message
        """
        return "Hello from zope.mytest!"


def verify_interface(obj):
    """Verifies if an object implements IMyInterface.
    
    Args:
        obj: Object to be verified
        
    Returns:
        bool: True if the object implements the interface, False otherwise
    """
    return IMyInterface.providedBy(obj)


# Usage example
def usage_example():
    """Demonstrates the basic usage of the package."""
    # Create an instance
    obj = MyImplementation()
    
    # Verify if it implements the interface
    if verify_interface(obj):
        print("The object implements IMyInterface")
        print(f"Result: {obj.my_method()}")
    else:
        print("The object does NOT implement IMyInterface")


# Make main classes and functions available at the module level
__all__ = [
    'IMyInterface',
    'MyImplementation', 
    'verify_interface',
    'usage_example'
]