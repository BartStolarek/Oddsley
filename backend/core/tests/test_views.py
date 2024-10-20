# In backend/core/tests/test_views.py

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Sport, Team


class HomeViewTests(TestCase):

    def test_home_page(self):
        response = self.client.get(
            reverse('home'))  # Adjust the URL name as needed
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Backend!", response.content)


class UserViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',
                                             password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_user_list(self):
        response = self.client.get(
            reverse('user-list'))  # Adjust URL name as needed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class SportViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',
                                             password='testpass')
        self.client.force_authenticate(user=self.user)
        self.sport = Sport.objects.create(key='football',
                                          group='Team Sports',
                                          title='Football')

    def test_sport_list(self):
        response = self.client.get(
            reverse('sport-list'))  # Adjust URL name as needed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_sport(self):
        response = self.client.post(reverse('sport-list'), {
            'key': 'basketball',
            'group': 'Team Sports',
            'title': 'Basketball'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sport.objects.count(), 2)


class TeamViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',
                                             password='testpass')
        self.client.force_authenticate(user=self.user)
        self.sport = Sport.objects.create(key='football',
                                          group='Team Sports',
                                          title='Football')


    def test_create_team(self):
        response = self.client.post(
            reverse('team-list'),
            {
                'name': 'Team A',
                'sport': self.sport.id,
            })

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED,
                         msg=f"Response data: {response.data}")
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get().name, 'Team A')
