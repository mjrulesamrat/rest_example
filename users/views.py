__author__ = 'Jay Modi'

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status

from .utils import import_callable
from .serializers import (
    TokenSerializer as DefaultTokenSerializer, UserSerializer)


serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})

TokenSerializer = import_callable(
    serializers.get('TOKEN_SERIALIZER', DefaultTokenSerializer))


class CreateUser(APIView):
    permission_classes = (AllowAny,)
    token_model = Token
    response_serializer = TokenSerializer

    def login(self, user_obj):
        """
        Login user and create token
        """
        self.user = authenticate(username=self.request.data['email'], password=self.request.data['password'])
        self.token, created = self.token_model.objects.get_or_create(
            user=self.user)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            # new_user = authenticate(username=self.request.data['username'], password=self.request.data['password'])
            login(self.request, self.user)

    def get_response(self):
        """
        return token for further authentication & 200 OK 
        """
        return Response({'code': 1, 'status': status.HTTP_200_OK, 'message': 'Success', 'token':self.token.key }
            # self.response_serializer(self.token).data, status=status.HTTP_200_OK
        )

    def get_error_response(self):
        """
        retun 400 error
        """
        return Response({'code': 0, 'status': status.HTTP_400_BAD_REQUEST, 'message': 'Fail', }
            # status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request, *args, **kwargs):
        """
        Create new user from post data
        """
        if User.objects.filter(email=request.data['email']):
                self.token, created = self.token_model.objects.get_or_create(
                    user=user_obj
                )
                return self.get_response()
        else:
            try:
                user_data = User(email=request.data['email'], username=request.data['email'], )
                user_data.password = make_password(request.data['password'])
                user_data.is_active = True
                user_data.save()
                # send_mail('Welcome to Django Rest example', message, 'mjrulesamrat@gmail.com', [str(user_data.email)],
                #           fail_silently=False)
                self.login(user_data)
                return self.get_response()
            except Exception as e:
                print e, "<--- Exception at Create User"
                try:
                    user_data.delete()
                    return Response({'code': 0, 'status': 200, 'message': 'All fields are mandatory'})
                except:
                    return Response({'code': 0, 'status': 200, 'message': 'Failed'})


class UserDetails(viewsets.ModelViewSet):
    """
    Retrive and Update User
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()