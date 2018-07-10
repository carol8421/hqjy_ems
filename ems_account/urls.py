#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: warlock921 
# @Date: 2018-07-08 02:30:52 
# @Last Modified by:   warlock921 
# @Last Modified time: 2018-07-08 02:30:52 

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.user_login, name="user_login"),
    path('logout/', auth_views.logout, {"template_name": "ems_account/logout.html"}, name="user_logout"),
    path('userinfo-detail/', views.userinfo_detail, name="userinfo_detail"),
    path('userinfo-edit/', views.userinfo_edit, name="userinfo_edit"),
]