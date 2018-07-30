#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: warlock921
# @Date: 2018-07-08 01:59:06
# @Last Modified by:   warlock921
# @Last Modified time: 2018-07-08 01:59:06

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ems_account.models import UserPermissionProfile
from ems_mainsite.models import InternalCircular
from .check_system import check_system_open

def check_system_open_or_close(request):
    context = {}
    return render(request, 'system_maintenance.html', context)
    
@login_required(login_url='user_login')
@check_system_open(redirect='/system_maintenance/')
def index(request):
    context = {}
    user = User.objects.filter(username=request.user.username)
    userprofile = UserPermissionProfile.objects.filter(user=request.user)

    today = timezone.now().date()
    # 取得自动撤销日期大于当天的通知
    notification_list = InternalCircular.objects.filter(
        notification_auto_revocation__gt=today, notification_revocation_flag=False)[:3]

    context['user'] = user
    context['userprofile'] = userprofile
    context['notification_list'] = notification_list
    return render(request, 'index.html', context)
