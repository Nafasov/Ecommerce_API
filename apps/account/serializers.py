from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts

from .models import User, UserToken


class UserRegisterSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        user = super().create(validated_data)
        user.set_password(password1)
        user.save()
        return user


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('Email not registered')
        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.IntegerField()

    class Meta:
        fields = ['email', 'token']

    def validate(self, attrs):
        email = attrs.get('email')
        token = attrs.get('token')
        user = User.objects.get(email=email)
        if not UserToken.objects.filter(user=user).exists():
            raise ValidationError('Credentials is not valid')
        user_token = UserToken.objects.filter(user=user).last()
        if user_token.is_used:
            raise ValidationError('Token is already used')
        if str(user_token) != str(token):
            raise ValidationError('Token does not match')
        user_token.is_used = True
        user.is_active = True
        user_token.save()
        user.save()
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if not self.context['request'].user.check_password(old_password):
            raise ValidationError('Old password does not match')
        if old_password == password1:
            raise ValidationError('Old password does not match')
        if password1 != password2:
            raise ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        user = self.context['request'].user
        user.set_password(password1)
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('password2')
        if self.context['request'].user.check_password(password1):
            raise ValidationError('Old password does not match')
        if password1 != password2:
            raise ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password')
        user = self.context['request'].user
        user.set_password(password1)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'avatar', 'is_active', 'is_superuser', 'is_superuser', 'modified_date', 'created_date')


