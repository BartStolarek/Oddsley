from django.contrib import admin

from .models import (Bookmaker, Event, EventResult, Market,
                     Odd, Outcome, Region, Sport, Team)

admin.site.register(Region)
admin.site.register(Sport)
admin.site.register(Team)
admin.site.register(Bookmaker)
admin.site.register(Market)
admin.site.register(Event)
admin.site.register(Odd)
admin.site.register(Outcome)
admin.site.register(EventResult)