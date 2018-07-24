#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: warlock921 
# @Date: 2018-07-09 01:26:04 
# @Last Modified by:   warlock921 
# @Last Modified time: 2018-07-09 01:26:04 

from django.urls import path
from . import views

urlpatterns = [
    path('query/', views.index_query, name='index_query'),
    path('workbench/', views.index_workbench, name='index_workbench'),
    path('notification/<int:Internalcircular_pk>', views.notification_detail, name='notification_detail'),
     path('get-type-data/', views.get_company_type_data, name='get_company_type_data'),
    path('get-second-type-data/', views.get_company_second_type_data, name='get_company_second_type_data'),
]