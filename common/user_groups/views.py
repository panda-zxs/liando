#!/usr/bin/env python
# -*- coding: utf-8 -*-

import coreapi
import coreschema

from django.contrib.auth.models import Group
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework import status

from wisdom_brain.apps.swagger_docs.schemas import CustomAutoSchema

from . import filters as group_filter
from . import serializers as group_serializer


class GroupLCView(ListCreateAPIView):
    serializer_class = group_serializer.GroupLCSerializer
    permission_classes = (AllowAny,)
    queryset = Group.objects.filter(
        profile__deleted=False).prefetch_related('profile')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    filter_class = group_filter.GroupFilter


class GroupDView(DestroyAPIView):
    serializer_class = group_serializer.GroupDSerializer
    permission_classes = (AllowAny,)
    queryset = Group.objects.filter(
        profile__deleted=False).prefetch_related('profile')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    def delete(self, request, *args, **kwargs):
        serializer = group_serializer.GroupDSerializer(data=request.data)
        if serializer.is_valid():
            instances = [instance for instance in
                         serializer.validated_data['instances']]
            print(instances)
            target_id = []
            target_name = []
            for instance in instances:
                instance.profile.deleted = True
                instance.profile.save()
                target_id.append(instance.id)
                target_name.append(instance.name)
            ret = {
                'target_id': target_id,
                'target_name': target_name,
                'results': target_id,
            }
            return Response(status=status.HTTP_200_OK, data=ret)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    schema = CustomAutoSchema(
        manual_fields=[
            coreapi.Field(
                "id",
                required=True,
                location="form",
                schema=coreschema.Array(),
                description='jwt token'
            ),
        ]
    )



class GroupRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = group_serializer.GroupRUDSerializer
    permission_classes = ()
    queryset = Group.objects.all().prefetch_related('profile', 'user_set',
                                                    'permissions')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.profile.deleted = True
        instance.profile.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {'results': serializer.data}
        return Response(data)


class GroupUserRUView(RetrieveUpdateAPIView):
    serializer_class = group_serializer.GroupUserSerializer
    authentication_classes = []
    permission_classes = ()
    queryset = Group.objects.all().prefetch_related('user_set')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    lookup_field = 'id'


class GroupPermissionRUView(RetrieveUpdateAPIView):
    serializer_class = group_serializer.GroupPermissionSerializer
    permission_classes = ()
    queryset = Group.objects.all().prefetch_related('permissions')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    lookup_field = 'id'


class GroupRelationRView(RetrieveAPIView):
    serializer_class = group_serializer.GroupRelationSerializer
    permission_classes = ()
    queryset = Group.objects.all().prefetch_related('profile')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    lookup_field = 'id'


# 返回部门信息
class GroupTreeView(ListAPIView):
    pagination_class = None
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = group_serializer.GroupTreeSerializer
    queryset = Group.objects.filter(
        profile__parent_group=None,
        profile__deleted__exact=False).prefetch_related('profile')
    filter_class = group_filter.GroupTreeFilter

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {"results": serializer.data}
        return Response(status=status.HTTP_200_OK, data=data)


# 根据名字查询部门
class GroupLookUpView(RetrieveAPIView):
    queryset = Group.objects.all().prefetch_related("profile")
    permission_classes = ()
    serializer_class = group_serializer.GroupLCSerializer
    lookup_field = 'profile.name'


# 修改部门名称
class GroupNameView(UpdateAPIView):
    permission_classes = ()
    authentication_classes = []
    queryset = Group.objects.all()
    lookup_field = 'id'
    serializer_class = group_serializer.GroupNameSerializer
