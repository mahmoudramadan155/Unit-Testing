# Comprehensive Guide to Unit Testing in Python with unittest

Unit testing is a critical practice in software development that ensures individual components of a program work as expected. Python provides the built-in unittest module, which is a powerful tool for writing and running tests.

## 1. Introduction to Unit Testing

Unit testing involves testing the smallest testable parts (units) of an application in isolation. In Python, the unittest module provides a robust framework for writing, organizing, and running tests.

**Why Unit Testing?**
- Ensures code correctness
- Helps in debugging and catching regressions
- Facilitates refactoring
- Supports Test-Driven Development (TDD)

## 2. Basics of unittest in Python

### Writing a Simple Test Case
A test case is created by subclassing unittest.TestCase and defining methods that start with test_.

```python
import unittest

# Function to be tested
def add(x, y):
    return x + y

# Creating a test case
class TestMathOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)  # Test case 1
        self.assertEqual(add(-1, 1), 0)  # Test case 2

if __name__ == '__main__':
    unittest.main()
```

**Explanation**
- unittest.TestCase: Inherits from this class to create test cases.
- assertEqual(a, b): Checks if a == b, otherwise fails the test.
- unittest.main(): Runs all test cases.

## 3. Common Assertions in unittest

unittest provides various assertion methods:

| Assertion Method | Description |
|-----------------|-------------|
| assertEqual(a, b) | Checks if a == b |
| assertNotEqual(a, b) | Checks if a != b |
| assertTrue(x) | Checks if x is True |
| assertFalse(x) | Checks if x is False |
| assertIs(a, b) | Checks if a is b |
| assertIsNot(a, b) | Checks if a is not b |
| assertIsNone(x) | Checks if x is None |
| assertIsNotNone(x) | Checks if x is not None |
| assertRaises(Exception, func, *args) | Checks if func(*args) raises Exception |

### Example: Testing for Exceptions

```python
def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

class TestMathOperations(unittest.TestCase):
    def test_divide(self):
        self.assertRaises(ValueError, divide, 4, 0)
```

## 4. Running Tests

### Running Tests from the Command Line
Save the test script (e.g., test_math.py) and run:

```bash
python -m unittest test_math.py
```

or discover all tests in a directory:

```bash
python -m unittest discover
```

## 5. Setup and Teardown Methods

- setUp(): Runs before each test case (e.g., initializing resources).
- tearDown(): Runs after each test case (e.g., cleaning up).

### Example: Using setUp and tearDown

```python
class TestExample(unittest.TestCase):
    def setUp(self):
        self.data = [1, 2, 3]

    def tearDown(self):
        self.data = None

    def test_length(self):
        self.assertEqual(len(self.data), 3)
```

## 6. Mocking with unittest.mock

Mocking is useful for testing code that depends on external systems.

### Example: Using unittest.mock

```python
from unittest.mock import MagicMock

class Database:
    def fetch_data(self):
        return "Real Data"

class TestDatabase(unittest.TestCase):
    def test_fetch_data(self):
        db = Database()
        db.fetch_data = MagicMock(return_value="Mocked Data")
        self.assertEqual(db.fetch_data(), "Mocked Data")
```

## 7. Advanced Testing Techniques

### Parameterized Tests
Using subTest() to run multiple test cases efficiently.

```python
class TestMath(unittest.TestCase):
    def test_add(self):
        test_cases = [(2, 3, 5), (-1, 1, 0), (0, 0, 0)]
        for x, y, expected in test_cases:
            with self.subTest(x=x, y=y, expected=expected):
                self.assertEqual(add(x, y), expected)
```

### Skipping Tests

```python
class TestExample(unittest.TestCase):
    @unittest.skip("Skipping this test")
    def test_skipped(self):
        self.fail("This should not run")

    @unittest.expectedFailure
    def test_expected_failure(self):
        self.assertEqual(1, 0)
```

## 8. Test Coverage with coverage.py

To measure test coverage, install coverage:

```bash
pip install coverage
```

Run tests with coverage:

```bash
coverage run -m unittest discover
coverage report -m
```

## 9. Structuring Unit Tests in a Project

A common structure:

```
project/
│── mymodule/
│   ├── __init__.py
│   ├── math_utils.py
│── tests/
│   ├── __init__.py
│   ├── test_math_utils.py
```

Run all tests:

```bash
python -m unittest discover tests
```

## 10. Best Practices for Writing Unit Tests

- Keep tests isolated and independent.
- Use descriptive test method names.
- Cover edge cases and invalid inputs.
- Run tests frequently and integrate with CI/CD pipelines.
- Maintain clear test documentation.
