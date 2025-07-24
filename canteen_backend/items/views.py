from django.shortcuts import render
from rest_framework import generics, permissions, filters
from .models import Item, TodaysItem
from .serializers import ItemSerializer, TodaysItemSerializer
from accounts.permissions import IsAdmin, IsEmployee
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied


class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name','price']
    ordering_fields = ['name', 'price']
    lookup_field = 'name'


class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'name'



class TodaysItemListCreateView(generics.ListCreateAPIView):
    serializer_class = TodaysItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        today = timezone.now().date()
        return TodaysItem.objects.filter(date=today)

    def perform_create(self, serializer):
        serializer.save()


class TodaysItemUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = TodaysItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'item__name'

    def get_queryset(self):
        today = timezone.now().date()
        return TodaysItem.objects.filter(date=today).select_related('item')


    def delete(self, request, *args, **kwargs):
        raise PermissionDenied("Admin cannot manually delete today's items.")



class TodaysItemListEmployeeView(generics.ListAPIView):
    serializer_class = TodaysItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployee]

    def get_queryset(self):
        today = timezone.now().date()
        return TodaysItem.objects.filter(date=today, quantity__gt=0)
