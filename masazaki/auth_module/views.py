from auth_module.serializers import (ViewUserProfileSerializer, UpdatePasswordSerializer, 
                                    UserSerializer, UpdateUserProfileSerializer)
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from knox.views import LoginView as KnoxLoginView
from django_email_verification import send_email
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import login
from django.shortcuts import render
from rest_framework import status


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
        data['message'] = 'New user has been created.'
    else:
        data = serializer.errors
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = UpdatePasswordSerializer(data=request.data, context={'request': request})
    data = {}
    if serializer.is_valid():
        serializer.save()
        data = {'message': 'Password has been updated.'}
        response = Response(data, status=status.HTTP_202_ACCEPTED)
    else:
        data = serializer.errors
        response = Response(data, status=status.HTTP_501_NOT_IMPLEMENTED)
    return response


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def verify_email(request):
    user = request.user
    if not user.is_email_verified:
        send_email(user=user)
        msg = _('Verification email has been sent to the user.')
        response = Response({'message':msg}, status=status.HTTP_201_CREATED)
    else:
        msg = _('This user is already verified.')
        response = Response({'message':msg}, status=status.HTTP_208_ALREADY_REPORTED)
    return response


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def view_profile(request):
    print(request.user)
    user_profile_serializer = ViewUserProfileSerializer(request.user)
    return Response(user_profile_serializer.data)


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def update_profile(request):
    update_user  = UpdateUserProfileSerializer(data=request.data, context={'request': request})
    if update_user.is_valid():
        update_user.save()
    return Response(update_user.data)

from django.core.management import call_command
def home(request):
    call_command('makemigrations')
    call_command('migrate')
    return render(request, "home.html")

    