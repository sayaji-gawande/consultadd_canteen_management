from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class AccountsAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            user_id='A1',
            name='admin1',
            password='consultadd',
            role='admin',
        )

        self.employee = User.objects.create_user(
            user_id='E1',
            name='employee1',
            password='12345@qwert',
            role='employee',
        )
        self.employee.balance = 100
        self.employee.save()

        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.employee_list_url = reverse('employee-list')
        self.add_employee_url = reverse('admin-add-employee')
        self.employee_balance_url = lambda eid: reverse('employee-balance', args=[eid])
        self.my_balance_url = reverse('my-balance')

    def get_jwt_headers(self, user):
        refresh = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {str(refresh.access_token)}'}

    def test_register(self):
        data = {
            "user_id": "E2",
            "name": "employee2",
            "password": "12345@qwert",
            "role": "employee"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        data = {
            "user_id": "E1",
            "password": "12345@qwert"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_logout(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_add_employee(self):
        headers = self.get_jwt_headers(self.admin)
        data = {
            "user_id": "E3",
            "name": "employee3",
            "password": "12345@qwert"
        }
        response = self.client.post(self.add_employee_url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_admin_view_employee_list(self):
        headers = self.get_jwt_headers(self.admin)
        response = self.client.get(self.employee_list_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_employee_cannot_view_employee_list(self):
        headers = self.get_jwt_headers(self.employee)
        response = self.client.get(self.employee_list_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_view_employee_balance(self):
        headers = self.get_jwt_headers(self.admin)
        response = self.client.get(self.employee_balance_url("E1"), **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['balance']), "100.00")

    def test_employee_cannot_view_other_employee_balance(self):
        headers = self.get_jwt_headers(self.employee)
        response = self.client.get(self.employee_balance_url("E3"), **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_view_own_balance(self):
        headers = self.get_jwt_headers(self.employee)
        response = self.client.get(self.my_balance_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['balance']), "100.00")