#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: warlock921 
# @Date: 2018-07-21 14:29:22 
# @Last Modified by:   warlock921 
# @Last Modified time: 2018-07-21 14:29:22 

from django import forms
import re
from django.forms import widgets
from django.forms import fields
from .models import CompanyInfo, CompanyInfoOverHead, CompanyType, CompanySecondType, CompanyTag

class CompanyInfoForm(forms.ModelForm):
    
    COUNTY_CHOICES = (
        ("个旧市","个旧市"),
        ("开远市","开远市"),
        ("蒙自市","蒙自市"),
        ("建水县","建水县"),
        ("石屏县","石屏县"),
        ("弥勒市","弥勒市"),
        ("泸西县","泸西县"),
        ("红河县","红河县"),
        ("元阳县","元阳县"),
        ("绿春县","绿春县"),
        ("屏边县","屏边县"),
        ("金平县","金平县"),
        ("河口县","河口县"),
        ("昆明市","昆明市"),
        ("其他地州","其他地州"),
        ("其他省市","其他省市"),
    )

    SEX_CHOICES = (
        ("男","男"),
        ("女","女"),
    )

    POLITICS_CHOICES = (
        ("党员","党员"),
        ("群众","群众"),
        ("其他","其他"),
    )

    EDUCATION_CHOICES = (
        ("初中","初中"),
        ("高中(中专)","高中(中专)"),
        ("大专","大专"),
        ("本科","本科"),
        ("本科以上","本科以上"),
    )

    BOOL_CHOICES =(
        (1,"是"),
        (2,"否"),
    )

    company_area = forms.ChoiceField(label="企业归属地", choices=COUNTY_CHOICES, widget=forms.Select(attrs={'class':"form-control"}))
    company_name = forms.CharField(label="企业名称", error_messages={'required':'企业名称不能为空'}, widget = forms.TextInput(attrs={'placeholder':"请输入企业全称",'class':"form-control"}))
    #company_type = forms.CharField(label="企业一级分类", widget=forms.Select(attrs={'class':"form-control"}))
   # company_second_type = forms.CharField(label="企业二级分类",  widget=forms.Select(attrs={'class':"form-control"}))
    company_IDcard = forms.CharField(required=False, label="企业统一信用代码", error_messages={'required':'企业统一信用代码'}, widget = forms.TextInput(attrs={'placeholder':"请输入企业统一信用代码",'class':"form-control"}))
    company_business_scope = forms.CharField(required=False, label="经营范围", widget=forms.Textarea(attrs={'class':"form-control",'rows':"3"}))
    company_registered_capital = forms.CharField(required=False, label="注册资金", error_messages={'required':'注册资金不能为空'},  widget=forms.TextInput(attrs={'class':"form-control"}))
    responsible_person =forms.CharField(required=False, label="法人/负责人姓名", error_messages={'required':'法人/负责人姓名不能为空'},  widget=forms.TextInput(attrs={'class':"form-control"}))
    responsible_person_phone = forms.CharField(required=False, max_length=11, label="法人/负责人电话", error_messages={'required':'法人/负责人电话不能为空'},  widget=forms.TextInput(attrs={'class':"form-control"}))
    responsible_person_sex = forms.ChoiceField(required=False, label="法人/负责人性别", choices=SEX_CHOICES, widget=forms.RadioSelect(attrs={'class':"radio-inline "}))
    responsible_person_age = forms.CharField(required=False, label="法人/负责人年龄", error_messages={'required':'法人年龄不能为空'},  widget=forms.TextInput(attrs={'class':"form-control"}))
    responsible_person_politics_status = forms.ChoiceField(required=False, label="法人/负责人政治面貌", choices=POLITICS_CHOICES, widget=forms.RadioSelect(attrs={'class':"radio-inline "}))
    responsible_person_education = forms.ChoiceField(required=False, label="法人/负责人文化程度", choices=EDUCATION_CHOICES, widget=forms.RadioSelect(attrs={'class':"radio-inline "}))
    contact_name = forms.CharField(required=False, label="联系人姓名", error_messages={'required':'联系人姓名不能为空'},  widget=forms.TextInput(attrs={'class':"form-control"}))
    contact_phone = forms.CharField(required=False, max_length=11, label="联系人电话", error_messages={'required':'联系人电话不能为空'},  widget=forms.TextInput(attrs={'class':"form-control"}))
    contact_email = forms.EmailField(required=False, label="Email地址", error_messages={'required':'email地址不能为空'}, widget=forms.EmailInput(attrs={'class':"form-control"}))
    company_web = forms.URLField(required=False, label="企业网址", error_messages={'required':'企业网址不能为空'}, widget=forms.URLInput(attrs={'placeholder':"请输入网址全称：例如 http://www.thinkheh.cn", 'class':"form-control"}))
    contact_address = forms.CharField(required=False, label="通讯地址", error_messages={'required':'通讯地址不能为空'},  widget=forms.TextInput(attrs={'class':"form-control"}))
    # company_cancel = models.IntegerField(choices=BOOL_CHOICES, verbose_name="公司是否注销", default=2)
    # create_time = models.DateTimeField(auto_now_add=True, verbose_name="录入系统时间")
    # create_auth = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="录入信息的用户", default=1)
    
    # 使用ModelForm时的内部类
    class Meta:
        model = CompanyInfo
        exclude = ['company_type','company_second_type', 'company_cancel', 'create_time', 'create_auth']
    
    #效验公司名称是否存在
    def clean_company_name(self):
        company_name = self.cleaned_data['company_name']
        if CompanyInfo.objects.filter(company_name=company_name).exists():
            raise forms.ValidationError('此公司已经存在，无需再次录入')
        else:
            self.cleaned_data['company_name'] = company_name
        return company_name

    #效验社会统一信用代码是否存在并且无误
    def clean_company_IDcard(self):
        company_IDcard = self.cleaned_data['company_IDcard']
        pattern = re.compile(r'[^_IOZSVa-z\W]{2}\d{6}[^_IOZSVa-z\W]{10}')

        if company_IDcard == "":
            return company_IDcard
        else:
            if pattern.match(company_IDcard) != None:
                if CompanyInfo.objects.filter(company_IDcard=company_IDcard).exists():
                    raise forms.ValidationError('您输入的社会统一信用代码已经存在')
                else:
                    self.cleaned_data['company_IDcard'] = company_IDcard
            else:
                raise forms.ValidationError('您输入的社会统一信用代码有误')
            return company_IDcard


    #效验手机号是否存在并且无误
    def clean_contact_phone(self):
        contact_phone = self.cleaned_data['contact_phone']
        pattern = re.compile(r'((\d{3,4}-)?\d{7,8})$|(1[3-9][0-9]{9})')

        if contact_phone == "":
            return contact_phone
        else:
            if pattern.match(contact_phone) != None:
                if CompanyInfo.objects.filter(contact_phone=contact_phone).exists():
                    raise forms.ValidationError('您输入的手机号码已经存在')
                else:
                    self.cleaned_data['contact_phone'] = contact_phone
            else:
                raise forms.ValidationError('请输入正确的手机号码')
            return contact_phone

    #效验法人手机号是否存在并且无误
    def clean_responsible_person_phone(self):
        responsible_person_phone = self.cleaned_data['responsible_person_phone']
        pattern = re.compile(r'((\d{3,4}-)?\d{7,8})$|(1[3-9][0-9]{9})')

        if responsible_person_phone == "":
            return responsible_person_phone
        else:
            if pattern.match(responsible_person_phone) != None:
                if CompanyInfo.objects.filter(responsible_person_phone=responsible_person_phone).exists():
                    raise forms.ValidationError('您输入的手机号码已经存在')
                else:
                    self.cleaned_data['responsible_person_phone'] = responsible_person_phone
            else:
                raise forms.ValidationError('请输入正确的手机号码')
            return responsible_person_phone


class CompanyInfoOverHeadForm(forms.ModelForm):
    COMPANYTAG = CompanyTag.objects.all()
    # company_info_id = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE, verbose_name="所属企业")
    company_tag = forms.ModelMultipleChoiceField(label="企业标签", queryset=COMPANYTAG, widget=forms.CheckboxSelectMultiple(attrs={'class':""}))
    company_employee = forms.IntegerField(required=False, label="从业人员规模", error_messages={'invalid':'请填入整数数值'},  widget=forms.TextInput(attrs={'class':"form-control"}))
    company_senior_staff = forms.IntegerField(required=False, label="大专及以上学历人数", error_messages={'invalid':'请填入整数数值'},  widget=forms.TextInput(attrs={'class':"form-control"}))
    company_job_title = forms.IntegerField(required=False, label="中级及以上职称人数", error_messages={'invalid':'请填入整数数值'},  widget=forms.TextInput(attrs={'class':"form-control"}))
    company_patents_number = forms.IntegerField(required=False, label="企业拥有专利个数", error_messages={'invalid':'请填入整数数值'},  widget=forms.TextInput(attrs={'class':"form-control"}))
    company_product = forms.CharField(required=False, label="主要产品/服务", widget=forms.Textarea(attrs={'class':"form-control",'rows':"3"}))
    company_annual_income = forms.IntegerField(required=False, label="企业年产值（ 万元 ）", error_messages={'invalid':'请填入整数数值'},  widget=forms.TextInput(attrs={'class':"form-control"}))
    company_remark = forms.CharField(required=False, label="备注", widget=forms.Textarea(attrs={'class':"form-control",'rows':"3"}))

    # 使用ModelForm时的内部类
    class Meta:
        model = CompanyInfoOverHead
        exclude = ['company_info_id', 'company_tag', 'create_time', 'create_auth']

    #效验是否为数字类型
    def clean_company_employee(self):
        company_employee = self.cleaned_data['company_employee']
        if company_employee == None:
            company_employee = 0
            return company_employee
        else:
            try:
                company_employee_zh = int(company_employee)
            except ValueError as e:
                raise forms.ValidationError('从业人员规模只能为正整数')
            else:
                self.cleaned_data['company_employee'] = company_employee_zh

            return company_employee

    #效验是否为数字类型
    def clean_company_senior_staff(self):
        company_senior_staff = self.cleaned_data['company_senior_staff']
        if company_senior_staff == None:
            company_senior_staff = 0
            return company_senior_staff
        else:
            try:
                company_senior_staff_zh = int(company_senior_staff)
            except ValueError as e:
                raise forms.ValidationError('大专及以上学历人数只能为正整数')
            else:
                self.cleaned_data['company_senior_staff'] = company_senior_staff_zh

            return company_senior_staff

    #效验是否为数字类型
    def clean_company_job_title(self):
        company_job_title = self.cleaned_data['company_job_title']
        if company_job_title == None:
            company_job_title = 0
            return company_job_title
        else:
            try:
                company_job_title_zh = int(company_job_title)
            except ValueError as e:
                raise forms.ValidationError('中级及以上职称人数只能为正整数')
            else:
                self.cleaned_data['company_job_title'] = company_job_title_zh

            return company_job_title

    #效验是否为数字类型
    def clean_company_patents_number(self):
        company_patents_number = self.cleaned_data['company_patents_number']
        if company_patents_number == None:
            company_patents_number = 0
            return company_patents_number
        else:
            try:
                company_patents_number_zh = int(company_patents_number)
            except ValueError as e:
                raise forms.ValidationError('大专及以上学历人数只能为正整数')
            else:
                self.cleaned_data['company_patents_number'] = company_patents_number_zh

            return company_patents_number

    #效验是否为数字类型
    def clean_company_annual_income(self):
        company_annual_income = self.cleaned_data['company_annual_income']
        if company_annual_income == None:
            company_annual_income = 0
            return company_annual_income
        else:
            try:
                company_annual_income_zh = int(company_annual_income)
            except ValueError as e:
                raise forms.ValidationError('中级及以上职称人数只能为正整数')
            else:
                self.cleaned_data['company_annual_income'] = company_annual_income_zh

            return company_annual_income