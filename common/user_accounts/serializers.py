#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from rest_framework import serializers

from common.users.models import User
from common.user_accounts.models import AccountModel

from common.utils.log import getLogger
from common.utils import choices
from common.utils.str_utils import name_maker

LOG = getLogger(__name__)


class GroupSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(source='id',
                                                  read_only=True)
    group_name = serializers.CharField(
        source='name',
    )
    parent_group = serializers.PrimaryKeyRelatedField(
        source='profile.parent_group',
        queryset=Group.objects.all(),
        required=False
    )

    class Meta:
        model = Group
        fields = ('group_id', 'group_name', 'parent_group')


class PermissionSerializer(serializers.ModelSerializer):
    permission_id = serializers.PrimaryKeyRelatedField(source='id',
                                                       read_only=True)
    codename = serializers.CharField(required=False)

    class Meta:
        model = Permission
        fields = ('permission_id', 'codename')


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='id',
                                                 read_only=True)
    password = serializers.CharField(write_only=True)

    groups = GroupSerializer(many=True)
    permissions = PermissionSerializer(source='user_permissions',
                                       many=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'user_id', 'groups', 'permissions')

    def to_internal_value(self, data):
        group_id_list = [each['group_id']
                         for each in data.pop('groups')]
        _groups = Group.objects.filter(pk__in=group_id_list)

        permission_id_list = [each['permission_id']
                              for each in data.pop('permissions')]
        _permissions = Permission.objects.filter(pk__in=permission_id_list)
        data['groups'] = _groups
        data['user_permissions'] = _permissions
        return data

    def create(self, validated_data):
        LOG.debug('user validated_data: %s', validated_data)
        validated_data['username'] = self.gen_username()
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    @staticmethod
    def gen_username():
        return name_maker(prefix='usr')


class AccountLCSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    sex = serializers.ChoiceField(choices.SEX_CHOICES)
    email = serializers.EmailField()
    account_id = serializers.PrimaryKeyRelatedField(source='id',
                                                    read_only=True)

    class Meta:
        model = AccountModel
        fields = ('email', 'phone', 'nickname', 'sex', 'job_num', 'wechat',
                  'user', 'account_id')

    def create(self, validated_data):
        LOG.debug('account validated_data: %s', validated_data)
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user = user_serializer.create(user_data)
        validated_data['user'] = user
        account = super(AccountLCSerializer, self).create(validated_data)
        return account


class AccountRUDSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    sex = serializers.ChoiceField(choices.SEX_CHOICES, required=False)
    email = serializers.EmailField(required=False)

    account_id = serializers.PrimaryKeyRelatedField(source='id',
                                                    read_only=True)

    class Meta:
        model = AccountModel
        fields = ('email', 'phone', 'nickname', 'sex', 'job_num', 'wechat',
                  'user', 'account_id')


class AccountPermissionSerializer(serializers.ModelSerializer):
    account_id = serializers.PrimaryKeyRelatedField(source='id',
                                                    read_only=True)
    all_permissions = serializers.SerializerMethodField()
    account_permissions = PermissionSerializer(
        source='user.user_permissions',
        many=True
    )
    op = serializers.ChoiceField(choices.OP_CHOICES,
                                 write_only=True,
                                 required=False)

    class Meta:
        model = AccountModel
        fields = ('all_permissions', 'account_permissions', 'account_id', 'op')

    @classmethod
    def get_all_permissions(cls, obj):
        permissions = obj.get_all_permissions()
        ret = []
        for permission in permissions:
            serializer = PermissionSerializer(permission)
            ret.append(serializer.data)
        return ret

    def to_internal_value(self, data):
        """
        Convert from request.data to validated_data.
        :param data:
        {
            "op": "add",
            "account_permissions": [
                {
                    "permission_id": "y",
                }
            ]
        }
        :return:
        """
        id_list = [each['permission_id']
                   for each in data['account_permissions']]
        ret = {
            'op': data.get('op'),
            'permissions': Permission.objects.filter(pk__in=id_list),
        }
        return ret

    def update(self, instance, validated_data):
        LOG.debug('update account_permission, inst: %s, data: %s', instance,
                  validated_data)
        if not self.partial:
            instance.user.user_permissions.set(validated_data['permissions'])
        else:
            for permission in validated_data['permissions']:
                if validated_data['op'] == 'add':
                    instance.user.user_permissions.add(permission)
                else:
                    instance.user.user_permissions.remove(permission)
        return instance

class AccountInfoSerializer(serializers.ModelSerializer):
    nickname = serializers.StringRelatedField(source='account.nickname')
    sex = serializers.StringRelatedField(source='account.sex')
    job_num = serializers.StringRelatedField(source='account.job_num')
    phone = serializers.StringRelatedField(source='account.phone')
    email = serializers.StringRelatedField(source='account.email')
    wechat = serializers.StringRelatedField(source='account.wechat')
    qq = serializers.StringRelatedField(source='account.qq')

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname',
                  'sex', 'job_num', 'phone',
                  'email', 'wechat', 'qq')
