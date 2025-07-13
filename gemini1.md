# Mastering Unit Testing in Python with unittest

## Slide 1: Title Slide
**Title:** Mastering Unit Testing in Python with unittest  
**Subtitle:** Write Robust and Reliable Code
name of extension for show markdown in vscode
*Speaker Notes:*
> Welcome, everyone! Today, we're going to dive deep into unit testing in Python using the built-in unittest framework. By the end of this presentation, you'll have a solid understanding of how to write effective tests, organize your test suites, and use mocking to isolate your code.

## Slide 2: What is Unit Testing?
* Testing individual units of code (functions, methods) in isolation
* Focuses on verifying the smallest testable parts of an application
* Like testing individual gears in a machine, not the whole machine at once

*Speaker Notes:*
> Unit testing is all about breaking down your code into its smallest components and testing each one independently. Think of it like quality control for individual parts before assembling a larger product.
> 
> We're isolating these units to make sure they behave exactly as we expect.

## Slide 3: Why Unit Testing? (Benefits)
* **Reduces Defects:** Find bugs early, saving time and money
* **Improves Code Quality:** Forces better design and modularity
* **Facilitates Refactoring:** Provides a safety net for code changes
* **Living Documentation:** Tests show how code should work
* **Increased Confidence:** Make changes without fear of breaking things

*Speaker Notes:*
> Unit testing isn't just extra work; it's an investment that pays off significantly.
> 
> Early bug detection is crucial. Fixing a bug in production is much more expensive than fixing it during development.
> 
> Tests act as a safety net, allowing you to refactor and improve your code without worrying about introducing regressions.
> 
> Well-written tests are like living documentation, providing clear examples of how your code is supposed to be used.

## Slide 4: The Testing Pyramid
* Base (Largest): Unit Tests
* Middle: Integration Tests
* Top (Smallest): End-to-End (E2E) Tests

**Key Points:**
* Unit tests should form the foundation of your testing strategy
* Integration tests check how units work together
* E2E tests validate the entire application flow

*Speaker Notes:*
> The testing pyramid illustrates the ideal distribution of tests.
> 
> Unit tests are fast, cheap, and easy to write, so we should have a lot of them.
> 
> E2E tests are slow, brittle, and expensive, so we should have fewer of them.
> 
> Integration tests fall somewhere in between.

## Slide 5: FIRST Principles of Good Unit Tests
* **Fast:** Run quickly
* **Isolated:** Independent of each other
* **Repeatable:** Same result every time
* **Self-validating:** Clear pass/fail
* **Timely:** Written before/alongside code (TDD)

*Speaker Notes:*
> These principles are guidelines for writing effective unit tests.
> 
> Fast tests encourage frequent execution, leading to faster feedback.
> 
> Isolation ensures that tests don't interfere with each other.
> 
> Repeatability is essential for reliable results.
> 
> Self-validation means we don't need to manually inspect the results.
> 
> Timely test writing promotes better code design.

## Slide 6: Introducing unittest
* Python's built-in testing framework
* Inspired by JUnit (Java)
* Provides tools for:
  * Creating test cases (unittest.TestCase)
  * Making assertions (e.g., assertEqual)
  * Running tests (test runners)

*Speaker Notes:*
> unittest is readily available; you don't need to install anything extra.
> 
> It's a powerful and versatile framework for writing all kinds of unit tests.

## Slide 7: Your First Unit Test
```python
# my_module.py
def add(x, y):
    return x + y

# test_my_module.py
import unittest
from my_module import add

class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

if __name__ == '__main__':
    unittest.main()
```

*Speaker Notes:*
> Here's a simple example of a function and its corresponding test.
> 
> We create a class that inherits from unittest.TestCase.
> 
> Test methods start with test_.
> 
> We use self.assertEqual to check the expected result.
> 
> unittest.main() runs the tests.

## Slide 8: Running Tests
**From the Command Line:**
```bash
python -m unittest test_my_module.py
python -m unittest discover
python -m unittest discover -s tests -p '*_test.py'
python -m unittest -v test_my_module.py
```

**From within File:**
```python
if __name__ == '__main__':
    unittest.main()
```

*Speaker Notes:*
> You can run tests from the command line or directly within your test file.
> 
> The discover option automatically finds tests.
> 
> Verbose mode (-v) provides more detailed output.
> 
> Explain the meaning of ., F, E, and s in the test output.

## Slide 9: Assertion Methods
Common assertions with examples:
```python
self.assertEqual(a, b)      # Checks a == b
self.assertTrue(x)          # Checks bool(x) is True
self.assertIsNone(x)        # Checks x is None
self.assertIn(a, b)         # Checks a in b
self.assertRaises(Exception, callable, *args, **kwargs)  # Checks for exceptions
```

*Speaker Notes:*
> Assertions are the heart of your tests; they verify the expected behavior.
> 
> Use the most specific assertion possible for better readability and error messages.
> 
> Especially emphasize assertRaises for testing error handling.

## Slide 10: assertRaises Example
```python
import unittest

def divide(x, y):
    if y == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return x / y

class TestDivide(unittest.TestCase):
    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)
```

*Speaker Notes:*
> It's crucial to test how your code handles errors.
> 
> The with self.assertRaises(...) context manager ensures the exception is caught.
> 
> If the expected exception is not raised, the test will fail.

## Slide 11: Setup and Teardown
* `setUp()`: Runs before each test method
* `tearDown()`: Runs after each test method (even if it fails)
* `setUpClass()`: Runs once before all tests in a class (@classmethod)
* `tearDownClass()`: Runs once after all tests in a class (@classmethod)

*Speaker Notes:*
> Setup and teardown methods ensure that each test starts in a consistent and clean state.
> 
> This prevents tests from interfering with each other.
> 
> tearDown is crucial for cleaning up resources, even if a test fails.

## Slide 12: Setup and Teardown Example
```python
import unittest
import tempfile
import os

class TestFileOps(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.file_path = self.temp_file.name

    def tearDown(self):
        self.temp_file.close()
        os.remove(self.file_path)

    def test_write_to_file(self):
        # ... (test logic) ...
```

*Speaker Notes:*
> This example shows how to create and delete a temporary file for each test.
> 
> The setUp method creates the file, and tearDown cleans it up.

## Slide 13: Organizing Tests
* Separate Test Files: Keep tests separate from production code
* Mirror Directory Structure: Organize test files similarly to your source code
* Descriptive Names: Use clear names for files, classes, and methods
* Test Suites: Group related tests together
* `__init__.py`: Include in test directories to make them packages

*Speaker Notes:*
> Good organization is essential for maintainability, especially as your project grows.
> 
> Mirroring the directory structure makes it easy to find the tests for a specific module.
> 
> Test suites can help you run specific groups of tests.

## Slide 14: Mocking - Isolating Dependencies
**Problem:** Testing code with external dependencies (network, database, etc.)
**Solution:** Replace dependencies with "test doubles" (mocks, stubs)

**Benefits:**
* Faster tests
* More reliable tests (no external dependencies)
* Control over dependency behavior

*Speaker Notes:*
> Mocking is a powerful technique for isolating your units of code.
> 
> We replace real dependencies with controlled objects, allowing us to focus on the logic of the unit we're testing.

## Slide 15: unittest.mock
* Built-in library for creating mocks and stubs
* Key classes:
  * `Mock`: The basic mock object
  * `MagicMock`: Handles magic methods automatically
  * `patch`: Decorator/context manager for replacing objects

*Speaker Notes:*
> unittest.mock provides everything you need to create sophisticated mocks.
> 
> patch is a very convenient way to replace real objects with mocks.

## Slide 16: Mocking Example (Part 1)
```python
# my_module.py
import requests

def get_data_from_api(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

*Speaker Notes:*
> This function fetches data from an API. We want to test it without making actual network requests.

## Slide 17: Mocking Example (Part 2)
```python
import unittest
from unittest.mock import Mock, patch
from my_module import get_data_from_api

class TestGetData(unittest.TestCase):
    @patch('my_module.requests.get')
    def test_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'data': 'Mocked'}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        data = get_data_from_api('https://example.com')
        
        mock_get.assert_called_once_with('https://example.com')
        self.assertEqual(data, {'data': 'Mocked'})
```

*Speaker Notes:*
> We use @patch to replace requests.get with a mock.
> 
> We configure the mock to return a specific response.
> 
> We call the function and make assertions.
> 
> We verify that the mock was called with the correct arguments.

## Slide 18: Mocking Example - Handling Exceptions
```python
@patch('my_module.requests.get')
def test_failure(self, mock_get):
    mock_get.side_effect = requests.exceptions.RequestException()
    with self.assertRaises(requests.exceptions.RequestException):
        get_data_from_api('https://example.com')
```

*Speaker Notes:*
> We can also use side_effect to make the mock raise an exception.
> 
> This allows us to test how our code handles errors from the API.

## Slide 19: patch as a Context Manager
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
            mock_response.raise_for_status.assert_not_called()
```

*Speaker Notes:*
> You can also use patch as a context manager, which can be cleaner for simple mocks.
> 
> The patching is automatically undone when the with block ends.

## Slide 20: Test-Driven Development (TDD)
**Red-Green-Refactor:**
1. Red: Write a failing test first
2. Green: Write the minimum code to pass the test
3. Refactor: Clean up and improve the code

**Benefits:**
* 100% test coverage (in theory)
* Better code design
* Immediate feedback

*Speaker Notes:*
> TDD is a powerful development methodology where you write the tests before the code.
> 
> This forces you to think about the requirements and design before implementation.

## Slide 21: Parametrized Tests with subTest
```python
class TestDiscount(unittest.TestCase):
    def test_calculate_discount(self):
        test_cases = [(100, 0, 100), (100, 50, 50)]
        for price, discount, expected in test_cases:
            with self.subTest(price=price, discount=discount):
                self.assertEqual(calculate_discount(price, discount), expected)
```

*Speaker Notes:*
> subTest allows for running multiple test cases efficiently.
> 
> If one sub-test fails, the others continue to run, and you'll get detailed output.

## Slide 22: Skipping Tests
* `@unittest.skip(reason)`: Skip unconditionally
* `@unittest.skipIf(condition, reason)`: Skip if condition is true
* `@unittest.skipUnless(condition, reason)`: Skip unless condition is true

*Speaker Notes:*
> Sometimes you need to temporarily disable tests (e.g., for platform-specific features or known bugs).

## Slide 23: Advanced Topics
* Expected Failures: `@unittest.expectedFailure`
* Code Coverage: Tools like coverage.py
* Continuous Integration (CI): Automate test execution
* Fixtures (brief mention, suggest pytest for more advanced fixture management)

*Speaker Notes:*
> Briefly introduce some more advanced topics to give audience an idea of the next steps.

## Slide 24: Key Takeaways
* Unit testing is crucial for writing robust and reliable code
* unittest is Python's built-in, powerful testing framework
* Use assertions to verify expected behavior
* Organize your tests for maintainability
* Mock dependencies to isolate your code
* Practice TDD for better design and coverage

*Speaker Notes:*
> Recap the most important concepts covered in the presentation.

## Slide 25: Q&A
Time for questions from the audience.

## Slide 26: Thank You & Resources
**Useful Links:**
* [unittest documentation](https://docs.python.org/3/library/unittest.html)
* [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)

*Speaker Notes:*
> Thank the audience for their time and attention.
> 
> Provide useful links and resources.

---

### Presentation Tips
1. Keep it Concise: Don't overload slides with text. Use bullet points and visuals.
2. Use Visuals: Images, diagrams, and code snippets make the presentation more engaging.
3. Code Highlighting: Use a good code highlighting theme in your presentation software.
4. Live Coding (Optional): Consider doing some live coding to demonstrate concepts.
5. Practice: Rehearse your presentation to ensure a smooth delivery.
6. Engage the Audience: Ask questions, encourage participation, and be enthusiastic.
7. Use a Consistent Theme: Choose a professional and visually appealing theme for your slides.
8. Large, Readable Fonts: Ensure text is easily readable from the back of the room.
