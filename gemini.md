# Mastering Unit Testing in Python with `unittest`

**Target Audience:** 
    Python developers with some programming experience who want to improve code quality and reliability through testing.

    This comprehensive guide covers the fundamentals and advanced techniques of unit testing in Python using the built-in `unittest` framework. It aims to equip Python developers with the knowledge to write robust, reliable, and maintainable code.

**Course Objectives:**

*   Understand the fundamental principles of unit testing.
*   Write effective unit tests using the `unittest` framework.
*   Organize test suites and manage test execution.
*   Handle setup and teardown operations within tests.
*   Use assertions to verify expected outcomes.
*   Understand and implement test doubles (mocks and stubs).
*   Integrate testing into a development workflow.

**Course Outline:**

## Table of Contents

1. [Introduction to Unit Testing](#introduction-to-unit-testing)
   * [What is Unit Testing?](#what-is-unit-testing)
   * [Why Unit Testing is Important (The Benefits)](#why-unit-testing-is-important-the-benefits)
   * [The Testing Pyramid](#the-testing-pyramid)
   * [FIRST Principles of Good Unit Tests](#first-principles-of-good-unit-tests)
2. [Getting Started with `unittest`](#getting-started-with-unittest)
   * [The `unittest` Framework](#the-unittest-framework)
   * [Your First Unit Test](#your-first-unit-test)
   * [Running Tests](#running-tests)
3. [Assertion Methods](#assertion-methods)
   * [Commonly Used Assertions](#commonly-used-assertions)
   * [Choosing the Right Assertion](#choosing-the-right-assertion)
4. [Setup and Teardown](#setup-and-teardown)
   * [Purpose](#purpose)
   * [Example](#example)
5. [Organizing Tests](#organizing-tests)
   * [Test Suites](#test-suites)
   * [Test Discovery](#test-discovery)
   * [Best Practices for Organization](#best-practices-for-organization)
6. [Mocking and Test Doubles](#mocking-and-test-doubles)
   * [The Problem with Dependencies](#the-problem-with-dependencies)
   * [Test Doubles](#test-doubles)
   * [`unittest.mock`](#unittestmock)
   * [Mocking Example](#mocking-example)
   * [`patch` as a context manager](#patch-as-a-context-manager)
7. [Advanced Techniques and Best Practices](#advanced-techniques-and-best-practices)
   * [Test-Driven Development (TDD)](#test-driven-development-tdd)
   * [Parameterized Tests (using `subTest`)](#parameterized-tests-using-subtest)
   * [Skipping Tests](#skipping-tests)
   * [Expected Failures](#expected-failures)
   * [Custom Assertions and Test Helpers](#custom-assertions-and-test-helpers)
   * [Dynamic Test Generation](#dynamic-test-generation)
   * [Testing Asynchronous Code](#testing-asynchronous-code)
   * [Performance Testing](#performance-testing)
   * [Property-Based Testing](#property-based-testing)
   * [Fuzz Testing with hypothesis](#fuzz-testing-with-hypothesis)
   * [Handling Flaky Tests](#handling-flaky-tests)
   * [Test Coverage and Quality Metrics](#test-coverage-and-quality-metrics)
   * [Integration with CI/CD](#integration-with-cicd)
8. [Additional Resources](#additional-resources)


## Module 1: Introduction to Unit Testing

*   **What is Unit Testing?**
    *   Definition:  Testing individual units (usually functions or methods) of code in isolation.
    *   Purpose:
        *   Early bug detection.
        *   Facilitates refactoring (changing code without changing functionality).
        *   Acts as documentation (tests show how code *should* work).
        *   Improved code design (testable code tends to be modular and well-structured).
        *   Increased confidence in code changes.
    *   Example: Imagine a simple calculator.  A unit test for the `add` function would check that `add(2, 3)` returns 5.  We're not testing the entire calculator, just that one specific function.

*   **Why Unit Testing is Important (The Benefits)**
    *   **Reduces Defects:** Catching errors early saves time and money compared to finding them later in the development cycle (or worse, in production).
    *   **Improves Code Quality:** The act of writing tests forces you to think about the design of your code.  If a function is difficult to test, it's often a sign that it's doing too much and should be broken down.
    *   **Facilitates Regression Testing:** When you make changes to your code, your unit tests act as a safety net.  They ensure that existing functionality hasn't been broken by the new code (regression).
    *   **Living Documentation:** Well-written tests clearly demonstrate how a function or class is intended to be used.  They provide concrete examples.

*   **The Testing Pyramid**
    *   Concept:  A visual representation of the ideal distribution of tests.  Unit tests form the broad base (most numerous), followed by integration tests (testing how units work together), and a smaller number of end-to-end (E2E) tests (testing the entire application).
    *   Explanation:  Unit tests are fast and cheap to run, so you should have many of them.  E2E tests are slow and brittle, so you should have fewer.  Integration tests are in the middle.
    *    Analogy: Like building a house, a strong foundation (unit tests) is crucial.

*   **FIRST Principles of Good Unit Tests**
    *   **F**ast: Tests should run quickly.  Slow tests discourage frequent running.
    *   **I**solated:  Tests should not depend on or affect each other.  The outcome of one test should not influence another.
    *   **R**epeatable:  Running the same test multiple times should always produce the same result, regardless of the environment.
    *   **S**elf-validating: Tests should clearly indicate success or failure (pass/fail) without manual inspection.
    *   **T**imely: Tests should be written *before* or alongside the code they are testing (Test-Driven Development, TDD).

## Module 2: Getting Started with `unittest`

*   **The `unittest` Framework**
    *   Introduction: Python's built-in testing framework, inspired by JUnit (from Java).
    *   Key Components:
        *   `unittest.TestCase`:  The base class for creating test cases.
        *   Assertion Methods:  Methods like `assertEqual`, `assertTrue`, `assertRaises` to check expected outcomes.
        *   Test Runners: Tools to discover and execute tests (e.g., `unittest.main()`, command-line tools).

*   **Your First Unit Test**

    ```python
    # my_module.py (The code to be tested)
    def add(x, y):
        """Adds two numbers."""
        return x + y

    def subtract(x, y):
        """Subtracts two numbers."""
        return x - y

    # test_my_module.py (The test file)
    import unittest
    from my_module import add, subtract  # Import the functions to test

    class TestMyModule(unittest.TestCase):  # Inherit from unittest.TestCase

        def test_add(self):
            """Test the add function."""
            self.assertEqual(add(2, 3), 5)  # Assertion: check equality
            self.assertEqual(add(-1, 1), 0)
            self.assertEqual(add(-1, -1), -2)

        def test_subtract(self):
            """Test the subtract function."""
            self.assertEqual(subtract(5, 2), 3)
            self.assertEqual(subtract(1, -1), 2)

    if __name__ == '__main__':
        unittest.main()  # Run the tests
    ```

    *   **Explanation:**
        *   We import `unittest` and the functions we want to test.
        *   We create a class that inherits from `unittest.TestCase`.
        *   Each test is a method within this class, starting with the prefix `test_`.
        *   We use `self.assertEqual()` to check if the result of the function call is equal to the expected value.
        *   `unittest.main()` discovers and runs all the test methods in the class.

*   **Running Tests**
    *   **From the Command Line:**
        *   `python -m unittest test_my_module.py` (Runs tests in the specified file)
        *   `python -m unittest discover` (Discovers and runs tests in the current directory and subdirectories)
        *   `python -m unittest discover -s tests` (Specifies a directory named "tests" to search)
        *   `python -m unittest -v test_my_module.py` (Verbose mode - more output)
    *   **From within the file**
        * `if __name__ == "__main__": unittest.main()`

    *   **Interpreting Test Results:**
        *   `.` (period):  Test passed.
        *   `F`:  Test failed (an assertion failed).
        *   `E`:  Error occurred (exception raised outside of an assertion).
        *   `s`: Test was skipped

## Module 3:  Assertion Methods

*   **Commonly Used Assertions**

    ```python
    import unittest

    class TestAssertions(unittest.TestCase):

        def test_equal(self):
            self.assertEqual(2 + 2, 4)  # Checks if two values are equal
            self.assertNotEqual(2 + 2, 5) # Checks if two values are not equal

        def test_true_false(self):
            self.assertTrue(True)  # Checks if a value is True
            self.assertFalse(False) # Checks if a value is False

        def test_is_none(self):
            self.assertIsNone(None) # Checks if a value is None
            self.assertIsNotNone(1)  # Checks if a value is not None.

        def test_in(self):
            self.assertIn(1, [1, 2, 3])  # Checks if an item is in a sequence
            self.assertNotIn(4, [1, 2, 3]) # Checks if an item is not in a sequence.

        def test_instance_of(self):
            self.assertIsInstance("hello", str)  # Checks if an object is an instance of a class
            self.assertNotIsInstance(5, str)  # Checks the opposite of the above

        def test_raises(self):
            with self.assertRaises(ValueError):  # Checks if a specific exception is raised
                raise ValueError("This is a test exception")

            with self.assertRaises(TypeError):
                int("a")

            with self.assertRaisesRegex(ValueError, "invalid literal"):
                int("abc") # Check if exception message matches regular expresion

    if __name__ == '__main__':
        unittest.main()

    ```
    * **Explanation:**
        *  `assertEqual(a, b)`: Checks if `a == b`.
        *  `assertNotEqual(a, b)`: Checks if `a != b`.
        *  `assertTrue(x)`: Checks if `bool(x)` is True.
        *  `assertFalse(x)`: Checks if `bool(x)` is False.
        *  `assertIs(a, b)`: Checks if `a is b` (same object in memory).
        *  `assertIsNot(a, b)`: Checks if `a is not b`.
        *  `assertIsNone(x)`: Checks if `x is None`.
        *  `assertIsNotNone(x)`: Checks if `x is not None`.
        *  `assertIn(a, b)`: Checks if `a in b` (for lists, tuples, sets, etc.).
        *  `assertNotIn(a, b)`: Checks if `a not in b`.
        *  `assertIsInstance(a, b)`: Checks if `isinstance(a, b)`.
        *  `assertNotIsInstance(a, b)`: Checks if `not isinstance(a, b)`.
        *  `assertRaises(exception, callable, *args, **kwargs)`:  Checks if calling `callable` with the given arguments raises the specified `exception`.  This is crucial for testing error handling. The `with` statement ensures the exception is properly caught and handled.
        *   `assertRaisesRegex`: Same as `assertRaises`, but also checks if the exception message matches a regular expression.

*   **Choosing the Right Assertion:** Use the most specific assertion possible.  This makes your tests more readable and provides better error messages.  For example, use `assertIsNone` instead of `assertEqual(x, None)`.

## Module 4: Setup and Teardown

*   **Purpose:**
    *   `setUp()`:  Executed *before* each test method.  Used to create resources or set up a consistent environment for each test.
    *   `tearDown()`: Executed *after* each test method, even if the test fails. Used to clean up resources (e.g., close files, delete temporary data).
    *   `setUpClass()`: Executed *once* before all tests in a class. Class method, uses `@classmethod` decorator.
    *   `tearDownClass()`: Executed *once* after all tests in a class. Class method, uses `@classmethod` decorator.
    *  `setUpModule()`: Function that's called *once* when the module is loaded.
    *  `tearDownModule()`: Function that's called *once* when the module is unloaded.

*   **Example:**

    Imagine you're testing a database connection.

    setUp(): Would establish a connection before each individual test.
    tearDown(): Would close that connection after each individual test.
    setUpClass(): Might create the database table structure once before all tests start.
    tearDownClass(): Might drop that table structure once after all tests are finished.

    ```python
    class DatabaseTest(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls.db = DatabaseConnection()
            cls.db.create_schema()
        
        def setUp(self):
            self.transaction = self.db.begin_transaction()
        
        def tearDown(self):
            self.transaction.rollback()
        
        @classmethod
        def tearDownClass(cls):
            cls.db.close()
    ```

    ```python
    import unittest
    import tempfile
    import os

    class TestFileOperations(unittest.TestCase):

        @classmethod
        def setUpClass(cls):
            print("Setting up the class...")
            # Create a class-level resource if needed.
            cls.global_resource = "This is a shared resource"

        @classmethod
        def tearDownClass(cls):
            print("Tearing down the class...")
            # Clean up the class-level resource.
            cls.global_resource = None  # Or any other cleanup

        def setUp(self):
            print("Setting up the test...")
            # Create a temporary file for each test
            self.temp_file = tempfile.NamedTemporaryFile(delete=False)
            self.file_path = self.temp_file.name

        def tearDown(self):
            print("Tearing down the test...")
            # Close and delete the temporary file
            self.temp_file.close()
            os.remove(self.file_path)

        def test_write_to_file(self):
            with open(self.file_path, 'w') as f:
                f.write("Hello, world!")
            with open(self.file_path, 'r') as f:
                content = f.read()
            self.assertEqual(content, "Hello, world!")

        def test_read_from_file(self):
            # Example where we pre-populate the file in setUp
            with open(self.file_path, 'w') as f:
                f.write("Pre-existing content")
            with open(self.file_path, 'r') as f:
                content = f.read()
            self.assertEqual(content, "Pre-existing content")

    if __name__ == '__main__':
        unittest.main(verbosity=2)

    ```

    *   **Explanation:**
        *   `setUp()` creates a temporary file *before each test*.
        *   `tearDown()` closes and deletes the temporary file *after each test*. This ensures that tests don't interfere with each other and that we clean up after ourselves.
        *   `setUpClass` and `tearDownClass` are used for setup/teardown that only needs to happen once per test class, which can be more efficient.

## Module 5:  Organizing Tests

*   **Test Suites:**
    *   Concept:  A collection of test cases or other test suites.  Useful for grouping related tests.
    *   Example:

        ```python
        import unittest
        # Assume you have TestClass1 and TestClass2 defined in other files.
        from test_module1 import TestClass1
        from test_module2 import TestClass2

        def suite():
            suite = unittest.TestSuite()
            suite.addTest(unittest.makeSuite(TestClass1))  # Add all tests from TestClass1
            suite.addTest(unittest.makeSuite(TestClass2))
            # Or add individual tests:
            # suite.addTest(TestClass1('test_method_name'))
            return suite

        if __name__ == '__main__':
            runner = unittest.TextTestRunner()
            runner.run(suite())

        ```
        * **Explanation:**
            *  `unittest.TestSuite()` creates a test suite.
            *  `suite.addTest()` adds tests to the suite.
            *  `unittest.makeSuite(TestClass)` creates a suite containing all tests in `TestClass`.
            *  `unittest.TextTestRunner` runs the suite and provides text output.

*   **Test Discovery:**
    *   `unittest` can automatically discover and run tests.  This is usually the preferred method.
    *   Command-line: `python -m unittest discover` (finds all files matching `test*.py`)
    *   Customize discovery: `python -m unittest discover -s test_directory -p '*_test.py'` (searches in `test_directory` for files ending in `_test.py`)

    * Files must match pattern: `test*.py`
    * Classes must inherit from `unittest.TestCase`
    * Methods must start with `test_`

*   **Best Practices for Organization:**
    *   **Separate Test Files:** Keep your tests in separate files from your production code. This keeps things clean and organized.
    *   **Mirror Directory Structure:**  Often, the structure of your test directory mirrors the structure of your source code directory.  For example, if you have `my_project/module1/file1.py`, your tests might be in `my_project/tests/module1/test_file1.py`.
    *   **Use Descriptive Names:**  Test file names, class names, and method names should clearly indicate what is being tested.
    *   **`__init__.py` files:** Make sure any directory containing tests has an `__init__.py` file (even if it's empty).  This tells Python that the directory is a package.

## Module 6:  Mocking and Test Doubles

*   **The Problem with Dependencies:**
    *   Sometimes, a unit you want to test depends on other units (e.g., a function that makes a network request or interacts with a database).
    *   Directly testing these dependencies can be problematic:
        *   Slow (network requests, database access).
        *   Unreliable (external services might be down).
        *   Difficult to set up (database connections, specific data).
        *   Violates the "isolated" principle of unit testing.

*   **Test Doubles:**
    *   Concept:  Replacing real dependencies with "fake" objects that you control.
    *   Types of Test Doubles:
        *   **Mocks:**  Objects that record interactions.  You can verify that specific methods were called with expected arguments.
        *   **Stubs:**  Objects that provide pre-programmed responses to method calls.  They don't record interactions.
        *   **Fakes:** Simplified implementations of a dependency (e.g., an in-memory database).
        *   **Spies:**  Like mocks, but they also allow the original method to be called.
        *   **Dummies:** Objects that are passed around but never actually used (e.g., to satisfy a function signature).

*   **`unittest.mock` (or `mock` in Python 2)**
    *   Introduction:  A powerful library for creating mocks and stubs in Python.
    *   Key Classes:
        *   `Mock`:  The basic mock object.
        *   `MagicMock`:  A `Mock` subclass that automatically implements magic methods (like `__str__`, `__len__`).
        *   `patch`:  A decorator or context manager used to replace real objects with mocks.

*   **Mocking Example:**

    ```python
    import unittest
    from unittest.mock import Mock, patch

    # my_module.py (The code to be tested)
    import requests  # We'll mock this

    def get_data_from_api(url):
        """Fetches data from an API."""
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()

    # test_my_module.py (The test file)
    # from my_module import get_data_from_api

    class TestGetDataFromApi(unittest.TestCase):

        @patch('my_module.requests.get')  # Replace requests.get with a mock
        def test_get_data_from_api_success(self, mock_get):
            # Configure the mock to return a specific response
            mock_response = Mock()
            mock_response.json.return_value = {'data': 'Mocked data'}
            mock_response.status_code = 200 #added to fix missing status code
            mock_get.return_value = mock_response
            # Call the function being tested
            data = get_data_from_api('https://example.com/api')

            # Assertions
            mock_get.assert_called_once_with('https://example.com/api')  # Check if get was called
            self.assertEqual(data, {'data': 'Mocked data'})
            mock_response.raise_for_status.assert_not_called() # Check raise_for_status

        @patch('my_module.requests.get')
        def test_get_data_from_api_failure(self, mock_get):
            # Configure the mock to raise an exception
            mock_get.side_effect = requests.exceptions.RequestException("Mocked error")

            # Assert that the exception is raised
            with self.assertRaises(requests.exceptions.RequestException):
                get_data_from_api('https://example.com/api')

            mock_get.assert_called_once_with('https://example.com/api')

        ################################
        @patch('module.function')
        def test_function(self, mock_function):
            mock_function.return_value = 'mocked'
            # Test code here
            mock_function.assert_called_once()

    if __name__ == '__main__':
        unittest.main(verbosity=2)
    ```
    * **Explanation:**
        *   `@patch('my_module.requests.get')`:  This decorator replaces the `requests.get` function *within the `my_module` module* with a `Mock` object. The mock is passed as an argument (`mock_get`) to the test method.
        *   `mock_get.return_value`:  We set the return value of the mock.  When `requests.get` is called (which is now actually `mock_get`), it will return our mock response object.
        *   `mock_get.side_effect`: We can make the mock raise an exception, simulate a network error.
        *   `mock_get.assert_called_once_with(...)`: We verify that the mock was called with the expected arguments.
        *   `mock_response.json.return_value`: We configure the `json()` method of our mock response to return a specific dictionary.
        *   `mock_response.raise_for_status.assert_not_called()`: Verifies that the raise_for_status() method was not called.
        *  The `test_get_data_from_api_failure` test demonstrates how to test for exceptions.

* **`patch` as a context manager:**

    ```python
     class TestGetDataFromApi(unittest.TestCase):
        def test_get_data_from_api_success_context_manager(self):
            with patch('my_module.requests.get') as mock_get:
                mock_response = Mock()
                mock_response.json.return_value = {'data': 'Mocked data'}
                mock_response.status_code = 200
                mock_get.return_value = mock_response

                data = get_data_from_api('https://example.com/api')

                mock_get.assert_called_once_with('https://example.com/api')
                self.assertEqual(data, {'data': 'Mocked data'})
                mock_response.raise_for_status.assert_not_called()  # Check raise_for_status
    ```

    *   Using `patch` as a context manager (`with patch(...) as ...`) is often cleaner, especially for simple mocks.  The patching is automatically undone when the `with` block ends.

* **Context Managers vs Decorators**
    ```python
    # Using context manager
    with patch('module.ClassName') as mock_class:
        instance = mock_class.return_value
        instance.method.return_value = 'mocked'
        
    # Using decorator
    @patch('module.ClassName')
    def test_function(self, mock_class):
        instance = mock_class.return_value
        instance.method.return_value = 'mocked'
    ```

    - **Mock Side Effects**
    ```python
    def side_effect_func(arg):
        if arg < 0:
            raise ValueError("Negative value")
        return arg * 2

    mock_obj.method.side_effect = side_effect_func
    ```

## Module 7: Advanced Topics and Best Practices

*   **Table of Contents**
    1. [Test-Driven Development (TDD)](#test-driven-development-tdd)
    2. [Parameterized Tests](#parameterized-tests)
    3. [Skipping Tests](#skipping-tests)
    4. [Expected Failures](#expected-failures)
    5. [Custom Assertions](#custom-assertions)
    6. [Dynamic Test Generation](#dynamic-test-generation)
    7. [Testing Asynchronous Code](#testing-asynchronous-code)
    8. [Performance Testing](#performance-testing)
    9. [Property-Based Testing](#property-based-testing)
    10. [Test Coverage](#test-coverage)
    11. [CI/CD Integration](#cicd-integration)

*   **Test-Driven Development (TDD):**
    *   Process:
        1.  **Red:** Write a failing test *before* writing any production code.
        2.  **Green:** Write the *minimum* amount of code to make the test pass.
        3.  **Refactor:** Clean up and improve the code, while keeping the tests passing.
    *   Benefits:
        *   Ensures 100% test coverage (in theory).
        *   Leads to better code design (because you think about testability from the start).
        *   Provides immediate feedback.
        * Forces you to think about requirements before implementation.
        * Example (simple addition function, following TDD):

            ```python
            # test_tdd_example.py (Start here!)
            import unittest
            # from tdd_example import add  # Uncomment after the first test fails

            class TestAdd(unittest.TestCase):
                def test_add_two_positive_numbers(self):
                    self.assertEqual(add(2, 3), 5)  # This will fail initially

            if __name__ == '__main__':
                unittest.main()

            # --- (Run the test - it fails) ---

            # tdd_example.py (Now write the code)
            def add(x, y):
                return x + y

            # --- (Run the test again - it passes) ---

            # Now you might add more tests (negative numbers, floats, etc.)
            # and refactor the add function if needed, always keeping the tests green.
            ```

*   **Parametrized Tests (using `subTest`)**
    *   Avoid code duplication when testing the same logic with different inputs.
    * Example:

    ```python
    import unittest

    def calculate_discount(price, discount_percentage):
        if not (0 <= discount_percentage <= 100):
            raise ValueError("Discount percentage must be between 0 and 100")
        return price * (1 - discount_percentage / 100)

    class TestCalculateDiscount(unittest.TestCase):
        def test_calculate_discount(self):
            test_cases = [
                (100, 0, 100),  # (price, discount, expected)
                (100, 10, 90),
                (100, 50, 50),
                (100, 100, 0),
                (50, 25, 37.5),
            ]
            for price, discount, expected in test_cases:
                with self.subTest(price=price, discount=discount):
                    self.assertEqual(calculate_discount(price, discount), expected)

        def test_invalid_discount(self):
            with self.assertRaises(ValueError):
                calculate_discount(100,-10)
            with self.assertRaises(ValueError):
                calculate_discount(100,110)

        #######################
        @parameterized.expand([
            ("valid_case", "input1", True),
            ("edge_case", "", False),
            ("error_case", None, False)
        ])
        def test_validation(self, name, input_value, expected):
            result = validate_input(input_value)
            self.assertEqual(result, expected)

    if __name__ == '__main__':
        unittest.main(verbosity=2)

    ```
    *   **Explanation:**
        *  `subTest`: Creates a sub-test within a test method.  If one sub-test fails, the others still run. The `with self.subTest(...)` block allows you to run the same assertion logic with different inputs. Each iteration of the loop is treated as a separate sub-test.  This makes the test output more informative.

*   **Skipping Tests**
    *   `@unittest.skip(reason)`:  Skips a test unconditionally.
    *   `@unittest.skipIf(condition, reason)`:  Skips a test if the `condition` is true.
    *   `@unittest.skipUnless(condition, reason)`: Skips a test unless the `condition` is true.
    *   `unittest.SkipTest(reason)`:  Raise this exception within a test method to skip it.

    ```python
    import unittest
    import sys

    class TestSkipping(unittest.TestCase):

        @unittest.skip("This test is always skipped")
        def test_always_skipped(self):
            self.fail("This should never be executed")

        @unittest.skipIf(sys.platform.startswith("win"), "Only runs on non-Windows platforms")
        def test_skip_on_windows(self):
            pass  # Test logic for non-Windows platforms

        @unittest.skipUnless(sys.version_info >= (3, 8), "Requires Python 3.8 or higher")
        def test_python_version_dependent(self):
            pass  # Test logic for Python 3.8+

        def test_conditional_skip(self):
            if some_condition:  # Replace with your actual condition
                raise unittest.SkipTest("Skipping because some_condition is true")
            # Test logic that runs if some_condition is false

    ```
    *   **Explanation:**
        Skip decorators:
        * `@unittest.skip(reason)`: Always skip the test
        * `@unittest.skipIf(condition, reason)`: Skip if condition is true
        * `@unittest.skipUnless(condition, reason)`: Skip unless condition is true
        * `unittest.SkipTest`: Raise within test to skip dynamically

*   **Expected Failures**
    *   `@unittest.expectedFailure`:  Marks a test as expected to fail.  If it passes, it's considered an unexpected success. Useful for documenting known bugs that haven't been fixed yet.

    ```python
    import unittest

    class TestExpectedFailure(unittest.TestCase):

        @unittest.expectedFailure
        def test_known_bug(self):
            self.assertEqual(1, 2)  # This test will fail, but it's marked as expected

    ```
    *   **Explanation:**
        Use cases for expected failures:
        * Documenting known bugs before fixes
        * Tracking regressions in progress
        * Testing negative scenarios
        * Marking tests that depend on unimplemented features

*   **Custom Assertions**
    Create reusable assertion methods:
    You can create custom assertion methods within your test classes to improve readability and reduce code duplication.

    ```python
    class CustomAssertions(unittest.TestCase):
        def assertDictContainsSubset(self, expected, actual):
            """Assert that actual dict contains all items from expected."""
            for key, value in expected.items():
                self.assertIn(key, actual)
                self.assertEqual(actual[key], value)

        def assertValidResponse(self, response):
            """Custom assertion for API responses."""
            self.assertEqual(response.status_code, 200)
            self.assertIn('data', response.json())
    ```

*   **Dynamic Test Generation**
    Generate tests programmatically:
    Instead of manually writing numerous similar tests, you can dynamically generate them using metaprogramming techniques.

    ```python
    import unittest

    def dynamic_test_generator(value, expected):
        def test(self):
            self.assertEqual(value + 2, expected)
        return test

    class TestDynamic(unittest.TestCase):
        pass

    test_cases = [(2, 4), (5, 7), (-1, 1)]
    for index, (val, exp) in enumerate(test_cases):
        setattr(TestDynamic, f"test_dynamic_case_{index}",
                dynamic_test_generator(val, exp))
    ```
    This uses setattr to add test methods to the TestDynamic class dynamically. This approach is useful when you have a large number of similar test cases.

*   **Testing Asynchronous Code**
    Handle async operations:
    When working with asynchronous code (using async and await), you need special handling in your tests.

    ```python
    import unittest
    import asyncio

    class AsyncTests(unittest.TestCase):
        async def async_setup(self):
            await asyncio.sleep(0.1)
            self.client = "Async Client"
            # self.client = await create_async_client()

        async def test_async_operation(self):
            await self.async_setup()
            await asyncio.sleep(0.1)
            result = self.client
            # result = await self.client.fetch_data()
            self.assertIsNotNone(result)

        def test_async_wrapper(self):
            asyncio.run(self.test_async_operation())
    ```
    *   **Explanation:**
        Key Points:
        *  Use async def to declare asynchronous test functions.
        *  Use await inside the async test to call other async functions.
        *  Use asyncio.run() to run the async test function within a synchronous test method.

*   **Performance Testing**
    Measure execution time:

    ```python
    import time
    import unittest

    def time_test(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} took {end - start:.2f} seconds")
            return result
        return wrapper

    class MyTest(unittest.TestCase):
        @time_test
        def test_slow_function(self):
        time.sleep(1)
        self.assertEqual(1,1)
    ```

*   **Property-Based Testing**
    Using Hypothesis for property testing:
    Property-based testing involves generating random inputs to test properties of your code, rather than using fixed examples. The hypothesis library is a popular choice for this.

    ```python
    from hypothesis import given, strategies as st
    import unittest

    # Using Hypothesis
    class PropertyTests(unittest.TestCase):
        @given(st.lists(st.integers()))
        def test_sort_idempotent(self, lst):
            """Test that sorting twice gives same result as sorting once."""
            once = sorted(lst)
            twice = sorted(sorted(lst))
            self.assertEqual(once, twice)

    # Fuzz Testing with hypothesis
    class TestFuzz(unittest.TestCase):
        @given(st.integers(), st.integers())
        def test_fuzz_addition(self, a, b):
            self.assertEqual(a + b, b + a)  # Commutative property
    # Key Benefit: Catches edge cases that manual testing might miss.

    # Handling Flaky Tests
    import unittest
    from flaky import flaky

    @flaky(max_runs=3, min_passes=1)
    class TestFlaky(unittest.TestCase):
        def test_may_fail(self):
            import random
            self.assertTrue(random.choice([True, False]))
    # Key Benefit: Useful when testing APIs, time-sensitive features, or race conditions.
    ```

*   **Test Coverage and Quality Metrics**
    Using coverage.py:
    Code Coverage: Tools like `coverage.py` measure which lines of your code are executed during test runs. This helps identify gaps in test coverage.  High coverage is a good indicator, but it doesn't guarantee that your tests are *effective* (they might not be testing the right things).

    ```bash
    pip install coverage
    coverage run -m unittest discover   # Run tests with coverage
    coverage report -m                  # Show coverage report
    coverage html                       # Generate HTML report
    ```

    Configure coverage (.coveragerc): You can configure coverage to exclude certain lines or files.

    ```ini
    # Coverage configuration (.coveragerc)
    [run]
    branch = True
    source = your_package

    [report]
    exclude_lines =
        pragma: no cover
        def __repr__
        raise NotImplementedError
    ```

*   **CI/CD Integration**
    Example GitHub Actions workflow:
    Continuous Integration/Continuous Deployment (CI/CD) pipelines automate the process of building, testing, and deploying code. Integrating unit tests into a CI/CD pipeline (e.g., Jenkins, Travis CI, GitHub Actions) ensures that tests are run automatically whenever code changes are pushed to the repository, providing rapid feedback.

    ```yaml
    name: Python Tests
    on: [push, pull_request]

    jobs:
    test:
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@v3
        - name: Set up Python
            uses: actions/setup-python@v4
            with:
            python-version: '3.x'
        - name: Install dependencies
            run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
        - name: Run Tests
            run: python -m unittest discover
    ```
    *   **Explanation:**
        *  This GitHub Actions workflow runs tests automatically on every push or pull request to the repository. Other CI/CD platforms (e.g., Jenkins, Travis CI, CircleCI) have similar mechanisms.

*   **Fixtures (External Resources):** 
    While `setUp` and `tearDown` are great for managing simple resources, sometimes you need more complex setup or teardown logic, or you need to share resources between test classes. While `unittest` doesn't have a built-in "fixtures" system like pytest, you can achieve similar functionality using class-level setup/teardown and helper functions.  Consider using `pytest` for more advanced fixture management.

*   **Testing Design Patterns** 
    Test Doubles Pattern
    ```python
    class TestDouble:
        def __init__(self, test_case):
            self.test_case = test_case
            self.calls = []
            
        def record_call(self, *args, **kwargs):
            self.calls.append((args, kwargs))
            
        def verify_calls(self, expected_calls):
            self.test_case.assertEqual(
                self.calls,
                expected_calls
            )
    ```

## Best Practices Summary
1. **Test Organization**
   - Group related tests
   - Use descriptive names
   - Maintain test independence

2. **Performance Considerations**
   - Mock expensive operations
   - Use appropriate fixtures
   - Consider test parallelization

3. **Maintenance Tips**
   - Regular test cleanup
   - Documentation updates
   - Coverage monitoring

## Additional Resources

* [unittest Documentation](https://docs.python.org/3/library/unittest.html)
* [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
* [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
* [Coverage.py Documentation](https://coverage.readthedocs.io/)
* [Parameterized Documentation](https://github.com/wolever/parameterized)
* [Flaky Documentation](https://github.com/box/flaky)
* [Python Testing Guide](https://docs.python-guide.org/writing/tests/)