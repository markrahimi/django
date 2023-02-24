from rest_framework.exceptions import ValidationError
from functions.filter import *
from rest_framework import serializers
from account.models import CustomUser


class ManagerRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'profile', 'mobile', 'email',\
            'bio', 'state', 'city',\
            'address', 'sex','birthday']

        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('password2')
        if password != confirm_password:
            raise ValidationError("passwords do not match")
        return data

    def create(self, validated_data):
        user = super(ManagerRegistrationSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'mobile', 'email',\
            'password', 'password2']

        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('password2')
        if password != confirm_password:
            raise ValidationError("passwords do not match")
        return data

    def create(self, validated_data):
        user = super(UserRegistrationSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ManagerUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'profile', 'email','bio', 'sex',
                  'state', 'city', 'address','birthday']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'profile', 'email', 'resume', 'bio', 'sex',
                  'state', 'city', 'address','field_area', 'birthday']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'profile', 'email', 'mobile', 'username', 'bio', 'birthday']


class UserReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'profile', 'email', 'mobile', 'birthday']

