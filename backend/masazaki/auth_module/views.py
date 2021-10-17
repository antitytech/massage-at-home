from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers, status
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from auth_module.serailizers import UserSerializer, UpdatePasswordSerializer
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated


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

@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = UpdatePasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    # if using drf authtoken, create a new token 
    if hasattr(user, 'auth_token'):
        user.auth_token.delete()
    # token, created = Token.objects.get_or_create(user=user)
    # # return new token
    # return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'success': 'Password has been updated.'})


@api_view(['POST',])
def update_profile():
    pass