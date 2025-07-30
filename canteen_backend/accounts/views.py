from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions,generics, filters
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from accounts.permissions import IsAdmin , IsEmployee
from .models import User
from .serializers import UserRegisterSerializer, UserLoginSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            login(request, user)  

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role,
                'name': user.name
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)  
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class EmployeeListView(generics.ListAPIView):
    queryset = User.objects.filter(role='employee')
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user_id', 'name']
    ordering_fields = ['user_id', 'name']

class AdminAddEmployeeView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request):
        data = request.data.copy()
        data['role'] = 'employee'  # Force role as employee

        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request, employee_id):
        try:
            employee = User.objects.get(user_id=employee_id, role='employee')
        except User.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'name': employee.name,
            'balance': employee.balance
        })

class MyBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployee]

    def get(self, request):
        return Response({
            'balance': request.user.balance
        })
