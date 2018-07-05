from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#企业类型表
class CompanyType(models.Model):
    company_type_name = models.CharField(max_length=50, verbose_name="企业一级产业分类")

    def __str__(self):
        return self.company_type_name

    class Meta:
        verbose_name_plural = "企业一级产业分类"

class CompanySecondType(models.Model):
    company_second_type_name = models.CharField(max_length=50, verbose_name="企业二级产业分类")
    company_type_id = models.ForeignKey(CompanyType, on_delete=models.CASCADE, verbose_name="企业一级产业分类")

    def __str__(self):
        return self.company_second_type_name

    class Meta:
        verbose_name_plural = "企业二级产业分类"



#标签表
class CompanyTag(models.Model):
    
    LEVEL_CHOICES = (
        (1,"特别重要"),
        (2,"非常重要"),
        (3,"一般重要"),
    )

    tag_name = models.CharField(max_length=50, verbose_name="标签名称")
    tag_important_level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="重要级别", default=3)

    def __str__(self):
        return self.tag_name
    
    class Meta:
        ordering = ['-tag_important_level', ]
        verbose_name_plural = "企业标签"

#企业信息表
class CompanyInfo(models.Model):
    
    COUNTY_CHOICES = (
        (1,"个旧市"),
        (2,"开远市"),
        (3,"蒙自市"),
        (4,"建水县"),
        (5,"石屏县"),
        (6,"弥勒市"),
        (7,"泸西县"),
        (8,"红河县"),
        (9,"元阳县"),
        (10,"绿春县"),
        (11,"屏边县"),
        (12,"金平县"),
        (13,"河口县"),
    )

    SEX_CHOICES = (
        (1,"男"),
        (2,"女"),
    )

    POLITICS_CHOICES = (
        (1,"党员"),
        (2,"群众"),
        (3,"其他"),
    )

    EDUCATION_CHOICES = (
        (1,"初中"),
        (2,"高中(中专)"),
        (3,"大专"),
        (4,"本科"),
        (5,"本科以上"),
    )

    BOOL_CHOICES =(
        (1,"是"),
        (2,"否"),
    )

    company_name = models.CharField(max_length=200, verbose_name="企业名称")
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE, related_name="company_type_id", verbose_name="企业一级产业分类")
    company_second_type = models.ForeignKey(CompanySecondType, on_delete=models.CASCADE, related_name="company_second_type_id", verbose_name="企业二级产业分类", default=1)
    company_area = models.IntegerField(choices=COUNTY_CHOICES, verbose_name="企业归属地", default=1)
    company_IDcard = models.CharField(max_length=18, verbose_name="企业统一信用代码", blank=True)
    company_business_scope = models.TextField(max_length=500, verbose_name="企业经营范围", blank=True)
    company_registered_capital = models.CharField(max_length=50, verbose_name="企业注册资金", blank=True)
    responsible_person = models.CharField(max_length=50, verbose_name="企业法人/负责人姓名")
    responsible_person_sex = models.IntegerField(choices=SEX_CHOICES, verbose_name="企业法人性别", default=1)
    responsible_person_age = models.CharField(max_length=2, verbose_name="企业法人年龄", blank=True)
    responsible_person_politics_status = models.IntegerField(choices=POLITICS_CHOICES, verbose_name="企业法人政治面貌", default=2)
    responsible_person_education = models.IntegerField(choices=EDUCATION_CHOICES, verbose_name="企业法人文化程度", default=3)
    contact_name = models.CharField(max_length=50, verbose_name="企业联系人姓名", blank=True)
    contact_phone = models.CharField(max_length=11, verbose_name="企业联系人电话", blank=True)
    contact_email = models.EmailField(verbose_name="企业联系人email", blank=True)
    company_web = models.URLField(verbose_name="企业网站地址", blank=True)
    contact_address = models.CharField(max_length=200, verbose_name="企业通讯地址", blank=True)
    company_cancel = models.IntegerField(choices=BOOL_CHOICES, verbose_name="公司是否注销", default=2)
    #company_tag = models.ManyToManyField(CompanyTag ,related_name="company_info_to_tag")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="录入系统时间")

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ['-create_time', ]
        verbose_name_plural = "企业基础信息"


#企业附加信息表
class CompanyInfoOverHead(models.Model):
    company_info_id = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE, verbose_name="所属企业")
    company_tag = models.ManyToManyField(CompanyTag, related_name="company_tag_for_company", verbose_name="企业标签")
    company_employee = models.IntegerField(verbose_name="企业从业人员规模", blank=True)
    company_senior_staff = models.IntegerField(verbose_name="企业大专及以上学历人数", blank=True)
    company_job_title = models.IntegerField(verbose_name="企业中级及以上职称人数", blank=True)
    company_registered_capital = models.IntegerField(verbose_name="企业注册资金", blank=True)
    company_patents_number = models.IntegerField(verbose_name="企业拥有专利个数", blank=True)
    company_product = models.TextField(verbose_name="企业主要产品/服务", blank=True)
    company_annual_income = models.IntegerField(verbose_name="企业年产值", blank=True)
    company_remark = models.TextField(verbose_name="企业备注", blank=True)

    def __str__(self):
        return self.company_info_id

    class Meta:
        verbose_name_plural = "企业附加信息"


#内置通知表
class InternalCircular(models.Model):

    LEVEL_CHOICES = (
        (1,"特别重要"),
        (2,"非常重要"),
        (3,"一般重要"),
    )

    notification_title = models.CharField(max_length=200, verbose_name="通知标题")
    important_level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="通知重要级别", default=3)
    notification_content = models.TextField(verbose_name="通知内容")
    notification_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="通知作者")
    notification_date = models.DateField(auto_now_add=True, verbose_name="通知生成日期")
    notification_auto_revocation = models.DateField(verbose_name="通知自动撤销日期")

    def __str__(self):
        return self.notification_title

    class Meta:
        ordering = ['-notification_date', ]
        verbose_name_plural = "内置通知表"
