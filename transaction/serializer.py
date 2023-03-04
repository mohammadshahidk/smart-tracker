from rest_framework import serializers

from transaction import models as tran_models
from accounts.serializer import UserSerializer
from accounts.models import ProjectUser

from smart_tracker.fields import IdencodeField


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for Account Object.
    """
    id = IdencodeField(read_only=True)
    user = IdencodeField(
        serializer=UserSerializer, related_model=ProjectUser)
    initial_amount = serializers.FloatField(required=False)
    total_balance = serializers.FloatField(source='balance', read_only=True)

    class Meta:
        """
        Meta Info.
        """
        model = tran_models.Account
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction object.
    """
    id = IdencodeField(read_only=True)
    comment = serializers.CharField(required=False)
    summery = serializers.SerializerMethodField()
    account = IdencodeField(
        serializer=AccountSerializer, related_model=tran_models.Account)

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
        return data
