from django.contrib import admin
from ems_mainsite.models import CompanyInfo, CompanyInfoOverHead, CompanyTag, CompanyType, InternalCircular

# Register your models here.
@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = []

@admin.register(CompanyInfoOverHead)
class CompanyInfoOverHeadAdmin(admin.ModelAdmin):
    list_display = ['company_info_id', 'business_contact_flag']

@admin.register(CompanyTag)
class CompanyTagAdmin(admin.ModelAdmin):
    list_display = ['tag_name', 'tag_important_level']

@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ['company_type_name', ]

@admin.register(InternalCircular)
class InternalCircularAdmin(admin.ModelAdmin):
    list_display = ['notification_title', 'important_level', 'notification_content', 'notification_author', 'notification_date', 'notification_auto_revocation']