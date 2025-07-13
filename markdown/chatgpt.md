# Advanced Python Unit Testing
## A Comprehensive Deep Dive

### 1. Mock Objects and Patch Decorators
#### Understanding Advanced Mocking
- **Context Managers vs Decorators**
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

### 2. Test Fixtures and Resource Management
#### Advanced Setup and Teardown
```python
class AdvancedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared_resource = expensive_setup()
        
    def setUp(self):
        self.temp_dir = create_temp_directory()
        self.addCleanup(self.cleanup_temp_dir)
        
    def cleanup_temp_dir(self):
        shutil.rmtree(self.temp_dir)
```

### 3. Parameterized Testing Techniques
#### Using Data Providers
```python
class TestWithParameters(unittest.TestCase):
    @parameterized.expand([
        ("valid_case", "input1", True),
        ("edge_case", "", False),
        ("error_case", None, False)
    ])
    def test_validation(self, name, input_value, expected):
        result = validate_input(input_value)
        self.assertEqual(result, expected)
```

### 4. Testing Asynchronous Code
#### Handling Async Operations
```python
class AsyncTests(unittest.TestCase):
    async def async_setup(self):
        self.client = await create_async_client()
        
    async def test_async_operation(self):
        await self.async_setup()
        result = await self.client.fetch_data()
        self.assertIsNotNone(result)
        
    def test_async_wrapper(self):
        asyncio.run(self.test_async_operation())
```

### 5. Custom Assertions and Test Helpers
#### Building Test Infrastructure
```python
class CustomAssertions(unittest.TestCase):
    def assertDictContainsSubset(self, expected, actual):
        """Assert that actual dict contains all items from expected dict"""
        for key, value in expected.items():
            self.assertIn(key, actual)
            self.assertEqual(actual[key], value)
            
    def assertValidResponse(self, response):
        """Custom assertion for API responses"""
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())
```

### 6. Test Coverage and Quality Metrics
#### Advanced Coverage Techniques
```python
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

### 7. Integration with CI/CD
#### GitHub Actions Example
```yaml
name: Python Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - name: Run Tests
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          python -m pytest --cov
```

### 8. Testing Design Patterns
#### Test Doubles Pattern
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

### 9. Performance Testing
#### Timing Decorators
```python
def time_test(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper
```

### 10. Property-Based Testing
#### Using Hypothesis
```python
from hypothesis import given, strategies as st

class PropertyTests(unittest.TestCase):
    @given(st.lists(st.integers()))
    def test_sort_idempotent(self, lst):
        """Test that sorting twice gives same result as sorting once"""
        once = sorted(lst)
        twice = sorted(sorted(lst))
        self.assertEqual(once, twice)
```

### Best Practices Summary
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

### Additional Resources
- Python unittest documentation
- pytest framework
- Coverage.py
- Hypothesis testing framework
- Mock object library
