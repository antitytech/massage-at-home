from django.contrib.postgres import fields
from django.utils.functional import empty
from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model
User = get_user_model()
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django_email_verification import send_email


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'about', )
    
    def save(self, **kwargs):
        user = self.context['request'].user
        if 'first_name' in self.validated_data:
            user.first_name = self.validated_data['first_name']
        if 'last_name' in self.validated_data:
            user.last_name = self.validated_data['last_name']
        if 'about' in self.validated_data:   
            user.about = self.validated_data['about']
        user.save()


class ViewUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ( 'email', 'password', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions', 'id')

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        # Tuple of serialized model fields (see link [2])
        fields = ( 'email', 'password', 'client_type' )
    
    password = serializers.CharField(write_only=True)
    client_type = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        client_type = attrs.get('client_type')
        password = attrs.get('password')

        if email and client_type and password:
            if not client_type in ['therapist', 'client', 'spa']:
                msg = _('Invalid client_type is provided.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Please provide email, client_type and password to register.')
            raise serializers.ValidationError(msg)
        return super().validate(attrs)

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                email=validated_data['email'],
                client_type=validated_data['client_type']
            )
            user.set_password(validated_data['password'])
            user.save()
        except Exception as e:
            raise serializers.ValidationError(
                _('An error occured while creating user.')
            )
        try:
            send_email(user)
            print('Email sent.')
        except Exception as e:
            print('Email not sent.')
            print(e)
            pass
        return user



class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirm_new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    
    def validate_old_password(self, value):
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was incorrect.')
            )
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({'confirm_new_password': _('Passwords do not match.')})
        password_validation.validate_password(data['new_password'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        user.auth_token_set.all().delete()
        return user