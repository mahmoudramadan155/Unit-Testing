# tests/test_models.py
import unittest
from decimal import Decimal
from calculator.models import Person

class PersonTests(unittest.TestCase):
    def setUp(self):
        self.person1 = Person("Alice", 30, Decimal("50000"))
        self.person2 = Person("Bob", 25, Decimal("45000"))

    def test_person_creation(self):
        person = Person("Alice", 30, Decimal("50000"))
        self.assertEqual(person.name, "Alice")
        self.assertEqual(person.age, 30)
        self.assertEqual(person.salary, Decimal("50000"))
        
    def test_person_raise(self):
        original_salary = self.person1.salary
        raise_amount = Decimal("5000")
        
        self.person1.give_raise(raise_amount)
        self.assertEqual(
            self.person1.salary,
            original_salary + raise_amount,
            "Salary raise was not applied correctly"
        )

if __name__ == '__main__':
    unittest.main()