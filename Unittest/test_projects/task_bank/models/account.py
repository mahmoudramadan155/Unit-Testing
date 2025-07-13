
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

