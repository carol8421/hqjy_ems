#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: warlock921 
# @Date: 2018-07-07 22:11:46 
# @Last Modified by:   warlock921 
# @Last Modified time: 2018-07-07 22:11:46 
 
from django.contrib.auth.models import User
from django.db import models

class UserLevel(models.Model):
    ''' 用户级别表 '''
    level_name = models.CharField(max_length=20, verbose_name="用户级别设置")
    level_describe = models.TextField(verbose_name="此级别具备权限描述")

    def __str__(self):
        return self.level_name
    
    class Meta:
        verbose_name_plural = "用户级别设置"

class UserPermissionProfile(models.Model):
    ''' 用户附加信息表 '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, verbose_name="对应用户")
    user_level = models.ForeignKey(UserLevel, on_delete=models.CASCADE, related_name="user_level", verbose_name="用户级别")
    user_phone = models.CharField(max_length=11, unique=True, verbose_name="用户联系电话")
    #用户浏览器信息，每次登陆都会获取
    user_agent = models.CharField(max_length=500, blank=True, verbose_name="用户浏览器信息")
    #用户IP地址，每次登陆都会获取
    user_ip = models.CharField(max_length=18, blank=True, verbose_name="用户登录IP")
  
    def __str__(self):
        return self.user_phone
    
    class Meta:
        verbose_name_plural = "用户附加信息设置"

