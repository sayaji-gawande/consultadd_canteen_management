from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from accounts.models import User
from items.models import Item, TodaysItem
from rest_framework_simplejwt.tokens import RefreshToken


class ItemTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            user_id="A1",
            name="admin1",
            password="consultadd",
            role="admin",
        )
        self.employee = User.objects.create_user(
            user_id="E1",
            name="employee1",
            password="12345@qwert",
            role="employee",
        )
        self.item = Item.objects.create(name="Coffee", price=20)
        self.todays_date = timezone.now().date()

        self.item_list_url = reverse('item-list-create')
        self.item_detail_url = reverse('item-detail', args=[self.item.name])
        self.todays_item_create_url = reverse('todaysitem-list-create')
        self.todays_item_detail_url = reverse('todaysitem-detail', args=[self.item.name])
        self.todays_item_employee_url = reverse('todaysitem-employee-list')

        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_admin_can_create_item(self):
        response = self.client.post(self.item_list_url, {'name': 'Tea', 'price': 15})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_list_items(self):
        response = self.client.get(self.item_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_admin_can_retrieve_update_delete_item(self):
        response = self.client.get(self.item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(self.item_detail_url, {'name': 'Coffee', 'price': 25})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], '25.00')

        response = self.client.delete(self.item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_create_todays_item(self):
        response = self.client.post(self.todays_item_create_url, {
            'item_name': self.item.name,
            'quantity': 10
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.item.name)
        self.assertEqual(int(response.data['quantity']), 10)

    def test_admin_cannot_add_duplicate_todays_item(self):
        TodaysItem.objects.create(item=self.item, quantity=5, date=self.todays_date)
        response = self.client.post(self.todays_item_create_url, {
            'item_name': self.item.name,
            'quantity': 3
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('item_name', response.data)

    def test_admin_cannot_manually_delete_todays_item(self):
        TodaysItem.objects.create(item=self.item, quantity=5, date=self.todays_date)
        url = reverse('todaysitem-detail', args=[self.item.name])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_can_see_only_available_todays_items(self):
        TodaysItem.objects.create(item=self.item, quantity=5, date=self.todays_date)

        zero_item = Item.objects.create(name="Expired", price=10)
        TodaysItem.objects.create(item=zero_item, quantity=0, date=self.todays_date)

        refresh = RefreshToken.for_user(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.get(self.todays_item_employee_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.item.name)
