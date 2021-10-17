from django.http import response
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import login
from auth_module.serailizers import UserSerializer
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

@api_view(['POST',])
def register(request):
    serializer = UserSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['response'] = 'User has been created.'
    else:
        data = serializer.errors
    return Response(data)

@api_view(['POST',])
def update_profile():
    pass