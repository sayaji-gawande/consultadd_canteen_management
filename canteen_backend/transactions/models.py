from django.db import models
from accounts.models import User
from items.models import Item


class Transaction(models.Model):
    TRANSACTION_CHOICES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )
    SOURCE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        item_info = f" - {self.item.name}" if self.item else ""
        return f"{self.user.user_id}{item_info} ({self.transaction_type}) ₹{self.amount}"

