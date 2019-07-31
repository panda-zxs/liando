#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from common.users.models import User
from common.utils.models import BaseModel


class AccountManager(models.Manager):
    pass


class AccountModel(BaseModel):
    user = models.OneToOneField(User,
                                related_name='account',
                                on_delete=models.CASCADE)

    nickname = models.CharField(max_length=150, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    wechat = models.CharField(max_length=30, null=True, blank=True)
    qq = models.CharField(max_length=20, null=True, blank=True)
    job_num = models.CharField(max_length=30, null=True, blank=True)
    sex = models.CharField(choices=(('male', '男性'), ('female', '女性')),
                           max_length=10, default='male')

    objects = AccountManager()

    class Meta:
        db_table = 'auth_accounts'
        ordering = ('id',)

    def get_account_permissions(self):
        return self.user.user_permissions.all()

    def get_group_permissions(self):
        ret = set()
        for group in self.user.groups.all():
            for permission in group.permissions.all():
                ret.add(permission)
        return ret

    def get_all_permissions(self):
        permission_set = set()
        permission_set |= set(self.get_account_permissions())
        permission_set |= self.get_group_permissions()
        return permission_set
