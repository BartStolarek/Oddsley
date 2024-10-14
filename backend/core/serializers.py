from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


from .models import Competition, Event, OddsSnapshot, Outcome, Sport, Team

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

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
