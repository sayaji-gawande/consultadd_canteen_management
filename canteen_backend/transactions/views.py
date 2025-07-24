from django.shortcuts import render

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from decimal import Decimal
from .models import Transaction
from .serializers import AddMoneySerializer, PurchaseItemSerializer, TransactionSerializer
from items.models import TodaysItem,Item
from accounts.permissions import IsAdmin, IsEmployee
from accounts.models import User


class AddMoneyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployee]

    def post(self, request):
        serializer = AddMoneySerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            request.user.balance += amount
            request.user.save()

            Transaction.objects.create(
                user=request.user,
                amount=amount,
                transaction_type='credit',
                source='employee'
            )

            return Response({'message': f'₹{amount} added successfully.', 'balance': request.user.balance})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseItemView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployee]

    def post(self, request):
        item_name = request.data.get('item_name')
        quantity = request.data.get('quantity')

        if not item_name or not quantity:
            return Response({'error': 'item_name and quantity are required.'}, status=400)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({'error': 'Quantity must be positive.'}, status=400)
        except ValueError:
            return Response({'error': 'Quantity must be an integer.'}, status=400)

        try:
            item = Item.objects.get(name__iexact=item_name)
            todays_item = TodaysItem.objects.get(item=item, date=timezone.now().date())
        except (Item.DoesNotExist, TodaysItem.DoesNotExist):
            return Response({'error': 'Item not available in today\'s menu.'}, status=404)

        if todays_item.quantity < quantity:
            return Response({'error': 'Not enough quantity available.'}, status=400)

        total_price = quantity * item.price

        if request.user.balance < total_price:
            return Response({'error': 'Insufficient balance.'}, status=400)

        request.user.balance -= total_price
        request.user.save()

        todays_item.quantity -= quantity
        if todays_item.quantity <= 0:
            todays_item.delete()
        else:
            todays_item.save()

        Transaction.objects.create(
            user=request.user,
            item=item,
            amount=-total_price,
            transaction_type='debit',
            source='employee',
        )

        return Response({
            'message': f'Purchased {item.name} x{quantity} for ₹{total_price}.',
            'remaining_balance': request.user.balance
        })



class PassbookView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployee]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-timestamp')


class AllTransactionsAdminView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = Transaction.objects.all().order_by('-timestamp')


class AdminAddMoneyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request):
        employee_id = request.data.get('employee_id')
        amount = request.data.get('amount')

        if not employee_id or amount is None:
            return Response({'error': 'Employee ID and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError
        except:
            return Response({'error': 'Invalid amount.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = User.objects.get(user_id=employee_id, role='employee')
        except User.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        employee.balance += amount
        employee.save()

        Transaction.objects.create(
            user=employee,
            amount=amount,
            transaction_type='credit',
            source='admin'
        )

        return Response({
            'message': f'₹{amount} credited to {employee.name}.',
            'new_balance': str(employee.balance)
        }, status=status.HTTP_200_OK)
    