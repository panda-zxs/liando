#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.GroupLCView.as_view()),

    path(r'delete/', views.GroupDView.as_view()),

    path(r'<int:id>/',
         views.GroupRUDView.as_view()),

    path(r'<int:id>/users/',
         views.GroupUserRUView.as_view()),

    path(r'<int:id>/permissions/',
         views.GroupPermissionRUView.as_view()),

    path(r'<int:id>/relations/',
         views.GroupRelationRView.as_view()),

    path(r'tree/', views.GroupTreeView.as_view()),

    path(r'<name>/info/', views.GroupLookUpView.as_view()),

    path(r'<int:id>/name/', views.GroupNameView.as_view()),

    # path(r'<name>/users/', views.DepartmentAccountView.as_view())
]
