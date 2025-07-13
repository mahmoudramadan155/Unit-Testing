
# --- tests/test_account_model.py ---
import unittest
from models.account import Account

class TestAccountModel(unittest.TestCase):
    """Test cases for the Account model."""

    def setUp(self):
        """Setup method to create an Account instance before each test."""
        self.account = Account("ACC0001", "John Doe", 100.0)

    def test_create_account(self):
        """Test creating an account."""
        self.assertEqual(self.account.account_number, "ACC0001")
        self.assertEqual(self.account.account_holder, "John Doe")
        self.assertEqual(self.account.balance, 100.0)

    def test_deposit(self):
        """Test depositing money."""
        self.account.deposit(50.0)
        self.assertEqual(self.account.balance, 150.0)

    def test_deposit_negative_amount(self):
        """Test depositing a negative amount (should raise ValueError)."""
        with self.assertRaises(ValueError):
            self.account.deposit(-50.0)

    def test_withdraw(self):
        """Test withdrawing money."""
        self.account.withdraw(25.0)
        self.assertEqual(self.account.balance, 75.0)

    def test_withdraw_negative_amount(self):
        """Test withdrawing a negative amount (should raise ValueError)."""
        with self.assertRaises(ValueError):
            self.account.withdraw(-25.0)

    def test_withdraw_insufficient_balance(self):
        """Test withdrawing more than the balance (should raise ValueError)."""
        with self.assertRaises(ValueError):
            self.account.withdraw(150.0)

    def test_str(self):
        """Test the string representation of the account."""
        expected_str = "Account Number: ACC0001, Holder: John Doe, Balance: 100.00"
        self.assertEqual(str(self.account), expected_str)

    def test_to_dict(self):
        """Test account to_dict method."""
        expected_data = {
            'account_number' : "ACC0001",
            'account_holder': "John Doe",
            'balance': 100.0
        }
        self.assertEqual(self.account.to_dict(), expected_data)

    def test_from_dict(self):
        """Test account creation from_dict"""
        account_data = {
            'account_number' : "ACC0002",
            'account_holder': "Jane Smith",
            'balance': 550.50
        }
        account = Account.from_dict(account_data)
        self.assertEqual(account.account_number, account_data['account_number'])
        self.assertEqual(account.account_holder, account_data['account_holder'])
        self.assertEqual(account.balance, account_data['balance'])
        self.assertIsInstance(account, Account)
