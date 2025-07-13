# tests/test_main.py (Corrected)

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from main import command_line_interface
from services.bank_service import BankService
from models.account import Account


class TestCommandLineInterface(unittest.TestCase):
    def setUp(self):
        """Setup before each test."""
        self.bank_service_patch = patch('main.BankService', autospec=True)
        self.mock_bank_service = self.bank_service_patch.start()
        self.mock_bank_service_instance = MagicMock(spec=BankService)
        self.mock_bank_service.return_value = self.mock_bank_service_instance

        self.captured_output = StringIO()  # Redirect stdout
        sys.stdout = self.captured_output

    def tearDown(self):
        """Clean up after each test."""
        sys.stdout = sys.__stdout__  # Restore stdout
        self.bank_service_patch.stop()

    @patch('sys.argv', ['main.py', 'create', 'Test User', '100.0'])
    def test_create_command(self):
        mock_account = MagicMock(spec=Account)
        mock_account.__str__.return_value = "Mocked Account"
        self.mock_bank_service_instance.create_account.return_value = mock_account

        command_line_interface()
        self.mock_bank_service_instance.create_account.assert_called_once_with("Test User", 100.0)
        self.assertEqual(self.captured_output.getvalue().strip(), "Account created: Mocked Account")

    @patch('sys.argv', ['main.py', 'create', 'Test User', '-100.0'])  # Negative initial balance
    def test_create_command_invalid_balance(self):
        self.mock_bank_service_instance.create_account.side_effect = ValueError("Initial balance cannot be negative.")
        command_line_interface()
        self.assertIn("Error: Initial balance cannot be negative.", self.captured_output.getvalue())


    @patch('sys.argv', ['main.py', 'list'])
    def test_list_command(self):
        mock_account1 = MagicMock(spec=Account)
        mock_account1.__str__.return_value = "Account 1"
        mock_account2 = MagicMock(spec=Account)
        mock_account2.__str__.return_value = "Account 2"
        self.mock_bank_service_instance.list_all_accounts.return_value = [mock_account1, mock_account2]

        command_line_interface()
        self.mock_bank_service_instance.list_all_accounts.assert_called_once()
        self.assertEqual(self.captured_output.getvalue().strip(), "Account 1\nAccount 2")


    @patch('sys.argv', ['main.py', 'list'])
    def test_list_command_no_accounts(self):
        self.mock_bank_service_instance.list_all_accounts.return_value = []  # Empty list
        command_line_interface()
        self.assertEqual(self.captured_output.getvalue().strip(), "No accounts found.")



    @patch('sys.argv', ['main.py', 'get', 'ACC0001'])
    def test_get_command(self):
        mock_account = MagicMock(spec=Account)
        mock_account.__str__.return_value = "Mocked Account Details"
        self.mock_bank_service_instance.get_account.return_value = mock_account

        command_line_interface()
        self.mock_bank_service_instance.get_account.assert_called_once_with("ACC0001")
        self.assertEqual(self.captured_output.getvalue().strip(), "Mocked Account Details")

    @patch('sys.argv', ['main.py', 'get', 'ACC9999'])  # Non-existent
    def test_get_command_not_found(self):
        self.mock_bank_service_instance.get_account.return_value = None  # Simulate not found
        command_line_interface()
        self.assertEqual(self.captured_output.getvalue().strip(), "Account ACC9999 not found.")

    @patch('sys.argv', ['main.py', 'deposit', 'ACC0001', '50.0'])
    def test_deposit_command(self):
        # No return value needed for deposit (it's None)
        command_line_interface()
        self.mock_bank_service_instance.deposit.assert_called_once_with("ACC0001", 50.0)
        self.assertEqual(self.captured_output.getvalue().strip(), "Deposited 50.00 into ACC0001")

    @patch('sys.argv', ['main.py', 'deposit', 'ACC9999', '50.0'])
    def test_deposit_command_account_not_found(self):
        self.mock_bank_service_instance.deposit.side_effect = ValueError("Account not found")
        command_line_interface()
        self.assertIn("Error: Account not found", self.captured_output.getvalue())


    @patch('sys.argv', ['main.py', 'withdraw', 'ACC0001', '25.0'])
    def test_withdraw_command(self):
        command_line_interface()
        self.mock_bank_service_instance.withdraw.assert_called_once_with("ACC0001", 25.0)
        self.assertEqual(self.captured_output.getvalue().strip(), "Withdrew 25.00 from ACC0001")

    @patch('sys.argv', ['main.py', 'withdraw', 'ACC0001', '25000.0']) # Insufficient
    def test_withdraw_command_insufficient_funds(self):
        self.mock_bank_service_instance.withdraw.side_effect = ValueError("Insufficient balance.")
        command_line_interface()
        self.assertIn("Error: Insufficient balance.", self.captured_output.getvalue())

    @patch('sys.argv', ['main.py', 'withdraw', 'ACC9999', '25.0']) # Account not found
    def test_withdraw_command_account_not_found(self):
         self.mock_bank_service_instance.withdraw.side_effect = ValueError("Account not found")
         command_line_interface()
         self.assertIn("Error: Account not found", self.captured_output.getvalue())

    @patch('sys.argv', ['main.py', 'transfer', 'ACC0001', 'ACC0002', '25.0'])
    def test_transfer_command(self):
        command_line_interface()
        self.mock_bank_service_instance.transfer.assert_called_once_with("ACC0001", "ACC0002", 25.0)
        self.assertEqual(self.captured_output.getvalue().strip(), "Transferred 25.00 from ACC0001 to ACC0002")


    @patch('sys.argv', ['main.py', 'transfer', 'ACC0001', 'ACC0002', '2500.0']) # Insufficient funds
    def test_transfer_command_insufficient_funds(self):
        self.mock_bank_service_instance.transfer.side_effect = ValueError("Insufficient balance in source account.")
        command_line_interface()
        self.assertIn("Error: Insufficient balance in source account.", self.captured_output.getvalue())

    @patch('sys.argv', ['main.py', 'transfer', 'ACC9999', 'ACC0002', '25.0'])  # Source not found
    def test_transfer_command_source_account_not_found(self):
        self.mock_bank_service_instance.transfer.side_effect = ValueError("Source account not found.")
        command_line_interface()
        self.assertIn("Error: Source account not found.", self.captured_output.getvalue())

    @patch('sys.argv', ['main.py', 'transfer', 'ACC0001', 'ACC9999', '25.0']) # Dest not found
    def test_transfer_command_destination_account_not_found(self):
        self.mock_bank_service_instance.transfer.side_effect = ValueError("Destination account not found.")
        command_line_interface()
        self.assertIn("Error: Destination account not found.", self.captured_output.getvalue())

    @patch('sys.argv', ['main.py', 'transfer', 'ACC0001', 'ACC0002', '-50']) # Negative amount
    def test_transfer_command_negative_amount(self):
         self.mock_bank_service_instance.transfer.side_effect = ValueError("Transfer amount must be positive.")
         command_line_interface()
         self.assertIn("Error: Transfer amount must be positive.", self.captured_output.getvalue())

    @patch('sys.argv', ['main.py']) # No arguments provided
    @patch('argparse.ArgumentParser.print_help')
    def test_no_command(self, mock_print_help):
        command_line_interface()
        mock_print_help.assert_called_once()

    @patch('sys.argv', ['main.py', 'invalid_command'])
    @patch('argparse.ArgumentParser.print_help')
    def test_invalid_command(self, mock_print_help):
        with self.assertRaises(SystemExit):
            command_line_interface()
            mock_print_help.assert_called_once() # Check called within SystemExit context.