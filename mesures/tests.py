from django.test import TestCase
from django.contrib.auth import get_user_model
from culture.models import Culture
from .models import Mesure
from django.urls import reverse

User = get_user_model()

class MesureViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.culture1 = Culture.objects.create(user=self.user1, name='Mint', description='Fresh')
        self.culture2 = Culture.objects.create(user=self.user2, name='Rosemary', description='Aromatic')
        self.mesure1 = Mesure.objects.create(culture=self.culture1, valeur=10)
        self.mesure2 = Mesure.objects.create(culture=self.culture2, valeur=20)

    def test_mesure_list_user_filtering(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.get(reverse('mesures:mesure-list'))
        self.assertContains(response, '10')
        self.assertNotContains(response, '20')
