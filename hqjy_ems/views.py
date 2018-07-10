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
from ems_account.models import UserPermissionProfile
from ems_mainsite.models import SystemConfig

@login_required(login_url='user_login')
def index(request):
    context = {}
    system_config = SystemConfig.objects.all().values()[0]
    
    if system_config.get("system_open_or_close"):
        user = User.objects.filter(username = request.user.username)
        userprofile = UserPermissionProfile.objects.filter(user=request.user)
        context['user'] = user
        context['userprofile'] = userprofile
        return render(request, 'index.html', context)
    else:
        return render(request, 'system_maintenance.html', context)