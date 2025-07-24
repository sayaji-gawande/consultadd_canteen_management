from django.urls import path
from .views import (RegisterView, LoginView, LogoutView,
                   EmployeeListView, AdminAddEmployeeView,
                   EmployeeBalanceView,  MyBalanceView)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('add-employee/', AdminAddEmployeeView.as_view(), name='admin-add-employee'),
    path('employee-balance/<str:employee_id>/', EmployeeBalanceView.as_view(), name='employee-balance'),
    path('my-balance/', MyBalanceView.as_view(), name='my-balance'),
]
