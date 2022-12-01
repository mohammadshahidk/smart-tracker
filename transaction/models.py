import datetime

from django.db import models
from accounts import models as user_model
from django.db.models import Sum

from smart_tracker.library import encode
from smart_tracker.library import decode
from transaction import constants as tran_constants


class Account(models.Model):
    """
    Account class is for record user's accounts and its datas

    Attributes:
        user(obj) : user object
        name(str) : account name
        initial_amount(float) : initial amount of that account
        type(int) : type of that account
    """

    user = models.ForeignKey(
        user_model.ProjectUser, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(default='', max_length=50, null=True, blank=True)
    initial_amount = models.FloatField(default=0.0)
    type = models.IntegerField(
        default=tran_constants.AccountType.SAVINGS,
        choices=tran_constants.AccountType.choices())

    def __str__(self):
        """ Returns the account name on list of accounts"""
        return self.name

    @property
    def income(self):
        """ Returns users total income."""
        income = self.transactions.filter(
            type=tran_constants.TransactionType.INCOME).aggregate(
            Sum('amount'))['amount__sum']
        if income is None:
            income = 0
        return income

    @property
    def expense(self):
        """ Returns users total expense."""
        spend = self.transactions.filter(
            type=tran_constants.TransactionType.EXPENSE).aggregate(
            Sum('amount'))['amount__sum']
        if spend is None:
            spend = 0
        return spend

    @property
    def idencode(self):
        """To return encoded id."""
        return encode(self.id)

    @property
    def balance(self):
        """ Returns users current balance."""
        return (self.initial_amount + self.income) - self.expense


class Transaction(models.Model):
    """
    Transaction class is for record user's Transaction details.

    Attributes:
        account(obj) : account object.
        created_on(datetime) : date of the tranaction.
        type(int) : type of the tranaction (income or expense).
        category(int) : category of the transaction.
        amount(int) : Transaction amount.
        comments(str) : notes of the transaction.
    """
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='transactions')
    created_on = models.DateTimeField(
        auto_now_add=True)
    type = models.IntegerField(
        default=tran_constants.TransactionType.INCOME,
        choices=tran_constants.TransactionType.choices())
    category = models.IntegerField(
        default=tran_constants.Category.FOOD,
        choices=tran_constants.Category.choices())
    amount = models.FloatField(
        default=0.0, blank=True, null=True)
    comment = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        """ Returns the account name on list of accounts"""
        return self.idencode

    @property
    def idencode(self):
        """To return encoded id."""
        return encode(self.id)



