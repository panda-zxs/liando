#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from . import docs
from . import filters as account_filter
from . import serializers as account_serializer

from .models import AccountModel


class AccountLCView(ListCreateAPIView):
    response_docs = docs.doc_exp(docs.AccountLCView_FAKER)

    serializer_class = account_serializer.AccountLCSerializer
    permission_classes = ()
    queryset = AccountModel.objects.filter(
        deleted=False).prefetch_related('user')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    filter_class = account_filter.AccountFilter

    def get(self, request, *args, **kwargs):
        """
        获取账号列表

        """
        return super(AccountLCView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        创建账号

        支持Markdown
        - f
        - x

        ```shell
        python abc
        ```
        """
        return super(AccountLCView, self).post(request, *args, **kwargs)


class AccountRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = account_serializer.AccountRUDSerializer
    permission_classes = ()
    queryset = AccountModel.objects.filter(
        deleted=False).prefetch_related('user')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    lookup_field = 'id'


class AccountPermissionRUView(RetrieveUpdateAPIView):
    serializer_class = account_serializer.AccountPermissionSerializer
    permission_classes = ()
    queryset = AccountModel.objects.all().prefetch_related('user')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    lookup_field = 'id'


class AccountInfoView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = account_serializer.AccountInfoSerializer

    def get(self, request, *args, **kwargs):
        if request.user is not None:
            serializer = account_serializer.AccountInfoSerializer(request.user)
            data = {'results': serializer.data}
            return Response(status=status.HTTP_200_OK, data=data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data='please login')
