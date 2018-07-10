from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from ems_account.models import UserPermissionProfile
from .models import InternalCircular

# Create your views here.


@login_required(login_url='user_login')
def index_query(request):
    context = {}
    return render(request, "index_query.html", context)


@login_required(login_url='user_login')
def index_workbench(request):
    context = {}
    user_level = UserPermissionProfile.objects.filter(
        user=request.user).values()[0].get('user_level_id')
    if user_level == 4:
        return redirect("index_query")
    else:
        return render(request, "index_workbench.html", context)

@login_required(login_url='user_login')
def notification_index(request):
    today = timezone.now().date()
    #取得自动撤销日期大于当天的通知
    notification_list = InternalCircular.objects.filter(notification_auto_revocation__gt=today, notification_revocation_flag=False)
    print("这里有结果：%s" %  notification_list)
    context = {}
    context['notification_list'] = notification_list
    context['flag'] = "我过来了"
    return render(request, "ems_mainsite/notification.html", context)

