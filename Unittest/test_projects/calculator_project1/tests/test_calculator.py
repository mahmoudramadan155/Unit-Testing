# tests/test_calculator.py
import unittest
from calculator.core import Calculator, process_numbers

class SimpleCalculatorTests(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
        self.test_numbers = [1, 2, 3, 4, 5]

    def tearDown(self):
        self.calc = None
        self.test_numbers = None

    def test_addition(self):
        result = self.calc.add(3, 5)
        self.assertEqual(result, 8, "Addition failed")
        
        result = self.calc.add(-3, 5)
        self.assertEqual(result, 2, "Addition with negative numbers failed")
        
    def test_subtraction(self):
        result = self.calc.subtract(10, 5)
        self.assertEqual(result, 5, "Subtraction failed")
        
        result = self.calc.subtract(5, 10)
        self.assertEqual(result, -5, "Subtraction resulting in negative failed")

    def test_multiplication(self):
        result = self.calc.multiply(4, 3)
        self.assertEqual(result, 12, "Multiplication failed")
        
        result = self.calc.multiply(5, 0)
        self.assertEqual(result, 0, "Multiplication by zero failed")

class ExceptionTests(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_division_by_zero(self):
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertTrue("Division by zero" in str(context.exception))
            
    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            process_numbers([1, "2", 3])

class ParameterizedTests(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_multiple_additions(self):
        test_cases = [
            (2, 3, 5),
            (0, 0, 0),
            (-1, 1, 0),
            (10, -5, 5),
            (0.1, 0.2, 0.3)
        ]
        
        for input1, input2, expected in test_cases:
            with self.subTest(input1=input1, input2=input2):
                result = self.calc.add(input1, input2)
                if isinstance(input1, float) or isinstance(input2, float):
                    self.assertAlmostEqual(result, expected, places=7)
                else:
                    self.assertEqual(result, expected)