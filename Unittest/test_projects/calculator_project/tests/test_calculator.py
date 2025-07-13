
# tests/test_calculator.py
import unittest
from decimal import Decimal
from calculator.calculator import Calculator, process_numbers, Person

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
        self.test_numbers = [1, 2, 3, 4, 5]

    def tearDown(self):
        self.calc = None
        self.test_numbers = None

    def test_addition(self):
        result = self.calc.add(3, 5)
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calc.subtract(10, 5)
        self.assertEqual(result, 5)

class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person("Alice", 30, Decimal("50000"))

    def test_give_raise(self):
        original_salary = self.person.salary
        self.person.give_raise(Decimal("5000"))
        self.assertEqual(self.person.salary, original_salary + Decimal("5000"))
        