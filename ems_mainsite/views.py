from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.core import serializers
from ems_account.models import UserPermissionProfile
from .models import InternalCircular, CompanyType, CompanySecondType
from hqjy_ems.check_system import check_system_open
from .forms import CompanyInfoForm, CompanyInfoOverHeadForm

# Create your views here.


@login_required(login_url='user_login')
@check_system_open(redirect='/system_maintenance/')
def index_query(request):
    context = {}
    return render(request, "index_query.html", context)

#工作台主页视图
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
        context['company_info'] = company_info
        context['company_Info_over_head'] = company_Info_over_head

    context['user_level'] = user_level
    context['notification_list'] = notification_list
    


    #判断用户级别，是否有使用workbench的权限
    if user_level == 4:
        return redirect("index_query")
    else:
        return render(request, "index_workbench.html", context)

    
#显示指定的通知视图
@login_required(login_url='user_login')
@check_system_open(redirect='/system_maintenance/')
def notification_detail(request, Internalcircular_pk):
    current_notification = get_object_or_404(InternalCircular, pk=Internalcircular_pk)
    context = {}
    context['current_notification'] = current_notification
    return render(request, "ems_mainsite/notification_detail.html", context)

#获取企业一级分类信息-返回Json数据
@login_required(login_url='user_login')
@check_system_open(redirect='/system_maintenance/')
@csrf_exempt
def get_company_type_data(request):
    company_type = CompanyType.objects.all()
    json_data = serializers.serialize("json", company_type)
    return HttpResponse(json_data,content_type="application/json")

#获取企业二级分类信息-返回Json数据
@login_required(login_url='user_login')
@check_system_open(redirect='/system_maintenance/')
@csrf_exempt
def get_company_second_type_data(request):
    company_type_id = request.POST.get('company_type_id')
    company_second_type = CompanySecondType.objects.filter(company_type_id=company_type_id)
    #print(company_second_type)
    json_data = serializers.serialize("json", company_second_type)
    return HttpResponse(json_data,content_type="application/json")

#提交录入用户主信息数据视图
@login_required(login_url='user_login')
@check_system_open(redirect='/system_maintenance/')
@csrf_exempt
def input_data_submit(request):
    if request.method == 'POST':
        company_info_form = CompanyInfoForm(request.POST)
        print(request.POST)
        print(company_info_form.is_valid())
        company_type_id = request.POST.get('company_type')
        company_second_type_id = request.POST.get('company_second_type')
        print(company_type_id, company_second_type_id)
        if company_info_form.is_valid():
            new_company_info_form = company_info_form.save(commit=False)
            new_company_info_form.company_name = company_info_form.cleaned_data['company_name']
            new_company_info_form.company_type_id = company_type_id
            new_company_info_form.company_second_type_id = company_second_type_id
            new_company_info_form.company_IDcard = company_info_form.cleaned_data['company_IDcard']
            new_company_info_form.contact_phone = company_info_form.cleaned_data['contact_phone']
            new_company_info_form.save()
            #转换页面视图至用户附加信息
            ci_id = new_company_info_form.pk
            return HttpResponseRedirect(reverse('input_overhead_data_submit', args=[ci_id]))
        else:
            context = {}
            context ['company_info'] = company_info_form
            return render(request, 'index_workbench.html', context)

#提交录入用户附加信息数据视图
@login_required(login_url='user_login')
@check_system_open(redirect='/system_maintenance/')
@csrf_exempt
def input_overhead_data_submit(request, ci_id):
    context = {}
    if request.method == 'GET':
         company_overhead_info_form = CompanyInfoOverHeadForm()
         ci_id = ci_id
         context['ci_id'] = ci_id
         context['company_info'] = company_overhead_info_form
         return render(request, "index_workbench.html", context)
    elif request.method == 'POST':
        company_overhead_info_form = CompanyInfoOverHeadForm(request.POST)
        company_tag_list = request.POST.getlist("company_tag")
        print(company_tag_list)
        print(company_overhead_info_form)
        print(company_overhead_info_form.is_valid())
        if company_overhead_info_form.is_valid():
            new_company_oh_info_form = company_overhead_info_form.save(commit=False)
            new_company_oh_info_form.company_info_id_id = ci_id
            new_company_oh_info_form.company_employee = company_overhead_info_form.cleaned_data['company_employee']
            new_company_oh_info_form.company_senior_staff = company_overhead_info_form.cleaned_data['company_senior_staff']
            new_company_oh_info_form.company_job_title = company_overhead_info_form.cleaned_data['company_job_title']
            new_company_oh_info_form.company_annual_income = company_overhead_info_form.cleaned_data['company_annual_income']
            new_company_oh_info_form.save()

            for company_tag_id in company_tag_list:
                new_company_oh_info_form.company_tag.add(company_tag_id)
                new_company_oh_info_form.save()

            return HttpResponseRedirect(reverse('index_workbench'))
    else:
        pass 