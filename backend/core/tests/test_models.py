from django.test import TestCase

from core.models import Competition, Sport


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


class CompetitionModelTest(TestCase):

    def setUp(self):
        sport = Sport.objects.create(key="football",
                                     group="Ball Sports",
                                     title="Football",
                                     active=True)
        Competition.objects.create(sport=sport, name="Premier League")

    def test_competition_creation(self):
        competition = Competition.objects.get(name="Premier League")
        self.assertEqual(competition.sport.title, "Football")
