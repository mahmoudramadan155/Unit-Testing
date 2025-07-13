# Project: Simple Banking System

# Directory Structure:
# banking_system/
# ├── models/
# │   ├── __init__.py
# │   └── account.py
# ├── services/
# │   ├── __init__.py
# │   └── bank_service.py
# ├── utils/
# │   ├── __init__.py
# │   ├── logger.py
# │   └── config.py
# ├── tests/
# │   ├── __init__.py
# │   ├── test_account_model.py
# │   ├── test_bank_service.py
# │   └── test_main.py
# ├── main.py
# ├── config.json
# ├── requirements.txt
# ├── .env
# └── README.md

# --- models/account.py ---
class Account:
    """Represents a bank account."""

    def __init__(self, account_number: str, account_holder: str, balance: float = 0.0) -> None:
        """Initializes an Account object.

        Args:
            account_number: The unique account number.
            account_holder: The name of the account holder.
            balance: The initial balance (default is 0.0).
        """
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount: float) -> None:
        """Deposits money into the account.

        Args:
            amount: The amount to deposit.

        Raises:
            ValueError: If the amount is negative.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraws money from the account.

        Args:
            amount: The amount to withdraw.

        Raises:
            ValueError: If the amount is negative or exceeds the balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount

    def __str__(self) -> str:
        """Returns a string representation of the account."""
        return (f"Account Number: {self.account_number}, "
                f"Holder: {self.account_holder}, Balance: {self.balance:.2f}")

    def to_dict(self):
        """Converts account details to a dictionary"""
        return {
            'account_number': self.account_number,
            'account_holder': self.account_holder,
            'balance': self.balance
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Account':
        """Creates an Account object from a dictionary"""
        return cls(data['account_number'], data['account_holder'], data['balance'])



# --- services/bank_service.py ---
import json
from typing import Dict, List
from models.account import Account
from utils.logger import logger
from utils.config import config


class BankService:
    """Manages bank accounts and operations."""

    def __init__(self, data_source: str = None) -> None:
        """Initializes the BankService.  Loads accounts from data_source."""
        self.data_source = data_source or config.get('data_file', 'accounts.json')
        self.accounts: Dict[str, Account] = {}
        self.load_accounts()


    def load_accounts(self) -> None:
        """Loads accounts from the JSON file."""
        try:
            with open(self.data_source, "r") as f:
                accounts_data = json.load(f)
                for acc_num, acc_data in accounts_data.items():
                    self.accounts[acc_num] = Account.from_dict(acc_data)
            logger.info("Accounts loaded from file.")

        except FileNotFoundError:
            logger.warning(f"Data source file '{self.data_source}' not found.  Starting with empty account list.")
            self.accounts = {}
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON in '{self.data_source}'. Starting with empty account list.")
            self.accounts = {}
        except Exception as e:
            logger.exception(f"An unexpected error occurred while loading accounts: {e}")
            self.accounts = {}



    def save_accounts(self) -> None:
        """Saves accounts to the JSON file."""

        try:
            accounts_data = {acc_num: acc.to_dict() for acc_num, acc in self.accounts.items()}
            with open(self.data_source, 'w') as file:
                json.dump(accounts_data, file, indent=4)
            logger.info("Accounts successfully saved")
        except Exception as e:
            logger.exception(f"Error saving account data: {e}")
            raise

    def create_account(self, account_holder: str, initial_balance: float = 0.0) -> Account:
        """Creates a new bank account.

        Args:
            account_holder: The name of the account holder.
            initial_balance: The initial balance (default is 0.0).

        Returns:
            The newly created Account object.
        Raises:
            ValueError: If initial_balance is negative
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        account_number = self._generate_account_number()
        new_account = Account(account_number, account_holder, initial_balance)
        self.accounts[account_number] = new_account
        self.save_accounts()
        logger.info(f"Created account {account_number} for {account_holder}.")
        return new_account

    def _generate_account_number(self) -> str:
        """Generates a unique account number (simple incrementing for this example)."""
        # In a real system, this would use a more robust method (e.g., UUIDs).
        next_number = len(self.accounts) + 1
        return f"ACC{next_number:04}"  # e.g., ACC0001, ACC0002, ...

    def get_account(self, account_number: str) -> Account | None:
        """Retrieves an account by its account number.

        Args:
            account_number: The account number.

        Returns:
            The Account object if found, otherwise None.
        """
        return self.accounts.get(account_number)

    def deposit(self, account_number: str, amount: float) -> None:
        """Deposits money into an account.

        Args:
            account_number: The account number.
            amount: The amount to deposit.

        Raises:
            ValueError: If the account is not found or the amount is invalid.
        """
        account = self.get_account(account_number)
        if not account:
            raise ValueError(f"Account {account_number} not found.")
        account.deposit(amount)
        self.save_accounts()
        logger.info(f"Deposited {amount:.2f} into account {account_number}.")


    def withdraw(self, account_number: str, amount: float) -> None:
        """Withdraws money from an account.

        Args:
            account_number: The account number.
            amount: The amount to withdraw.

        Raises:
            ValueError: If the account is not found or the amount is invalid.
        """
        account = self.get_account(account_number)
        if not account:
            raise ValueError(f"Account {account_number} not found.")
        account.withdraw(amount)
        self.save_accounts()
        logger.info(f"Withdrew {amount:.2f} from account {account_number}.")


    def transfer(self, from_account_number: str, to_account_number: str, amount: float) -> None:
        """Transfers money between two accounts.

        Args:
            from_account_number: The account number to transfer from.
            to_account_number: The account number to transfer to.
            amount: The amount to transfer.

        Raises:
            ValueError: If either account is not found or the amount is invalid.
        """
        from_account = self.get_account(from_account_number)
        to_account = self.get_account(to_account_number)

        if not from_account or not to_account:
            raise ValueError("One or both accounts not found.")

        # Use a try-except block to handle potential withdrawal errors *and* rollback
        try:
            from_account.withdraw(amount)
            to_account.deposit(amount)
            self.save_accounts()
            logger.info(f"Transferred {amount:.2f} from {from_account_number} to {to_account_number}.")
        except ValueError as e:
            logger.error(f"Transfer failed: {e}")  # Log specific error
            raise  # Re-raise to propagate the error to the caller

    def list_all_accounts(self) -> List[Account]:
        """Lists all accounts."""
        return list(self.accounts.values())



# --- utils/logger.py ---
import logging
import os
from datetime import datetime

def setup_logger() -> logging.Logger:
    """Sets up the logger with file and stream handlers."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_dir, f"bank_system_{timestamp}.log")

    logger = logging.getLogger("BankSystemLogger")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    return logger

logger = setup_logger()

# --- utils/config.py ---
import json
import os
from dotenv import load_dotenv

def load_config(config_file: str = "config.json") -> dict:
    """Loads configuration from JSON and .env files."""
    config = {}
    try:
        with open(config_file, "r") as f:
            config.update(json.load(f))
    except FileNotFoundError:
        logger.warning(f"Configuration file '{config_file}' not found.")
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON in '{config_file}'.")

    load_dotenv()
    config.update(os.environ)  # .env overrides JSON
    return config

config = load_config()

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



# --- tests/test_bank_service.py ---
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
        self.bank_service = BankService(data_source="mock_accounts.json")
        self.account_data = {
            "ACC0001": {"account_number": "ACC0001", "account_holder": "John Doe", "balance": 100.0},
            "ACC0002": {"account_number": "ACC0002", "account_holder": "Jane Smith", "balance": 500.0}
        }
        #Preload with some accounts.
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
        bs = BankService(data_source='dummy.json')
        mock_file.assert_called_with('dummy.json', 'r')
        self.assertEqual(len(bs.accounts), 1)
        self.assertEqual(bs.accounts['ACC0001'].account_holder, 'John Doe')

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_accounts_file_not_found(self, mock_open_func):
        bs = BankService(data_source = 'nofile.json')
        mock_open_func.assert_called_once_with("nofile.json", 'r')
        self.assertEqual(len(bs.accounts), 0)

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_load_accounts_json_decode_error(self, mock_file):
       bs = BankService(data_source='invalid.json')
       mock_file.assert_called_with('invalid.json', "r")
       self.assertEqual(len(bs.accounts), 0)


    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_accounts(self, mock_json_dump, mock_file_open):
        bs = BankService(data_source="test_accounts.json")
        # Use existing test accounts:
        bs.accounts = {
            "ACC0001": Account.from_dict(self.account_data["ACC0001"]),
            "ACC0002": Account.from_dict(self.account_data["ACC0002"]),
        }
        bs.save_accounts()

        mock_file_open.assert_called_once_with("test_accounts.json", 'w')
        mock_json_dump.assert_called_once()

        args, kwargs = mock_json_dump.call_args
        written_data = args[0]
        self.assertEqual(len(written_data), 2)
        self.assertEqual(written_data['ACC0001']['account_holder'], "John Doe")
        self.assertEqual(written_data['ACC0002']['balance'], 500.0)


# --- config.json ---
# {
#   "data_file": "accounts.json"
# }

# --- .env ---
# API_KEY=your_secret_api_key # Example

# --- main.py ---
from services.bank_service import BankService
from utils.config import config
from utils.logger import logger
import argparse


def command_line_interface() -> None:
    """Provides a command-line interface for the banking system."""

    parser = argparse.ArgumentParser(description="Simple Banking System")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create account
    create_parser = subparsers.add_parser("create", help="Create a new account")
    create_parser.add_argument("holder_name", type=str, help="Account holder name")
    create_parser.add_argument("initial_balance", type=float, nargs='?', default=0.0, help="Initial balance (optional)")

    # List accounts
    list_parser = subparsers.add_parser("list", help="List all accounts")

    # Get account details
    get_parser = subparsers.add_parser("get", help="Get details of an account")
    get_parser.add_argument("account_number", type=str, help="Account number")

    # Deposit
    deposit_parser = subparsers.add_parser("deposit", help="Deposit into an account")
    deposit_parser.add_argument("account_number", type=str, help="Account number")
    deposit_parser.add_argument("amount", type=float, help="Amount to deposit")

    # Withdraw
    withdraw_parser = subparsers.add_parser("withdraw", help="Withdraw from an account")
    withdraw_parser.add_argument("account_number", type=str, help="Account number")
    withdraw_parser.add_argument("amount", type=float, help="Amount to withdraw")

    # Transfer
    transfer_parser = subparsers.add_parser("transfer", help="Transfer between accounts")
    transfer_parser.add_argument("from_account", type=str, help="Source account number")
    transfer_parser.add_argument("to_account", type=str, help="Destination account number")
    transfer_parser.add_argument("amount", type=float, help="Amount to transfer")

    args = parser.parse_args()

    bank_service = BankService(config.get("data_file"))

    try:
        if args.command == "create":
            account = bank_service.create_account(args.holder_name, args.initial_balance)
            print(f"Account created: {account}")

        elif args.command == "list":
            accounts = bank_service.list_all_accounts()
            if accounts:
                for account in accounts:
                    print(account)
            else:
                print("No accounts found.")

        elif args.command == "get":
            account = bank_service.get_account(args.account_number)
            if account:
                print(account)
            else:
                print(f"Account {args.account_number} not found.")

        elif args.command == "deposit":
            bank_service.deposit(args.account_number, args.amount)
            print(f"Deposited {args.amount:.2f} into {args.account_number}")

        elif args.command == "withdraw":
            bank_service.withdraw(args.account_number, args.amount)
            print(f"Withdrew {args.amount:.2f} from {args.account_number}")

        elif args.command == "transfer":
            bank_service.transfer(args.from_account, args.to_account, args.amount)
            print(f"Transferred {args.amount:.2f} from {args.from_account} to {args.to_account}")

        else:
            parser.print_help()

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



# --- tests/test_main.py ---
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
        self.mock_bank_service_instance.withdraw.side_effect = ValueError("