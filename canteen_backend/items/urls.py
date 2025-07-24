from django.urls import path
from .views import (
    ItemListCreateView, ItemRetrieveUpdateDestroyView,
    TodaysItemListCreateView, TodaysItemUpdateView,
    TodaysItemListEmployeeView,
)

urlpatterns = [
  
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<str:name>/', ItemRetrieveUpdateDestroyView.as_view(), name='item-detail'),

 
    path('todays-items/', TodaysItemListCreateView.as_view(), name='todaysitem-list-create'),
    path('todays-items/<str:item_name>/', TodaysItemUpdateView.as_view(), name='todaysitem-detail'),

 
    path('todays-items-employee/', TodaysItemListEmployeeView.as_view(), name='todaysitem-employee-list'),
]
