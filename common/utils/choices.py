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
    ('set', _(u'重置')),
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

OPERATION_OBJ = {
    'Group': '组',
    'User': '人员',
    'MessagePush': '消息推送',
    'MyObtain': '生成jwt',
    'MyFetch': '获取jwt',
    'Account': '用户',
    'AccountPermission': '用户权限',
    'AccountInfo': '用户详情',
    'GroupUser': '组成员',
    'GroupPermission': '组权限',
    'GroupRelation': '组层级关系',
    'GroupTreeView': '组织架构',
    'Logout': '登出',
    'Login': '登陆',

}

OPERATION_METHOD = {
    'DELETE': '删除',
    'PUT': '更新',
    'PATCH': '更新',
    'POST': '创建',
}
