# calculator/calculator.py
from typing import List, Optional
from decimal import Decimal
from dataclasses import dataclass

class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b

def process_numbers(numbers: List[float]) -> float:
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise TypeError("All inputs must be numbers")
    return sum(numbers)

@dataclass
class Person:
    name: str
    age: int
    salary: Optional[Decimal] = None

    def give_raise(self, amount: Decimal) -> None:
        if self.salary is None:
            raise ValueError("Person has no current salary")
        self.salary += amount