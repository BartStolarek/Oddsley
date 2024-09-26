from django.contrib import admin
from .models import Region, Sport, Competition, Team, Bookmaker, Market, Event, OddsSnapshot, Outcome, EventResult

admin.site.register(Region)
admin.site.register(Sport)
admin.site.register(Competition)
admin.site.register(Team)
admin.site.register(Bookmaker)
admin.site.register(Market)
admin.site.register(Event)
admin.site.register(OddsSnapshot)
admin.site.register(Outcome)
admin.site.register(EventResult)