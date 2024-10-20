from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RegisterView

from . import views
from .views import (EventViewSet, OddViewSet,
                    OutcomeViewSet, SportViewSet, TeamViewSet, UserViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sports', SportViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'events', EventViewSet)
router.register(r'odd', OddViewSet)
router.register(r'outcomes', OutcomeViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='auth_regiser')
]