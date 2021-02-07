from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)

    def __str__(self):
        return self.item_id


class Account(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=100)
    available_balance = models.FloatField()
    current_balace = models.FloatField()
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    account_subtype = models.CharField(max_length=100)

    def __str__(self):
        return self.account_id


class Transaction(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField()
    name = models.CharField(max_length=100)
    payment_channel = models.CharField(max_length=100)

    def __str__(self):
        return self.transaction_id
