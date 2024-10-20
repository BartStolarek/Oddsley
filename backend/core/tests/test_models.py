from django.test import TestCase

from core.models import Sport


class SportModelTest(TestCase):

    def setUp(self):
        Sport.objects.create(key="football",
                             group="Ball Sports",
                             title="Football",
                             active=True)

    def test_sport_creation(self):
        sport = Sport.objects.get(key="football")
        self.assertEqual(sport.title, "Football")
        self.assertTrue(sport.active)

