from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class TodaysItem(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} ({self.quantity})"
    
    @property
    def price(self):
        return self.item.price
