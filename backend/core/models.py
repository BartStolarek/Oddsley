from django.db import models


class Region(models.Model):
    key = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Sport(models.Model):
    key = models.CharField(max_length=50, unique=True)
    group = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    has_outrights = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Competition(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sport.title} - {self.name}"


class Team(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    competitions = models.ManyToManyField(Competition)

    def __str__(self):
        return self.name


class Bookmaker(models.Model):
    key = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    regions = models.ManyToManyField(Region)

    def __str__(self):
        return self.title


class Market(models.Model):
    key = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Event(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    commence_time = models.DateTimeField()
    home_team = models.ForeignKey(Team,
                                  on_delete=models.CASCADE,
                                  related_name='home_events')
    away_team = models.ForeignKey(Team,
                                  on_delete=models.CASCADE,
                                  related_name='away_events')
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='scheduled')

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"


class OddsSnapshot(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('event', 'bookmaker', 'market', 'timestamp')

    def __str__(self):
        return f"{self.event} - {self.bookmaker} - {self.market} - {self.timestamp}"


class Outcome(models.Model):
    snapshot = models.ForeignKey(OddsSnapshot,
                                 on_delete=models.CASCADE,
                                 related_name='outcomes')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    point = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.price}"


class EventResult(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    winner = models.ForeignKey(Team,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    details = models.JSONField(
        null=True, blank=True)  # For storing additional result details

    def __str__(self):
        return f"{self.event}: {self.home_score} - {self.away_score}"
