import xadmin
from .models import CompanyInfo, CompanyInfoOverHead, CompanyTag, CompanyType, CompanySecondType, InternalCircular

# class ChoiceCompanySecondTypeInline(admin.TabularInline):
#     model = CompanySecondType
#     extra = 5

# Register your models here.
class CompanyInfoAdmin(object):
    list_display = ['company_name', 'company_type', 'company_area', 'company_IDcard', 'company_business_scope', 'company_registered_capital', 'responsible_person', 'responsible_person_sex', 'responsible_person_age', 'responsible_person_politics_status', 'responsible_person_education', 'contact_name', 'contact_phone', 'contact_email', 'company_web', 'contact_address', 'company_cancel', 'create_time']

    # change_form_template = 'area.html'
xadmin.site.register(CompanyInfo, CompanyInfoAdmin)

class CompanyInfoOverHeadAdmin(object):
    list_display = ['company_info_id', 'company_employee', 'company_senior_staff', 'company_job_title', 'company_registered_capital', 'company_patents_number', 'company_product', 'company_annual_income', 'company_remark']

xadmin.site.register(CompanyInfoOverHead, CompanyInfoOverHeadAdmin)

class CompanyTagAdmin(object):
    list_display = ['tag_name', 'tag_important_level']

xadmin.site.register(CompanyTag, CompanyTagAdmin)

class CompanyTypeAdmin(object):
    list_display = ['company_type_name', ]

xadmin.site.register(CompanyType, CompanyTypeAdmin)

class CompanySecondTypeAdmin(object):
    list_display = ['company_type_id', 'company_second_type_name']

xadmin.site.register(CompanySecondType, CompanySecondTypeAdmin)

class InternalCircularAdmin(object):
    list_display = ['notification_title', 'important_level', 'notification_content', 'notification_author', 'notification_date', 'notification_auto_revocation']

xadmin.site.register(InternalCircular, InternalCircularAdmin)