#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from rest_framework import serializers

from common.utils import choices
from common.user_groups.models import GroupProfileModel
from common.users.models import User
from common.user_accounts.serializers import AccountInfoSerializer

from common.utils.str_utils import name_maker


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='id',
                                                 read_only=True)

    class Meta:
        model = User
        fields = ('username', 'user_id')


class PermissionSerializer(serializers.ModelSerializer):
    permission_id = serializers.PrimaryKeyRelatedField(source='id',
                                                       read_only=True)
    codename = serializers.CharField(required=False)

    class Meta:
        model = Permission
        fields = ('permission_id', 'codename')


class GroupLCSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(source='id',
                                                  read_only=True)
    group_name = serializers.CharField(source='profile.group_name',)
    group_permissions = PermissionSerializer(source='permissions',
                                             many=True)
    group_type = serializers.CharField(source='profile.group_type',)
    group_create_time = serializers.CharField(source='profile.created_at',)
    parent_group = serializers.PrimaryKeyRelatedField(
        source='profile.parent_group',
        queryset=Group.objects.all(),
        required=False
    )

    class Meta:
        model = Group
        fields = ('group_id', 'group_name', 'group_permissions',
                  'group_type', 'parent_group', 'group_create_time')

    # def validate_group_permissions(self, value):
    #     print '**', value
    #     id_list = [each['permission_id'] for each in value]
    #     return self.Meta.model.objects.filter(pk__in=id_list)
    #
    # def validate_parent_group(self, value):
    #     parent_group = self.fields['parent_group'].queryset.get(pk=value)
    #     return parent_group

    # def validate(self, attrs):
    #     name_validator = validators.UniqueValidator(
    #         queryset=self.Meta.model.objects.all()
    #     )
    #     name_validator.set_context(self.fields['group_name'])
    #     name_validator(attrs['name'])
    #     return attrs

    def to_internal_value(self, data):
        id_list = [each['permission_id'] for each in data['group_permissions']]
        if 'parent_group' in data:
            parent_group = self.fields['parent_group'].queryset.get(
                pk=data['parent_group']
            )
        else:
            parent_group = None
        ret = {
            'group_name': data['group_name'],
            'name': name_maker('grp'),
            'permissions': Permission.objects.filter(pk__in=id_list),
            'parent_group': parent_group,
            'group_type': data['group_type']
        }
        return ret

    def create(self, validated_data):
        group_type = validated_data.pop('group_type')
        parent_group = validated_data.pop('parent_group')
        group_name = validated_data.pop('group_name')
        group = super(GroupLCSerializer, self).create(validated_data)
        group.profile = GroupProfileModel.objects.create(
            group=group,
            parent_group=parent_group,
            group_type=group_type,
            group_name=group_name,
        )
        group.save()
        return group

    # def create(self, validated_data):
    #     group_type = validated_data.pop('group_type')
    #     parent_group = validated_data.pop('parent_group')
    #     result = Group.objects.filter(
    #     name=validated_data.get('name')).exists()
    #     if not result:
    #         group = super(GroupLCSerializer, self).create(validated_data)
    #         group.profile = GroupProfileModel.objects.create(
    #             group=group,
    #             parent_group=parent_group,
    #             group_type=group_type
    #         )
    #     else:
    #         group = Group.objects.get(name=validated_data.get('name'))
    #         group.permissions.set(validated_data.get('permissions'))
    #         group.profile.group_type = group_type
    #         group.profile.parent_group = parent_group
    #         group.profile.deleted = False
    #         group.profile.save()
    #     group.save()
    #     return group


class GroupDSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(source='id',
                                                  read_only=True)
    group_name = serializers.CharField(
        source='profile.group_name',
    )
    group_permissions = PermissionSerializer(source='permissions',
                                             many=True)
    group_type = serializers.CharField(source='profile.group_type', )
    group_create_time = serializers.CharField(source='profile.created_at', )
    parent_group = serializers.PrimaryKeyRelatedField(
        source='profile.parent_group',
        queryset=Group.objects.all(),
        required=False
    )

    class Meta:
        model = Group
        fields = ('group_id', 'group_name', 'group_permissions',
                  'group_type', 'parent_group', 'group_create_time')

    @staticmethod
    def to_internal_value(data):
        return {'instances': Group.objects.filter(pk__in=data['id']).all()}


class GroupRUDSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(source='id',
                                                  read_only=True)
    group_name = serializers.CharField(source='profile.group_name',
                                       required=False)
    group_users = serializers.PrimaryKeyRelatedField(
        source='user_set',
        many=True,
        required=False,
        queryset=User.objects.all()
    )
    group_permissions = serializers.PrimaryKeyRelatedField(
        source='permissions',
        many=True,
        required=False,
        queryset=Permission.objects.all()
    )

    group_users_info = AccountInfoSerializer(
        source='user_set',
        many=True,
        required=False
    )

    group_permissions_info = PermissionSerializer(
        source='permissions',
        many=True,
        required=False,
    )

    class Meta:
        model = Group
        fields = ('group_id', 'group_name',
                  'group_users', 'group_permissions',
                  'group_users_info', 'group_permissions_info')

    def update(self, instance, validated_data):
        if validated_data.get('user_set') is not None and self.partial:
            instance.user_set.set(validated_data['user_set'])

        if validated_data.get('permissions') is not None and self.partial:
            instance.permissions.set(validated_data['permissions'])

        if validated_data.get('profile') is not None:
            instance.profile.group_name = \
                validated_data['profile']['group_name']
            instance.profile.save()

        instance.save()
        return instance


# 修改部门名称
class GroupNameSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='profile.group_name',
                                       required=False)
    class Meta:
        model = Group
        fields = ('id', 'group_name')

    def update(self, instance, validated_data):
        instance.profile.group_name = validated_data['name']
        instance.profile.save()
        return instance


class GroupUserSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(source='id',
                                                  read_only=True)
    group_name = serializers.StringRelatedField(source='profile.group_name')
    group_users = AccountInfoSerializer(source='user_set', many=True)
    group_users_count = serializers.SerializerMethodField(read_only=True)

    op = serializers.ChoiceField(choices.OP_CHOICES,
                                 write_only=True,
                                 required=False)

    class Meta:
        model = Group
        fields = ('group_id', 'group_name', 'group_users', 'group_users_count',
                  'op')

    @staticmethod
    def get_group_users_count(obj):
        return len(obj.user_set.all())

    @staticmethod
    def to_internal_value(data):
        """
        Convert from request.data to validated_data.
        :param data:
        {
            'op': 'add',
            "group_users": [
                {
                    "user_id": "y",
                }
            ]
        }
        :return:
        """
        # id_list = [each['user_id'] for each in data['group_users']]
        ret = {
            'op': data.get('op'),
            'user_set': User.objects.filter(pk__in=data.get('group_users')),
        }
        return ret

    def update(self, instance, validated_data):
        if not self.partial or validated_data['op'] == 'set':
            instance.user_set.set(validated_data['user_set'])
        else:
            for user in validated_data['user_set']:
                if validated_data['op'] == 'add':
                    instance.user_set.add(user)
                else:
                    instance.user_set.remove(user)
        return instance


class GroupPermissionSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(source='id',
                                                  read_only=True)
    group_permissions = PermissionSerializer(source='permissions',
                                             many=True)

    op = serializers.ChoiceField(choices.OP_CHOICES,
                                 write_only=True,
                                 required=False)

    class Meta:
        model = Group
        fields = ('group_permissions', 'group_id', 'op')

    def to_internal_value(self, data):
        """
        Convert from request.data to validated_data.
        :param data:
        {
            "op": "add",
            "group_permissions": [
                {
                    "permission_id": "y",
                }
            ]
        }
        :return:
        """
        id_list = [each['permission_id'] for each in data['group_permissions']]
        ret = {
            'op': data.get('op'),
            'permissions': Permission.objects.filter(pk__in=id_list),
        }
        return ret

    def update(self, instance, validated_data):
        if not self.partial or validated_data['op'] == 'set':
            instance.permissions.set(validated_data['permissions'])
        else:
            for permission in validated_data['permissions']:
                if validated_data['op'] == 'add':
                    instance.permissions.add(permission)
                else:
                    instance.permissions.remove(permission)
        return instance


class GroupRelationSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(source='id',
                                                  read_only=True)
    group_name = serializers.StringRelatedField(
        source='profile.group_name',
        read_only=True)

    relations = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('group_id', 'group_name', 'relations')

    @staticmethod
    def get_relations(obj):
        return obj.profile.get_relation_repr()


class GroupSerializer(serializers.ModelSerializer):
    # 部门信息序列化器
    group_name = serializers.StringRelatedField(
        source='profile.group_name',
        read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'group_name')


class SubGroupSerializer(serializers.ModelSerializer):
    # 子部门信息序列化器
    group_name = serializers.StringRelatedField(
        source='profile.group_name',
        read_only=True)
    subs = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'group_name', 'subs')

class GroupTreeSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return instance.profile.get_relation_repr()
