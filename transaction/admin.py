from django.contrib import admin
from .models import Account
from .models import Transaction

admin.site.register(Account)
admin.site.register(Transaction)
