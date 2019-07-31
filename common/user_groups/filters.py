#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group

from django_filters import rest_framework as filters

from common.utils import choices


class GroupFilter(filters.FilterSet):
    group_type = filters.ChoiceFilter(label='group_type',
                                      choices=choices.GROUP_TYPE_CHOICES,
                                      method='filter_by_group_type')
    name_like = filters.CharFilter(label='name_like',
                                   method='filter_by_pattern_name')

    class Meta:
        model = Group
        fields = ('group_type',)

    @classmethod
    def filter_by_group_type(cls, queryset, _, value):
        return queryset.filter(profile__group_type=value)

    @classmethod
    def filter_by_pattern_name(cls, queryset, _, value):
        return queryset.filter(name__contains=value)


class GroupTreeFilter(filters.FilterSet):
    group_type = filters.ChoiceFilter(label='group_type',
                                      choices=choices.GROUP_TYPE_CHOICES,
                                      method='filter_by_group_type')

    class Meta:
        model = Group
        fields = ('group_type',)

    @classmethod
    def filter_by_group_type(cls, queryset, _, value):
        query = queryset.filter(profile__group_type=value)
        return query
