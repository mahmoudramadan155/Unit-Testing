from bank_account import BankAccount

def test_initial_balance():
    """is the initial balance equal to 100"""
    balance = 100
    account = BankAccount(balance)
    assert account.balance == 100

def test_deposit():
    balance = 100
    account = BankAccount(balance)
    account.deposit(50)
    assert account.balance == 150

def test_withdraw():
    balance = 100
    account = BankAccount(balance)
    account.withdraw(30)
    assert account.balance == 70

def test_deposit_transaction():
    balance = 100

    account = BankAccount(balance)
    account.deposit(50)

    assert "Deposited 50" in account.transactions

def test_withdraw_transaction():
    balance = 100

    account = BankAccount(balance)
    account.withdraw(30)

    assert "Withdrew 30" in account.transactions

def test_invalid_deposit():
    balance = 100

    account = BankAccount(balance)
    account.deposit(-50)
    assert account.balance == 100

def test_invalid_withdraw():
    balance = 100

    account = BankAccount(balance)
    account.withdraw(150)
    assert account.balance == 100

def test_get_balance():
    balance = 100
    account = BankAccount(balance)
    assert account.get_balance() == 100
    account.deposit(50)
    assert account.get_balance() == 150
    account.withdraw(30)
    assert account.get_balance() == 120
