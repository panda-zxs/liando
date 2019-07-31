#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import auth

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from common.utils.log import getLogger

from .serializers import LoginSerializer
from .serializers import LogoutSerializer
from .serializers import UserUpdateSerializer
from .models import User

LOG = getLogger(__name__)


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            auth.login(request, user)
            LOG.info('User <%s> login success',
                     user.username)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)


class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        auth.logout(request)
        LOG.info('User <%s> logout success',
                 request.user.username)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SetPassword(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = ()
    queryset = User.objects.filter(
        is_active=True)
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    lookup_field = 'id'
