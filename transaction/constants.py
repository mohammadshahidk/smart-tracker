from smart_tracker.library import ChoiceAdapter


class AccountType(ChoiceAdapter):
    """
    Type of the accounts.
    """
    SAVINGS = 101
    INVESTMENT = 102
    FIXED_DEPOSIT = 103


class TransactionType(ChoiceAdapter):
    """
    Type of the transactions.
    """
    INCOME = 101
    EXPENSE = 102


class Category(ChoiceAdapter):
    """
    Category of the transactions.
    """
    SALARY = 101
    GIFT = 102
    INTREST = 103
    RETURN = 104
    TRAVEL = 105
    ENTERTAINMENT = 106
    VEHICLE = 107
    SHOPPING = 108
    FOOD = 109
    INVESTMENT = 110
