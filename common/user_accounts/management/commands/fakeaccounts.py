#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Management utility to create superusers.
"""

from django.core.management.base import BaseCommand

from common_lib.app.user_accounts.serializers import AccountLCSerializer


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
        print('fake accounts start')

        fake_user_data = {
            'password': 'fake-password',
            'groups': [],
            'permissions': []
        }

        fake_account_data = {
            'email': 'fake-email@email.com',
            'phone': '10012345678',
            'nickname': '',
            'sex': 'male',
            'job_num': '',
            'wechat': '',
            'user': fake_user_data
        }

        account_serializer = AccountLCSerializer(data=fake_account_data)
        account_serializer.is_valid()
        fake_account = account_serializer.create(
            account_serializer.validated_data)
        if fake_account:
            print('Create fake account of <%s> now'
                  % fake_user_data['username'])

        print('fake accounts over')
