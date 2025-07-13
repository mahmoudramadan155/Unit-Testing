# calculator/core.py
from typing import List

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
