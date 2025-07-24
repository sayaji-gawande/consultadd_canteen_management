from rest_framework import serializers
from .models import Item, TodaysItem
from datetime import date


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'price']



class TodaysItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(write_only=True)
    price = serializers.DecimalField(source='item.price', read_only=True, max_digits=8, decimal_places=2)
    name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = TodaysItem
        fields = ['item_name', 'name','price', 'quantity', 'date']
        read_only_fields = ['name','price', 'date']

    def create(self, validated_data):
        item_name = validated_data.pop('item_name')
        try:
            item = Item.objects.get(name=item_name)
        except Item.DoesNotExist:
            raise serializers.ValidationError({'item_name': 'Item not found in master list.'})
        
        today = date.today()

        if TodaysItem.objects.filter(item=item, date= today).exists():
            raise serializers.ValidationError({'item_name': 'Item already added for today.'})

        todays_item = TodaysItem.objects.create(item=item, date=today,**validated_data)
        return todays_item
    
