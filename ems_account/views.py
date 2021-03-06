#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: warlock921
# @Date: 2018-07-08 01:49:13
# @Last Modified by:   warlock921
# @Last Modified time: 2018-07-08 01:49:13

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import LoginForm
from .models import UserPermissionProfile, UserLevel
from hqjy_ems.check_system import check_system_open


#用户登录视图
@check_system_open(redirect='/system_maintenance/')
def user_login(request):
    context = {}
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            #获取用户客户端信息和IP地址
            agent = request.META.get('HTTP_USER_AGENT')
            user_ip = request.META.get('REMOTE_ADDR')

            user_id = User.objects.filter(username=user).values()[0].get('id')
            user_profile = UserPermissionProfile.objects.get(user_id=user_id)

            user_profile.user_agent = agent
            user_profile.user_ip = user_ip
            user_profile.save()

            return HttpResponseRedirect( "/")
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect( "/")
        else:
            login_form = LoginForm()
    context['login_form'] = login_form
    return render(request, 'ems_account/login.html', context)

@login_required(login_url='user_login')
@csrf_exempt
@check_system_open(redirect='/system_maintenance/')
def userinfo_detail(request, user_id):
    user_profile = UserPermissionProfile.objects.get(user_id=user_id)
    user_level = UserLevel.objects.filter(pk=user_profile.user_level_id)
    context = {}
    context['user_profile'] = user_profile
    context['user_level'] = user_level
    return render(request, 'ems_account/userinfo_detail.html', context)

@login_required(login_url='user_login')
@csrf_exempt
@check_system_open(redirect='/system_maintenance/')
def userinfo_edit(request):
    context = {}
    return render(request, 'ems_account/userinfo_edit.html', context)
