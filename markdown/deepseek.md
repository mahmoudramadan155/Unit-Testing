# Python Unit Testing Guide with unittest

## 1. Introduction to unittest
The unittest module is inspired by Java's JUnit and provides a rich set of tools for constructing and running tests. It supports:

- Test automation: Running multiple tests automatically
- Setup and teardown: Preparing and cleaning up test environments
- Assertions: Checking if conditions are met
- Test discovery: Automatically finding and running tests

## 2. Basic Structure of a Test Case
A test case is created by subclassing unittest.TestCase. Each test is a method whose name starts with test_.

```python
import unittest

# Function to be tested
def add(a, b):
    return a + b

# Test case
class TestMathOperations(unittest.TestCase):
    def test_add(self):
        result = add(2, 3)
        self.assertEqual(result, 5)  # Assertion

# Run the tests
if __name__ == "__main__":
    unittest.main()
```

## 3. Key Components of unittest

### a. Assertions
Assertions are used to verify that the code behaves as expected. Common assertions include:

- assertEqual(a, b): Checks if a == b
- assertTrue(x): Checks if x is True
- assertFalse(x): Checks if x is False
- assertRaises(exception, callable, *args, **kwargs): Checks if callable raises exception

```python
class TestAssertions(unittest.TestCase):
    def test_assertions(self):
        self.assertEqual(3 + 4, 7)
        self.assertTrue(10 > 5)
        self.assertFalse(10 < 5)
        with self.assertRaises(ZeroDivisionError):
            x = 1 / 0
```

### b. Setup and Teardown
- setUp(): Runs before each test method. Use it to prepare the test environment
- tearDown(): Runs after each test method. Use it to clean up resources

```python
class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Initialize a database connection
        self.db = Database()
        self.db.connect()

    def tearDown(self):
        # Close the database connection
        self.db.disconnect()

    def test_query(self):
        result = self.db.query("SELECT * FROM users")
        self.assertIsNotNone(result)
```

### c. Test Suites
A test suite is a collection of test cases. You can group related tests together.

```python
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestMathOperations('test_add'))
    suite.addTest(TestDatabase('test_query'))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
```

### d. Skipping Tests
You can skip tests using the @unittest.skip decorator.

```python
class TestSkip(unittest.TestCase):
    @unittest.skip("Skipping this test")
    def test_skip(self):
        self.fail("This test should be skipped")

    @unittest.skipIf(1 > 0, "Skipping if condition is True")
    def test_skip_if(self):
        self.fail("This test should be skipped if 1 > 0")
```

## 4. Running Tests
You can run tests in several ways:

From the command line:
```bash
python -m unittest test_module.py
```

Using unittest.main():
```python
if __name__ == "__main__":
    unittest.main()
```

Using test discovery:
```bash
python -m unittest discover
```

## 5. Advanced Features

### a. Mocking
The unittest.mock module allows you to replace parts of your system under test with mock objects.

```python
from unittest.mock import patch

class TestMocking(unittest.TestCase):
    @patch('math.sqrt')  # Mock the math.sqrt function
    def test_mock(self, mock_sqrt):
        mock_sqrt.return_value = 10
        result = math.sqrt(4)
        self.assertEqual(result, 10)  # Mocked result
```

### b. Parameterized Tests
You can use libraries like parameterized to run the same test with different inputs.

```python
from parameterized import parameterized

class TestParameterized(unittest.TestCase):
    @parameterized.expand([
        (1, 2, 3),
        (4, 5, 9),
        (0, 0, 0),
    ])
    def test_add(self, a, b, expected):
        self.assertEqual(add(a, b), expected)
```

## 6. Best Practices

- Write small, focused tests: Each test should verify one specific behavior
- Use descriptive test names: Method names like test_add_positive_numbers are more informative
- Avoid dependencies between tests: Tests should be independent and run in any order
- Use mocks for external dependencies: Isolate your code from external systems like databases or APIs
- Run tests frequently: Integrate tests into your development workflow

## 7. Example: Comprehensive Test Case
Here's a complete example that combines all the concepts:

```python
import unittest
from unittest.mock import patch

# Function to be tested
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Test case
class TestMathOperations(unittest.TestCase):
    def setUp(self):
        print("Setting up...")

    def tearDown(self):
        print("Tearing down...")

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(9, 3), 3)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)

    @patch('math.pow', return_value=16)
    def test_mock_pow(self, mock_pow):
        self.assertEqual(math.pow(2, 4), 16)  # Mocked result

    @unittest.skip("Skipping this test")
    def test_skip(self):
        self.fail("This test should be skipped")

# Run the tests
if __name__ == "__main__":
    unittest.main()
```

## 8. Conclusion
The unittest framework is a powerful tool for ensuring the correctness of your Python code. By writing comprehensive tests, you can catch bugs early, improve code quality, and make your codebase more maintainable. Use the concepts and examples above to build robust test suites for your projects.
