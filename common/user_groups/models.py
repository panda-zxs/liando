#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.db import models

from common.utils import choices
from common.utils.models import BaseModel


class GroupProfileModel(BaseModel):
    group = models.OneToOneField(Group,
                                 related_name='profile',
                                 on_delete=models.CASCADE)
    group_name = models.CharField(max_length=32,
                                  null=False,
                                  blank=False)
    parent_group = models.ForeignKey(Group,
                                     related_name='child_set',
                                     null=True,
                                     on_delete=models.CASCADE)
    group_type = models.CharField(max_length=32,
                                  choices=choices.GROUP_TYPE_CHOICES,
                                  default='user')

    class Meta:
        db_table = 'auth_group_profiles'
        ordering = ('id',)

    def get_relation_repr(self):
        child_groups = map(lambda x: x.get_relation_repr(),
                           self.group.child_set.filter(deleted=False))
        ret = {
            'id': self.group.id,
            'name': self.group_name,
            'group_type': self.group_type,
            'children': child_groups,
        }
        return ret

    def get_sub_relation(self, subs):
        subs.append(self.group.id)
        if not self.group.child_set.all().values():
            for child in self.group.child_set.all():
                child.get_sub_relation(subs)
        return subs
