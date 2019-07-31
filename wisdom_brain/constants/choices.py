#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _


SEX_CHOICES = (
    ('male', _(u'男性')),
    ('female', _(u'女性')),
)

OP_CHOICES = (
    ('add', _(u'添加')),
    ('del', _(u'删除')),
)

GROUP_TYPE_CHOICES = (
    ('user', _(u'部门')),
    ('permission', _(u'权限组')),
    ('notice', _(u'通知组')),
)

NOTICE_TYPE_CHOICES = (
    ('plat', _(u'平台')),
    ('email', _(u'邮箱')),
    ('message', _(u'短信')),
    ('wechat', _(u'微信'))
)

NOTICE_PRIORITY_CHOICES = (
    ('high', _(u'高')),
    ('middle', _(u'中')),
    ('low', _(u'低'))
)

OPERATION_TYPE_CHOICES = (
    ('user', _(u'个人信息')),
    ('admin', _(u'后台管理')),
    ('equipment', _(u'设备监控与告警'))
)
