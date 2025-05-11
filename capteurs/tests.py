from django.test import TestCase
from django.contrib.auth import get_user_model
from culture.models import Culture
from .models import Capteur, CapteurType
from django.urls import reverse

User = get_user_model()

class CapteurModelTest(TestCase):
    def test_create_capteur(self):
        user = User.objects.create_user(username='user1', password='testpass')
        culture = Culture.objects.create(user=user, name='Basil', description='Herb')
        ctype = CapteurType.objects.create(name='Temperature', unit='C')
        capteur = Capteur.objects.create(identifier='S1', type=ctype, culture=culture)
        self.assertEqual(str(capteur), 'S1')
        self.assertEqual(capteur.culture, culture)

class CapteurViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.ctype = CapteurType.objects.create(name='Humidity', unit='%')
        self.culture1 = Culture.objects.create(user=self.user1, name='Mint', description='Fresh')
        self.culture2 = Culture.objects.create(user=self.user2, name='Rosemary', description='Aromatic')
        self.capteur1 = Capteur.objects.create(identifier='C1', type=self.ctype, culture=self.culture1)
        self.capteur2 = Capteur.objects.create(identifier='C2', type=self.ctype, culture=self.culture2)

    def test_capteur_list_user_filtering(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.get(reverse('capteurs:capteur-list'))
        self.assertContains(response, 'C1')
        self.assertNotContains(response, 'C2')
