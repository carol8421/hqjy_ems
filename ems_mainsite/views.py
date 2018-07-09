from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ems_account.models import UserPermissionProfile

# Create your views here.


@login_required(login_url='ems_account/login/')
def index_query(request):
    context = {}
    return render(request, "index_query.html", context)

@login_required(login_url='ems_account/login/')
def index_workbench(request):
    context = {}
    user_level = UserPermissionProfile.objects.filter(user=request.user).values()[0].get('user_level_id')
    if user_level == 4:
        return redirect("index_query")
    else:
        return render(request, "index_workbench.html", context)

