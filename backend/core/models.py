from django.db import models
from django.utils import timezone
from django.db import transaction
from django.utils.dateparse import parse_datetime


class Region(models.Model):
    key = models.CharField(primary_key=True, max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Sport(models.Model):
    key = models.CharField(primary_key=True, max_length=50, unique=True)
    group = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    has_outrights = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    @classmethod
    def upsert_from_api(cls, sport_data):
        return cls.objects.update_or_create(
            key=sport_data['key'],
            defaults={
                'group': sport_data['group'],
                'title': sport_data['title'],
                'description': sport_data['description'],
                'active': sport_data['active'],
                'has_outrights': sport_data['has_outrights']
            }
        )


class Competition(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('sport', 'name')
        
    def __str__(self):
        return f"{self.sport.title} - {self.name}"


class Team(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('sport', 'competition', 'name')
    
    def __str__(self):
        return self.name


class Event(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    commence_time = models.DateTimeField(blank=True, null=True)
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

    @classmethod
    def upsert_from_api(cls, event_data):
        # Ensure Sport exists
        sport, _ = Sport.objects.get_or_create(key=event_data['sport_key'])
        
        # Get or create Teams
        home_team, _ = Team.objects.get_or_create(
            name=event_data['home_team'],
            sport=sport
        )
        away_team, _ = Team.objects.get_or_create(
            name=event_data['away_team'],
            sport=sport
        )
        
        # Get or create Competition (consider using a more specific name)
        competition, _ = Competition.objects.get_or_create(
            sport=sport,
            name=event_data.get('competition_name', event_data['sport_title'])
        )
        
        return cls.objects.update_or_create(
            id=event_data['id'],
            defaults={
                'sport': sport,
                'competition': competition,
                'commence_time': event_data['commence_time'],
                'home_team': home_team,
                'away_team': away_team,
                'status': event_data.get('status', 'scheduled')  # Assuming status is optional
            }
        )


class EventResult(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='odds_snapshots')
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


class Odd(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    previous_timestamp = models.DateTimeField(null=True, blank=True)
    next_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('event', 'timestamp')
        verbose_name_plural = 'Odds'

    def __str__(self):
        return f"{self.event} - {self.timestamp}"
    
    @classmethod
    def upsert_from_api(cls, odd_data):
        with transaction.atomic():
            event = Event.objects.get(id=odd_data['id'])
            
            odd, created = cls.objects.update_or_create(
                event=event,
                timestamp=parse_datetime(odd_data['timestamp']),
                defaults={
                    'previous_timestamp': parse_datetime(odd_data['previous_timestamp']),
                    'next_timestamp': parse_datetime(odd_data['next_timestamp'])
                }
            )
            
            for bookmaker_data in odd_data['bookmakers']:
                bookmaker, _ = Bookmaker.objects.update_or_create(
                    odd=odd,
                    key=bookmaker_data['key'],
                    defaults={
                        'title': bookmaker_data['title'],
                        'last_update': parse_datetime(bookmaker_data['last_update']),
                    }
                )

                for market_data in bookmaker_data['markets']:
                    market, _ = Market.objects.update_or_create(
                        bookmaker=bookmaker,
                        key=market_data['key'],
                    )

                    for outcome_data in market_data['outcomes']:
                        Outcome.objects.update_or_create(
                            market=market,
                            name=outcome_data['name'],
                            defaults={
                                'price': outcome_data['price'],
                                'point': outcome_data.get('point'),
                            }
                        )

            return odd, created
        

class Bookmaker(models.Model):
    odd = models.ForeignKey(Odd, on_delete=models.CASCADE, related_name='bookmakers')
    key = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    last_update = models.DateTimeField(default=timezone.now, null=True, blank=True)
    
    class Meta:
        unique_together = ('odd', 'key')

    def __str__(self):
        return f"{self.title} - {self.odd}"


class Market(models.Model):
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.CASCADE, related_name='markets')
    key = models.CharField(max_length=50)

    class Meta:
        unique_together = ('bookmaker', 'key')

    def __str__(self):
        return f"{self.key} - {self.bookmaker}"


class Outcome(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='outcomes')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    point = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('market', 'name')

    def __str__(self):
        return f"{self.name} - {self.price}"
    
