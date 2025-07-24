from rest_framework import serializers
from .models import Transaction
from items.models import TodaysItem
from accounts.models import User


class AddMoneySerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class PurchaseItemSerializer(serializers.Serializer):
    item_name = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        try:
            todays_item = TodaysItem.objects.get(item__name=data['item_name'])
        except TodaysItem.DoesNotExist:
            raise serializers.ValidationError("Today's item not found.")

        if todays_item.quantity < data['quantity']:
            raise serializers.ValidationError("Not enough quantity available.")

        data['todays_item'] = todays_item
        return data


class TransactionSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'source', 'item_name', 'timestamp']
