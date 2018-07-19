#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: warlock921
# @Date: 2018-07-18 19:42:56
# @Last Modified by:   warlock921
# @Last Modified time: 2018-07-18 19:42:56

from functools import wraps
from django.http import HttpResponseRedirect, Http404
from ems_mainsite.models import SystemConfig


def check_system_open(func=None, redirect=None):
    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            system_config = SystemConfig.objects.all().values()[0]
            if system_config.get("system_open_or_close") == False:
                return HttpResponseRedirect(redirect)
            else:
                return func(request, *args, **kwargs)
        return returned_wrapper
    return decorator
