from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

from .models import Competition, Event, OddsSnapshot, Outcome, Sport, Team
from .serializers import (CompetitionSerializer, EventSerializer,
                          OddsSnapshotSerializer, OutcomeSerializer,
                          SportSerializer, TeamSerializer, UserSerializer)


def home(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to the Oddsley Backend</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background-color: #f4f4f4;
                color: #333;
            }
            h1 {
                color: #007BFF;
            }
            a {
                text-decoration: none;
                color: #007BFF;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to the Backend!</h1>
        <p>This API does not have a frontend UI.</p>
        <p>You can access the API documentation at:</p>
        <ul>
            <li><a href="/swagger/">Swagger UI</a></li>
            <li><a href="/redoc/">Redoc</a></li>
        </ul>
    </body>
    </html>
    """
    return HttpResponse(html_content)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class SportViewSet(viewsets.ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
    permission_classes = [IsAuthenticated]


class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsAuthenticated]


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class OddsSnapshotViewSet(viewsets.ModelViewSet):
    queryset = OddsSnapshot.objects.all()
    serializer_class = OddsSnapshotSerializer
    permission_classes = [IsAuthenticated]


class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer
    permission_classes = [IsAuthenticated]
