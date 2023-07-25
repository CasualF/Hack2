from rest_framework.views import APIView
from rest_framework import permissions, generics
from .serializers import RegisterSerializer
from .send_email import send_activation_email
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = permissions.AllowAny,

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_activation_email(user.email, 'http://127.0.0.1:8000/account/activate/?c='+str(user.activation_code))
            except:
                return Response({'message': 'Registered, but wasnt able to send activation code',
                                 'data': serializer.data}, status=201)

        return Response(serializer.data, status=201)


class ActivationView(APIView):
    def get(self, request):
        code = request.GET.get('c')
        user = get_object_or_404(User, activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Successfully Activated your account', status=200)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class LogoutView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response('You logged out', status=205)
        except:
            return Response('Smth went wrong', status=400)
