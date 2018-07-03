from django.contrib import admin
from .models import CompanyInfo, CompanyInfoOverHead, CompanyProduct, CompanyTag, CompanyType, MyCompanyProductList, InternalCircular

# Register your models here.
@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_type', 'responsible_person', 'contact_name', 'contact_phone', 'contact_email', 'contact_QQ', 'contact_Ding', 'contact_address', 'create_time']

@admin.register(CompanyInfoOverHead)
class CompanyInfoOverHeadAdmin(admin.ModelAdmin):
    list_display = ['company_info_id', 'business_contact_flag']

@admin.register(CompanyProduct)
class CompanyProductAdmin(admin.ModelAdmin):
    list_display = ['company_info_id', 'cproduct_name', 'cproducts_type', 'cproduct_market_price', 'cproduct_internal_price', 'cproduct_in_storage_date', 'cproduct_on_sale']

@admin.register(CompanyTag)
class CompanyTagAdmin(admin.ModelAdmin):
    list_display = ['tag_name', 'tag_important_level']

@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ['company_type_name', ]

@admin.register(MyCompanyProductList)
class MyCompanyProductListAdmin(admin.ModelAdmin):
    list_display = ['mproduct_name', 'mproducts_makers', 'mproduct_market_price', 'mproduct_internal_price', 'mproduct_in_storage_date', 'mproduct_update_time', 'mproduct_on_sale']

@admin.register(InternalCircular)
class InternalCircularAdmin(admin.ModelAdmin):
    list_display = ['notification_title', 'important_level', 'notification_content', 'notification_author', 'notification_date', 'notification_auto_revocation']