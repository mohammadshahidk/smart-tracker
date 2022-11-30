from django.db.models import Sum
from rest_framework import serializers

from transaction import models as tran_models


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for Account Object.
    """
    summery = serializers.SerializerMethodField()
    initial_amount = serializers.FloatField(required=False)

    class Meta:
        """
        Meta Info.
        """
        model = tran_models.Account
        fields = '__all__'

    def get_summery(self, obj):
        """
        Function to get current balance and income, expense.
        """
        data = {
            'balance': obj.balance,
            'income': obj.income,
            'expense': obj.expense
        }

        return data


def aggregate(param):
    pass


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction object.
    """
    comment = serializers.CharField(required=False)
    summery = serializers.SerializerMethodField()

    class Meta:
        """Meta Info."""
        model = tran_models.Transaction
        fields = '__all__'

    def get_summery(self, obj):
        """
        to get users current balance, income and expense
        """
        user = self.context['request'].parser_context[
            'kwargs']['user']
        accounts = user.accounts.all()
        balance_sum = 0
        income_sum = 0
        expense_sum = 0
        for account in accounts:
            balance_sum += account.balance
            income_sum += account.income
            expense_sum += account.expense
        data = {
            'balance': balance_sum,
            'income': income_sum,
            'expense': expense_sum,
        }
        print(data)
        return True
