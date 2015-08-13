__author__ = "Jay Modi"

from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only = True
        fields = ('id', 'username', 'first_name', 'last_name', 'email', )

class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    class Meta:
        model = Token
        fields = ('key',)