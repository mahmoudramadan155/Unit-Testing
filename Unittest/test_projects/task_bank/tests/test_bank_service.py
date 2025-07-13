# tests/test_bank_service.py (Corrected Again!)
import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os
from services.bank_service import BankService
from models.account import Account

class TestBankService(unittest.TestCase):
    """Test cases for the BankService."""

    def setUp(self):
        """Setup method to create a BankService instance before each test."""
        # Use "mock" to prevent automatic file loading in setUp.
        self.bank_service = BankService(data_source="mock")
        self.account_data = {
            "ACC0001": {"account_number": "ACC0001", "account_holder": "John Doe", "balance": 100.0},
            "ACC0002": {"account_number": "ACC0002", "account_holder": "Jane Smith", "balance": 500.0}
        }
        # Preload with some accounts (but without file I/O).
        self.bank_service.accounts = {
            "ACC0001": Account.from_dict(self.account_data["ACC0001"]),
            "ACC0002": Account.from_dict(self.account_data["ACC0002"]),
        }

    @patch('services.bank_service.BankService.save_accounts') # Mock for create account
    def test_create_account(self, mock_save):
        """Test creating an account."""
        mock_save.return_value = None
        new_account = self.bank_service.create_account("Alice Wonderland", 200.0)
        self.assertIsInstance(new_account, Account)
        self.assertEqual(new_account.account_holder, "Alice Wonderland")
        self.assertEqual(new_account.balance, 200.0)
        self.assertIn(new_account.account_number, self.bank_service.accounts)
        mock_save.assert_called_once()

    @patch('services.bank_service.BankService.save_accounts')
    def test_create_account_negative_balance(self, mock_save):
         with self.assertRaises(ValueError):
              self.bank_service.create_account("Bob", -100)
         mock_save.assert_not_called()

    def test_get_account(self):
        """Test getting an account."""
        account = self.bank_service.get_account("ACC0001")
        self.assertIsInstance(account, Account)
        self.assertEqual(account.account_holder, "John Doe")

        not_found_account = self.bank_service.get_account("ACC9999")  # Non-existent
        self.assertIsNone(not_found_account)

    @patch('services.bank_service.BankService.save_accounts')
    def test_deposit(self, mock_save):
        """Test depositing into an account."""
        mock_save.return_value = None # Simulate successful save.
        self.bank_service.deposit("ACC0001", 50.0)
        self.assertEqual(self.bank_service.accounts["ACC0001"].balance, 150.0)
        mock_save.assert_called_once()

    @patch('services.bank_service.BankService.save_accounts')
    def test_deposit_account_not_found(self, mock_save):
        """Test depositing into a non-existent account (should raise ValueError)."""
        with self.assertRaises(ValueError):
            self.bank_service.deposit("ACC9999", 50.0)  # Non-existent account
        mock_save.assert_not_called()

    @patch('services.bank_service.BankService.save_accounts')
    def test_deposit_negative_amount(self, mock_save):
        with self.assertRaises(ValueError):
            self.bank_service.deposit("ACC0001", -50)
        mock_save.assert_not_called()

    @patch('services.bank_service.BankService.save_accounts')
    def test_withdraw(self, mock_save):
        """Test withdrawing from an account."""
        mock_save.return_value = None
        self.bank_service.withdraw("ACC0001", 25.0)
        self.assertEqual(self.bank_service.accounts["ACC0001"].balance, 75.0)
        mock_save.assert_called_once()

    @patch('services.bank_service.BankService.save_accounts')
    def test_withdraw_account_not_found(self, mock_save):
        """Test withdrawing from a non-existent account (should raise ValueError)."""
        with self.assertRaises(ValueError):
            self.bank_service.withdraw("ACC9999", 25.0)  # Non-existent account
        mock_save.assert_not_called()

    @patch('services.bank_service.BankService.save_accounts')
    def test_withdraw_negative_amount(self, mock_save):
         with self.assertRaises(ValueError):
              self.bank_service.withdraw("ACC0001", -25)
         mock_save.assert_not_called()

    @patch('services.bank_service.BankService.save_accounts')
    def test_withdraw_insufficient_funds(self, mock_save):
         with self.assertRaises(ValueError):
              self.bank_service.withdraw("ACC0001", 200) #More than balance
         mock_save.assert_not_called()

    @patch('services.bank_service.BankService.save_accounts')
    def test_transfer(self, mock_save):
        """Test transferring between accounts."""
        mock_save.return_value = None
        self.bank_service.transfer("ACC0001", "ACC0002", 25.0)
        self.assertEqual(self.bank_service.accounts["ACC0001"].balance, 75.0)
        self.assertEqual(self.bank_service.accounts["ACC0002"].balance, 525.0)
        mock_save.assert_called_once()

    @patch('services.bank_service.BankService.save_accounts')
    def test_transfer_insufficient_funds(self, mock_save):
        """Test transferring with insufficient funds (should raise ValueError)."""
        with self.assertRaises(ValueError):
            self.bank_service.transfer("ACC0001", "ACC0002", 150.0)  # Insufficient funds
        mock_save.assert_not_called()

    @patch('services.bank_service.BankService.save_accounts')
    def test_transfer_account_not_found(self, mock_save):
        with self.assertRaises(ValueError):
            self.bank_service.transfer("ACC0001", "ACC999", 50) # to account doesn't exist
        mock_save.assert_not_called()

    @patch('services.bank_service.BankService.save_accounts')
    def test_transfer_negative_amount(self, mock_save):
         with self.assertRaises(ValueError):
              self.bank_service.transfer("ACC0001", "ACC0002", -50)
         mock_save.assert_not_called()

    def test_list_all_accounts(self):
        all_accounts = self.bank_service.list_all_accounts()
        self.assertEqual(len(all_accounts), 2) #Based on initial setup.
        self.assertIsInstance(all_accounts[0], Account)

    @patch("builtins.open", new_callable=mock_open, read_data='{"ACC0001": {"account_number": "ACC0001", "account_holder": "John Doe", "balance": 100.0}}')
    def test_load_accounts_success(self, mock_file):
        bs = BankService(data_source='dummy.json')  # Create a *new* instance
        bs.load_accounts()  # Explicitly call load_tasks
        mock_file.assert_called_with('dummy.json', 'r')
        self.assertEqual(len(bs.accounts), 1)
        self.assertEqual(bs.accounts['ACC0001'].account_holder, 'John Doe')

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_accounts_file_not_found(self, mock_file):
        bs = BankService(data_source = 'nofile.json') # Create a *new* instance.
        bs.load_accounts()
        mock_file.assert_called_once_with("nofile.json", 'r')  # Correct assertion
        self.assertEqual(len(bs.accounts), 0)

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_load_accounts_json_decode_error(self, mock_file):
        bs = BankService(data_source='invalid.json')  # Create a *new* instance
        bs.load_accounts() # Explicitly call load_tasks
        mock_file.assert_called_with('invalid.json', "r")
        self.assertEqual(len(bs.accounts), 0)


    @patch('json.dump')
    def test_save_accounts(self, mock_json_dump):
        # Separate mocks for reading and writing
        mock_read = mock_open(read_data='{}')  # Mock read (empty data)
        mock_write = mock_open()

        with patch('builtins.open', mock_read):
            bs = BankService(data_source="test_accounts.json")

        # Use existing test accounts (no need to load again):
        bs.accounts = {
            "ACC0001": Account.from_dict(self.account_data["ACC0001"]),
            "ACC0002": Account.from_dict(self.account_data["ACC0002"]),
        }
        with patch('builtins.open', mock_write):
            bs.save_accounts()


        mock_write.assert_called_once_with("test_accounts.json", 'w')
        mock_json_dump.assert_called_once()

        args, kwargs = mock_json_dump.call_args
        written_data = args[0]
        self.assertEqual(len(written_data), 2)
        self.assertEqual(written_data['ACC0001']['account_holder'], "John Doe")
        self.assertEqual(written_data['ACC0002']['balance'], 500.0)