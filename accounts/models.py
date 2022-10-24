# app.models.py
from email.policy import default
from django.db import models
from django.conf import settings

def upload_to(instance, filename):
    return 'trading_systems/{filename}'.format(filename=filename)

class Trading_System(models.Model):
    # Description of the trading strategies
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="trading_systems", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to, default='images/default.png')
    created_at = models.DateTimeField(auto_now_add=True)


class Symbol(models.Model):
    # Ticker symbol
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="symbols", on_delete=models.CASCADE)
    label = models.CharField(max_length=100)


class Account(models.Model):
    # Account information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="accounts", on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label


# Transaction choises for deposit and withdraw
TRANSACTION_CHOICES = (
    ('deposit', 'deposit'),
    ('withdraw', 'withdraw'),
)


class Transaction(models.Model):
    # Transaction information
    account = models.ForeignKey(Account, related_name="transactions", on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_CHOICES, max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account.label

    # get all transactions from one user accross all accounts
    def get_all_transactions(user):
        return Transaction.objects.filter(account__user=user)

    # after transaction is saved, update account balance
    def save(self, *args, **kwargs):
        if self.transaction_type == 'deposit':
            self.account.balance += self.amount
        elif self.transaction_type == 'withdraw':
            self.account.balance -= self.amount
        self.account.save()
        super(Transaction, self).save(*args, **kwargs)
    
    # delete transaction and update account balance
    def delete(self, *args, **kwargs):
        if self.transaction_type == 'deposit':
            self.account.balance -= self.amount
        elif self.transaction_type == 'withdraw':
            self.account.balance += self.amount
        self.account.save()
        super(Transaction, self).delete(*args, **kwargs)