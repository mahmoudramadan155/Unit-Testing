
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
