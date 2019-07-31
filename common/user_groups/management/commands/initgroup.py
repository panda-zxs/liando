#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Management utility to create superusers.
"""

from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Used to sync permission profiles.'
    requires_migrations_checks = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        pass

    def execute(self, *args, **options):
        return super().execute(*args, **options)

    def handle(self, *args, **options):
        print('init group start')
        ROOT_GROUP_NAME = 'root'

        Group = apps.get_model('auth',
                               'Group')
        GroupProfile = apps.get_model('user_groups',
                                      'GroupProfileModel')
        group, created = Group.objects.update_or_create(
            name=ROOT_GROUP_NAME
        )
        _, created = GroupProfile.objects.update_or_create(
            group=group
        )
        if created:
            print('Create group of <%s> now' % group.name)
        print('init group over')
