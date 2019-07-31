#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):

    page_size_query_param = 'page_size'
