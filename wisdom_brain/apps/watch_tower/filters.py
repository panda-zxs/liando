#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django_filters import rest_framework as filters

from .models import Company


class StatisticFilter(filters.FilterSet):
    area_id = filters.CharFilter()
    industry_id = filters.NumberFilter()

    class Meta:
        model = Company
        fields = ('area_id', 'industry_id')
