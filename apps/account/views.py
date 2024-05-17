from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from .tasks import ecommerce_send_email


from apps.account.models import User, UserToken
from apps.account.serializers import (
    UserRegisterSerializer,
    SendEmailSerializer
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
