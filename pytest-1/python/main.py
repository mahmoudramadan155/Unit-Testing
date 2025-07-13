'''
from name_function import get_formatted_name

print("Enter 'q' any time to quit.")
while True:
    first = input("Please give me a first name: ")
    if first == 'q':
        break
    last = input("Please give me a last name: ")
    if last == 'q':
        break

    formatted_name = get_formatted_name(first, last)
    print(f"\tFormatted name: {formatted_name}")
'''

from bank_account import BankAccount

balance = 100
account = BankAccount(balance)

print(f"Initial balance: {account.balance}")
print(f"Despositing 50: {account.deposit(50)}")

print(f"Withdrawing 30: {account.withdraw(30)}")