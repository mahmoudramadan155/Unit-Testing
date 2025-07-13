import unittest
from typing import List, Optional
from unittest.mock import Mock, patch
import asyncio
import sys
from dataclasses import dataclass
from decimal import Decimal

# Basic Calculator Implementation
class Calculator:
    """A simple calculator class to demonstrate basic unit testing."""
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a."""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Divide a by b."""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b

def process_numbers(numbers: List[float]) -> float:
    """Process a list of numbers and return their sum."""
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise TypeError("All inputs must be numbers")
    return sum(numbers)

# 1. Basic Test Structure with Setup and Teardown
class SimpleCalculatorTests(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calc = Calculator()
        self.test_numbers = [1, 2, 3, 4, 5]

    def tearDown(self):
        """Clean up after each test method."""
        self.calc = None
        self.test_numbers = None

    def test_addition(self):
        """Test basic addition functionality."""
        result = self.calc.add(3, 5)
        self.assertEqual(result, 8, "Addition failed")
        
        # Testing negative numbers
        result = self.calc.add(-3, 5)
        self.assertEqual(result, 2, "Addition with negative numbers failed")
        
    def test_subtraction(self):
        """Test basic subtraction functionality."""
        result = self.calc.subtract(10, 5)
        self.assertEqual(result, 5, "Subtraction failed")
        
        # Testing negative results
        result = self.calc.subtract(5, 10)
        self.assertEqual(result, -5, "Subtraction resulting in negative failed")

    def test_multiplication(self):
        """Test multiplication functionality."""
        result = self.calc.multiply(4, 3)
        self.assertEqual(result, 12, "Multiplication failed")
        
        # Test multiplication by zero
        result = self.calc.multiply(5, 0)
        self.assertEqual(result, 0, "Multiplication by zero failed")

# 2. Testing Exceptions with Context Managers
class ExceptionTests(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_division_by_zero(self):
        """Test that division by zero raises an exception."""
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertTrue("Division by zero" in str(context.exception))
            
    def test_invalid_input(self):
        """Test handling of invalid input."""
        with self.assertRaises(TypeError):
            process_numbers([1, "2", 3])  # String in list should raise TypeError

# 3. Testing Complex Objects with Rich Comparisons
@dataclass
class Person:
    name: str
    age: int
    salary: Optional[Decimal] = None

    def give_raise(self, amount: Decimal) -> None:
        """Give the person a raise."""
        if self.salary is None:
            raise ValueError("Person has no current salary")
        self.salary += amount

class PersonTests(unittest.TestCase):
    def setUp(self):
        self.person1 = Person("Alice", 30, Decimal("50000"))
        self.person2 = Person("Bob", 25, Decimal("45000"))

    def test_person_creation(self):
        """Test person object creation and attributes."""
        person = Person("Alice", 30, Decimal("50000"))
        self.assertEqual(person.name, "Alice")
        self.assertEqual(person.age, 30)
        self.assertEqual(person.salary, Decimal("50000"))
        
    def test_person_raise(self):
        """Test giving a person a raise."""
        original_salary = self.person1.salary
        raise_amount = Decimal("5000")
        
        self.person1.give_raise(raise_amount)
        self.assertEqual(
            self.person1.salary,
            original_salary + raise_amount,
            "Salary raise was not applied correctly"
        )

# 4. Testing with Fixtures and Mocks
class DatabaseConnection:
    def query(self, sql: str) -> List[dict]:
        """Execute a SQL query."""
        pass

    def close(self) -> None:
        """Close the database connection."""
        pass

def create_test_database() -> DatabaseConnection:
    """Create a test database connection."""
    return DatabaseConnection()

def get_user_data(user_id: int) -> List[dict]:
    """Get user data from database."""
    conn = DatabaseConnection()
    return conn.query(f"SELECT * FROM users WHERE id = {user_id}")

class DatabaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests in the class."""
        cls.db_connection = create_test_database()
        
    @classmethod
    def tearDownClass(cls):
        """Clean up fixtures that were created for all tests."""
        cls.db_connection.close()
        
    def test_database_query(self):
        """Test database query with mock."""
        mock_db = Mock()
        mock_db.query.return_value = [
            {"id": 123, "name": "Test User", "email": "test@example.com"}
        ]
        
        # Patch the get_user_data function directly instead of trying to patch a non-existent module
        # with patch('database.get_connection', return_value=mock_db):
        with patch('__main__.DatabaseConnection', return_value=mock_db):
            results = get_user_data(user_id=123)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["name"], "Test User")
            mock_db.query.assert_called_once()

# 5. Parameterized Tests with SubTest
class ParameterizedTests(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_multiple_additions(self):
        """Test addition with multiple input combinations."""
        test_cases = [
            (2, 3, 5),    # (input1, input2, expected_output)
            (0, 0, 0),
            (-1, 1, 0),
            (10, -5, 5),
            (0.1, 0.2, 0.3)  # Note: Floating point arithmetic may need assertAlmostEqual
        ]
        
        for input1, input2, expected in test_cases:
            with self.subTest(input1=input1, input2=input2):
                result = self.calc.add(input1, input2)
                if isinstance(input1, float) or isinstance(input2, float):
                    self.assertAlmostEqual(result, expected, places=7)
                else:
                    self.assertEqual(result, expected)

# 6. Testing Asynchronous Code
class AsyncCalculator:
    async def async_add(self, a: float, b: float) -> float:
        """Asynchronously add two numbers (simulating async operation)."""
        await asyncio.sleep(0.1)  # Simulate async operation
        return a + b

class AsyncTests(unittest.TestCase):
    def setUp(self):
        self.async_calc = AsyncCalculator()

    async def async_test_add(self):
        """Async test helper method."""
        result = await self.async_calc.async_add(3, 4)
        self.assertEqual(result, 7)

    def test_async_operation(self):
        """Test asynchronous operations."""
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.async_test_add())
        asyncio.run(self.async_test_add())

# 7. Test Coverage and Skip Decorators
@unittest.skipUnless(sys.platform.startswith("win"), "Windows-specific tests")
class WindowsOnlyTests(unittest.TestCase):
    def test_windows_specific_feature(self):
        """Test that runs only on Windows."""
        pass

class SkipTests(unittest.TestCase):
    @unittest.skip("Demonstrating skip decorator")
    def test_skipped(self):
        """This test will be skipped."""
        self.fail("This test should have been skipped")
        
    @unittest.skipIf(sys.version_info < (3, 7),
                     "Requires Python 3.7 or higher")
    def test_new_feature(self):
        """Test that runs only on Python 3.7+"""
        # Test new Python 3.7+ feature
        pass

    @unittest.expectedFailure
    def test_expected_to_fail(self):
        """Test that we expect to fail."""
        self.assertEqual(1 + 1, 3, "This test is expected to fail")

if __name__ == '__main__':
    unittest.main()
