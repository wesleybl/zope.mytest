"""
Tests for the zope.mytest package
"""

import unittest
from zope.mytest import IMyInterface, MyImplementation, verify_interface


class TestZopeMytest(unittest.TestCase):
    """Tests for zope.mytest functionalities"""
    
    def setUp(self):
        """Initial setup for tests"""
        self.obj = MyImplementation()
    
    def test_interface_implementation(self):
        """Tests if the class correctly implements the interface"""
        self.assertTrue(verify_interface(self.obj))
        self.assertTrue(IMyInterface.providedBy(self.obj))
    
    def test_method_implemented(self):
        """Tests if the interface method was implemented correctly"""
        result = self.obj.my_method()
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Hello from zope.mytest!")
    
    def test_interface_defined(self):
        """Tests if the interface was defined correctly"""
        # Check if the interface has the method in its definition
        self.assertIn('my_method', IMyInterface.names())


if __name__ == '__main__':
    unittest.main()