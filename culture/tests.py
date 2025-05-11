from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Culture
from django.urls import reverse

User = get_user_model()

class CultureModelTest(TestCase):
    def test_create_culture(self):
        user = User.objects.create_user(username='user1', password='testpass')
        culture = Culture.objects.create(user=user, name='Basil', description='Herb')
        self.assertEqual(str(culture), 'Basil')
        self.assertEqual(culture.user, user)

class CultureViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.culture1 = Culture.objects.create(user=self.user1, name='Mint', description='Fresh')
        self.culture2 = Culture.objects.create(user=self.user2, name='Rosemary', description='Aromatic')

    def test_culture_list_user_filtering(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.get(reverse('culture:culture-list'))
        self.assertContains(response, 'Mint')
        self.assertNotContains(response, 'Rosemary')

    def test_culture_create_assigns_user(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.post(reverse('culture:culture-create'), {'name': 'Parsley', 'description': 'Green'})
        self.assertEqual(Culture.objects.filter(user=self.user1, name='Parsley').count(), 1)
