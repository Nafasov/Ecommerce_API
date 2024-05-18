from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from .permissions import IsOwnerOrReadOnly
from .tasks import ecommerce_send_email
from apps.account.models import User, UserToken
from apps.account.serializers import (
    UserRegisterSerializer,
    SendEmailSerializer,
    VerifyEmailSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer
)


class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = UserToken.objects.create(user=user)
        ecommerce_send_email.apply_async(("Activation Token Code", str(token.token), [user.email]), )
        data = {
            'success': True,
            'detail': 'Activation Token Code has been sent to your email.',
        }
        return Response(data, status=201)


class SendEmailView(generics.GenericAPIView):
    serializer_class = SendEmailSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        print(email)
        user = get_object_or_404(User, email=email)
        token = UserToken.objects.create(user=user)
        print(token)
        ecommerce_send_email.apply_async(("Activation Token Code", str(token.token), [user.email]), )
        data = {
            'success': True,
            'detail': 'Activation Token Code has been sent to your email.',
        }
        return Response(data, status=200)


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        user = get_object_or_404(User, email=email)
        refresh = RefreshToken.for_user(user)
        obtain_token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(obtain_token, status=200)


class LoginView(TokenObtainPairView):
    pass


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        date = {
            'success': True,
            'detail': 'Your password has been changed.',
        }
        return Response(date, status=200)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'success': True,
            'detail': 'Your password has been changed.',
        }
        return Response(data, status=200)


class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        deta = {
            'success': True,
            'detail': 'Your account has been deactivated.',
        }
        return Response(deta, status=200)
