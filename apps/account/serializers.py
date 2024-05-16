from django.contrib.auth import password_validation
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password], help_text=password_validators_help_texts)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

        def validate(self, attrs):
            email = attrs.get('email')
            password1 = attrs.get('password1')
            password2 = attrs.get('password2')
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError('Email already registered')
            if password1 != password2:
                raise serializers.ValidationError('Passwords do not match')
            return attrs