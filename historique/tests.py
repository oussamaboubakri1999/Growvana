from django.test import TestCase
from django.contrib.auth import get_user_model
from culture.models import Culture
from .models import CultureHistorique
from django.urls import reverse
from datetime import datetime

User = get_user_model()

class HistoriqueViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.culture1 = Culture.objects.create(user=self.user1, name='Mint', description='Fresh')
        self.culture2 = Culture.objects.create(user=self.user2, name='Rosemary', description='Aromatic')
        self.hist1 = CultureHistorique.objects.create(culture=self.culture1, action='Planté', timestamp=datetime.now())
        self.hist2 = CultureHistorique.objects.create(culture=self.culture2, action='Récolté', timestamp=datetime.now())

    def test_historique_list_user_filtering(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.get(reverse('historique:historique-list'))
        self.assertContains(response, 'Planté')
        self.assertNotContains(response, 'Récolté')
