#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class MyAuthBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            email = kwargs.get('email')
            user = UserModel.objects.all().prefetch_related(
                'account').only('username').get(
                    account__email=email)
        except UserModel.DoesNotExist:
            msg = 'User account is not found.'
            raise ValidationError(msg)
        else:
            if not user.check_password(password):
                msg = 'User password is wrong.'
                raise ValidationError(msg)
            if not self.user_can_authenticate(user):
                msg = 'User account is not active.'
                raise ValidationError(msg)
            return user
