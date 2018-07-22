from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from ems_account.models import UserPermissionProfile
from .models import InternalCircular
from hqjy_ems.check_system import check_system_open
from .froms import CompanyInfoForm, CompanyInfoOverHeadForm

# Create your views here.


@login_required(login_url='user_login')
@check_system_open(redirect='/system_maintenance/')
def index_query(request):
    context = {}
    return render(request, "index_query.html", context)


@login_required(login_url='user_login')
@check_system_open(redirect='/system_maintenance/')
def index_workbench(request):
    context = {}
    user_level = UserPermissionProfile.objects.filter(
        user=request.user).values()[0].get('user_level_id')

    #通知视图
    today = timezone.now().date()
    # 取得自动撤销日期大于当天的通知
    notification_list = InternalCircular.objects.filter(
        notification_auto_revocation__gt=today, notification_revocation_flag=False)
    
    if request.method == 'GET':
        company_info = CompanyInfoForm()
        company_Info_over_head = CompanyInfoOverHeadForm()

    context['user_level'] = user_level
    context['notification_list'] = notification_list
    context['company_info'] = company_info
    context['company_Info_over_head'] = company_Info_over_head


    #判断用户级别，是否有使用workbench的权限
    if user_level == 4:
        return redirect("index_query")
    else:
        return render(request, "index_workbench.html", context)

    

@login_required(login_url='user_login')
@check_system_open(redirect='/system_maintenance/')
def notification_detail(request, Internalcircular_pk):
    current_notification = get_object_or_404(InternalCircular, pk=Internalcircular_pk)
    context = {}
    context['current_notification'] = current_notification
    return render(request, "ems_mainsite/notification_detail.html", context)
