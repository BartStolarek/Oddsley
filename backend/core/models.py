from django.db import models
from django.utils import timezone
from django.db import transaction
from django.utils.dateparse import parse_datetime
from loguru import logger
from datetime import datetime
from django.db import IntegrityError


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


class Team(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('sport', 'name')
    
    def __str__(self):
        return self.name


class Event(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
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
        ('unknown', 'Unknown'),
    ]
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='unknown')

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
        
        
        return cls.objects.update_or_create(
            id=event_data['id'],
            defaults={
                'sport': sport,
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
    def upsert_from_api(cls, odd_data, timestamp: datetime = None, previous_timestamp: datetime = None, next_timestamp: datetime = None):
        with transaction.atomic():
            try:
                
                sport, _ = Sport.objects.get_or_create(key=odd_data['sport_key'])
                
                home_team, created = Team.objects.get_or_create(name=odd_data['home_team'], sport=sport)
                away_team, created = Team.objects.get_or_create(name=odd_data['away_team'], sport=sport)
                
                event, created = Event.objects.update_or_create(
                    id=odd_data['id'],
                    defaults={
                        'sport': Sport.objects.get(key=odd_data['sport_key']),
                        'commence_time': parse_datetime(odd_data['commence_time']),
                        'home_team': home_team,
                        'away_team': away_team,
                        'status': 'unknown'}
                )
            except Exception as e:
                logger.error(f"Error updating or creating event model object with id: {odd_data['id']}: {str(e)}")
                return None, False
            
            try:
                timestamp = parse_datetime(timestamp) if timestamp else timezone.now()
                previous_timestamp = parse_datetime(previous_timestamp) if previous_timestamp else None
                next_timestamp = parse_datetime(next_timestamp) if next_timestamp else None
            except Exception as e:
                logger.error(f"Error parsing timestamps: {str(e)}")
                return None, False
            
            try:
                odd, created = cls.objects.update_or_create(
                    event=event,
                    timestamp=timestamp,
                    defaults={
                        'previous_timestamp': previous_timestamp,
                        'next_timestamp': next_timestamp
                    }
                )
            except Exception as e:
                logger.error(f"Error updating or creating odd model object: {str(e)}, with event id: {event.id} and timestamp: {timestamp}")
                return None, False
        
            for bookmaker_data in odd_data['bookmakers']:
                try:
                    bookmaker, _ = Bookmaker.objects.update_or_create(
                        odd=odd,
                        key=bookmaker_data['key'],
                        defaults={
                            'title': bookmaker_data['title'],
                            'last_update': parse_datetime(bookmaker_data['last_update']),
                        }
                    )
                except Exception as e:
                    logger.error(f"Error updating or creating bookmaker model object: {str(e)}, with odd id: {odd.id} and key: {bookmaker_data['key']}")
                    continue
                
                for market_data in bookmaker_data['markets']:
                    try:
                        market, _ = Market.objects.update_or_create(
                            bookmaker=bookmaker,
                            key=market_data['key'],
                        )
                    except Exception as e:
                        logger.error(f"Error updating or creating market model object: {str(e)}, with bookmaker id: {bookmaker.id} and key: {market_data['key']}")
                        continue

                    for outcome_data in market_data['outcomes']:
                        try:
                            team_name = outcome_data['name']
                            team, created = Team.objects.get_or_create(name=team_name, sport=event.sport)
                            
                            
                            outcome, created = Outcome.objects.update_or_create(
                                market=market,
                                name=team,
                                defaults={
                                    'price': outcome_data['price'],
                                    'point': outcome_data.get('point'),
                                }
                            )
                            
                                
                        except IntegrityError as e:
                            logger.error(f"IntegrityError creating/updating outcome for {outcome_data['name']}: {str(e)}")
                        except Exception as e:
                            logger.error(f"Error creating/updating outcome for {outcome_data['name']}: {str(e)}")

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
    name = models.ForeignKey(Team, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    point = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('market', 'name')

    def __str__(self):
        return f"{self.name} - {self.price}"
    
