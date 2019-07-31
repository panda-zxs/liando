#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import auth

from rest_framework import serializers

from common.utils.str_utils import name_maker

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('password', 'is_superuser')

    def create(self, validated_data):
        validated_data['username'] = self.gen_username()
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    @staticmethod
    def gen_username():
        return name_maker(prefix='usr')


class UserUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'password')

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['old_password']):
            return 'update false'
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username',)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        max_length=128, required=True)
    password = serializers.CharField(
        max_length=128, required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        user = auth.authenticate(**attrs)
        if user is None:
            msg = 'Auth failed.'
            raise serializers.ValidationError(msg)
        attrs['user'] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    pass
