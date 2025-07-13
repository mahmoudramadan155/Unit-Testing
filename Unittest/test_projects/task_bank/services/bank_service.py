
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
