# calculator/models.py
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

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
