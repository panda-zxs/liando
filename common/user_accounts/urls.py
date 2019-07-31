#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.AccountLCView.as_view()),
    path(r'<int:id>/',
         views.AccountRUDView.as_view()),
    path(r'<int:id>/permissions/',
         views.AccountPermissionRUView.as_view()),
    path(r'info/', views.AccountInfoView.as_view()),
]
