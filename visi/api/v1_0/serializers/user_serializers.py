from rest_framework import serializers

from visi.users.models import User


class UserSerializer(serializers.ModelSerializer):
    model = User
    field = ('username', 'email', 'password',)
