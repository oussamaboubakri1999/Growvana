from django.test import TestCase
from django.contrib.auth import get_user_model
from culture.models import Culture
from .models import Alert
from django.urls import reverse

User = get_user_model()

class NotificationViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.culture1 = Culture.objects.create(user=self.user1, name='Mint', description='Fresh')
        self.culture2 = Culture.objects.create(user=self.user2, name='Rosemary', description='Aromatic')
        self.alert1 = Alert.objects.create(culture=self.culture1, message='Alert 1')
        self.alert2 = Alert.objects.create(culture=self.culture2, message='Alert 2')

    def test_notification_list_user_filtering(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.get(reverse('notification:notification-list'))
        self.assertContains(response, 'Alert 1')
        self.assertNotContains(response, 'Alert 2')
