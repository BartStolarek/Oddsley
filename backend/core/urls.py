from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import (CompetitionViewSet, EventViewSet, OddsSnapshotViewSet,
                    OutcomeViewSet, SportViewSet, TeamViewSet, UserViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sports', SportViewSet)
router.register(r'competitions', CompetitionViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'events', EventViewSet)
router.register(r'odds-snapshots', OddsSnapshotViewSet)
router.register(r'outcomes', OutcomeViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('', include(router.urls)),
]