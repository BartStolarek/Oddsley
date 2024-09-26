from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Competition, Event, OddsSnapshot, Outcome, Sport, Team


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class SportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sport
        fields = '__all__'


class CompetitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competition
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class OddsSnapshotSerializer(serializers.ModelSerializer):

    class Meta:
        model = OddsSnapshot
        fields = '__all__'


class OutcomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Outcome
        fields = '__all__'
