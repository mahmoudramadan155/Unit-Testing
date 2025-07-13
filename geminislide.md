## Mastering Unit Testing in Python with unittest

### Slide 1: Title Slide

- **Title:** Mastering Unit Testing in Python with unittest
- **Subtitle:** Write Robust and Reliable Code
- **Your Name / Affiliation / Date**
- **Image:** Python logo with a testing theme

**Speaker Notes:**

- Welcome the audience and introduce the topic.
- Explain the importance of unit testing and what they will learn.

### Slide 2: What is Unit Testing?

- **Bullet Points:**
  - Testing individual units of code (functions, methods) in isolation.
  - Focuses on verifying the smallest testable parts of an application.
  - Like testing individual gears in a machine, not the whole machine at once.

**Speaker Notes:**

- Explain unit testing using an analogy.
- Discuss why isolating units is beneficial.

### Slide 3: Why Unit Testing? (Benefits)

- **Bullet Points:**
  - Reduces Defects: Find bugs early, saving time and money.
  - Improves Code Quality: Forces better design and modularity.
  - Facilitates Refactoring: Provides a safety net for code changes.
  - Living Documentation: Tests show how code should work.
  - Increased Confidence: Make changes without fear of breaking things.

**Speaker Notes:**

- Explain each benefit with an example.
- Emphasize cost-saving and long-term advantages.

### Slide 4: The Testing Pyramid

- **Visual:** Pyramid diagram (Unit Tests > Integration Tests > E2E Tests)
- **Bullet Points:**
  - Unit tests should form the foundation of your testing strategy.
  - Integration tests check how units work together.
  - E2E tests validate the entire application flow.

**Speaker Notes:**

- Describe each layer of the pyramid and its role.
- Explain why unit tests are the foundation.

### Slide 5: FIRST Principles of Good Unit Tests

- **Bullet Points:**
  - **Fast:** Run quickly.
  - **Isolated:** Independent of each other.
  - **Repeatable:** Same result every time.
  - **Self-validating:** Clear pass/fail.
  - **Timely:** Written before/alongside code (TDD).

**Speaker Notes:**

- Describe each principle with a practical example.

### Slide 6: Introducing unittest

- **Bullet Points:**
  - Python's built-in testing framework.
  - Inspired by JUnit (Java).
  - Provides tools for:
    - Creating test cases (`unittest.TestCase`).
    - Making assertions (`assertEqual`).
    - Running tests (test runners).

**Speaker Notes:**

- Explain why unittest is widely used and readily available.

### Slide 7: Your First Unit Test (Code Example)

```python
# my_module.py
def add(x, y):
    return x + y
```

```python
# test_my_module.py
import unittest
from my_module import add

class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

if __name__ == '__main__':
    unittest.main()
```

**Speaker Notes:**

- Walk through the code step-by-step.
- Explain test structure and assertions.

### Slide 8: Running Tests

- **Bullet Points:**
  - Command Line:
    ```bash
    python -m unittest test_my_module.py
    python -m unittest discover
    python -m unittest -v test_my_module.py
    ```
  - Running within a file:
    ```python
    if __name__ == '__main__': unittest.main()
    ```

**Speaker Notes:**

- Explain different ways to execute tests.
- Discuss test discovery and verbosity options.

### Slide 9: Assertion Methods

- **Bullet Points:**
  - `self.assertEqual(a, b)`: Checks `a == b`
  - `self.assertTrue(x)`: Checks `bool(x) is True`
  - `self.assertIsNone(x)`: Checks `x is None`
  - `self.assertIn(a, b)`: Checks `a in b`
  - `self.assertRaises(Exception, callable)`: Checks for exceptions

**Speaker Notes:**

- Explain each assertion with a brief example.
- Emphasize using the most specific assertion available.

### Slide 10: assertRaises Example

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

**Speaker Notes:**

- Explain how `assertRaises` verifies exception handling.

### Slide 11: Setup and Teardown

- **Bullet Points:**
  - `setUp()`: Runs before each test method.
  - `tearDown()`: Runs after each test method.
  - `setUpClass()`: Runs once before all tests in a class.
  - `tearDownClass()`: Runs once after all tests in a class.

**Speaker Notes:**

- Describe the importance of setup/teardown.

### Slide 12: Mocking - Isolating Dependencies

- **Bullet Points:**
  - Problem: External dependencies (network, database, etc.).
  - Solution: Replace dependencies with mocks/stubs.
  - Benefits:
    - Faster tests.
    - More reliable tests.
    - Control over dependency behavior.

**Speaker Notes:**

- Explain when and why to use mocks.

### Slide 13: unittest.mock

```python
from unittest.mock import Mock, patch
@patch('my_module.requests.get')
def test_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {'data': 'Mocked'}
    mock_get.return_value = mock_response
```

**Speaker Notes:**

- Explain how to use `patch` to replace dependencies.

### Slide 14: Test-Driven Development (TDD)

- **Bullet Points:**
  - **Red:** Write a failing test first.
  - **Green:** Write the minimum code to pass the test.
  - **Refactor:** Improve the code.
  - **Benefits:**
    - 100% test coverage.
    - Better code design.
    - Immediate feedback.

**Speaker Notes:**

- Explain the TDD cycle with an example.

### Slide 15: Parametrized Tests with subTest

```python
class TestDiscount(unittest.TestCase):
    def test_calculate_discount(self):
        test_cases = [(100, 0, 100), (100, 50, 50)]
        for price, discount, expected in test_cases:
            with self.subTest(price=price, discount=discount):
                self.assertEqual(calculate_discount(price, discount), expected)
```

**Speaker Notes:**

- Explain how `subTest` reduces duplication.

### Slide 16: Key Takeaways

- **Bullet Points:**
  - Unit testing ensures robust, reliable code.
  - `unittest` is Python's built-in framework.
  - Use assertions to verify expected behavior.
  - Organize tests for maintainability.
  - Mock dependencies for isolation.
  - Practice TDD for better design.

### Slide 17: Q&A

- **Image:** Question mark or audience interaction visual.

### Slide 18: Thank You & Resources

- **Links:**
  - [unittest Documentation](https://docs.python.org/3/library/unittest.html)
  - [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)

---

This presentation is structured to be clear, engaging, and educational.

