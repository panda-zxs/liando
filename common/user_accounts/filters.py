#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import Q

from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework import status

from .models import AccountModel


class AccountFilter(filters.FilterSet):
    group_id = filters.CharFilter(label='group_id',
                                  method='filter_by_group',
                                  help_text='通过 group_id 过滤')
    name_like = filters.CharFilter(label='name_like',
                                   method='filter_by_pattern_name',
                                   help_text='通过 name 模糊匹配过滤')

    class Meta:
        model = AccountModel
        fields = ('group_id', 'name_like')

    @classmethod
    def filter_by_group(cls, queryset, _, value):
        try:
            _ = Group.objects.get(id=value)
        except ObjectDoesNotExist:
            return Response(status.HTTP_400_BAD_REQUEST)
        group_list = []
        subs = Group.objects.filter(profile__parent_group__id=value)
        for sub in subs:
            group_list.append(sub.id)
        subs = Group.objects.filter(profile__parent_group__id__in=group_list)
        for sub in subs:
            group_list.append(sub.id)
        group_list.append(value)
        return queryset.filter(user__groups__id__in=group_list)

    @classmethod
    def filter_by_pattern_name(cls, queryset, _, value):
        q = Q(user__username__contains=value) | Q(nickname__contains=value)
        return queryset.filter(q)
