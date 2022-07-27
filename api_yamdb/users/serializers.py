from rest_framework import serializers
from .models import User


class UserRegSerializer(serializers.ModelSerializer):
    """User registration serializer."""
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
