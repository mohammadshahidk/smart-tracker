from django.shortcuts import render

from rest_framework import viewsets

from transaction import serializer as trans_serializer
from transaction import models as trans_models
from transaction.filters import AccountFilter
from transaction.filters import TransactionFilter

from accounts import permissions as account_permissions


class AccountView(viewsets.ModelViewSet):
    """View to Account."""
    permission_classes = (account_permissions.IsAuthenticated,)
    serializer_class = trans_serializer.AccountSerializer
    queryset = trans_models.Account.objects.all()
    filterset_class = AccountFilter


class TransactionView(viewsets.ModelViewSet):
    """View to Transaction."""
    serializer_class = trans_serializer.TransactionSerializer
    permission_classes = (account_permissions.IsAuthenticated,)
    queryset = trans_models.Transaction.objects.all()
    filterset_class = TransactionFilter

