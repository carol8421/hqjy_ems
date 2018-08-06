from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from import_export import resources

#创建外键值的序列化函数
class CompanyTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name = name)

#创建外键值的序列化函数
class CompanyInfoOverHeadManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name = name)

#企业一级产业分类表
class CompanyType(models.Model):
    objects = CompanyTypeManager()
    company_type_name = models.CharField(max_length=50, verbose_name="企业一级产业分类")

    def __str__(self):
        return self.company_type_name

    def natural_key(self):
        return self.company_type_name

    class Meta:
        verbose_name_plural = "企业一级产业分类"
        unique_together = (('company_type_name',),)

#企业二级产业分类表
class CompanySecondType(models.Model):
    objects = CompanyInfoOverHeadManager()
    company_second_type_name = models.CharField(max_length=50, verbose_name="企业二级产业分类")
    company_type_id = models.ForeignKey(CompanyType, on_delete=models.CASCADE, verbose_name="企业一级产业分类")

    def __str__(self):
        return self.company_second_type_name

    def natural_key(self):
        return self.company_second_type_name

    class Meta:
        verbose_name_plural = "企业二级产业分类"
        unique_together = (('company_second_type_name',),)


#企业信息表
class CompanyInfo(models.Model):
    
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

    company_name = models.CharField(max_length=200, verbose_name="企业名称")
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE, related_name="company_type_id", verbose_name="企业一级产业分类", default=1)
    company_second_type = models.ForeignKey(CompanySecondType, on_delete=models.CASCADE, related_name="company_second_type_id", verbose_name="企业二级产业分类", default=1)
    company_area = models.CharField(max_length=50, choices=COUNTY_CHOICES, verbose_name="企业归属地", default="蒙自市")
    company_IDcard = models.CharField(max_length=18, verbose_name="企业统一信用代码", blank=True)
    company_business_scope = models.TextField(max_length=500, verbose_name="经营范围", blank=True)
    company_registered_capital = models.CharField(max_length=50, verbose_name="注册资金", blank=True)
    responsible_person = models.CharField(max_length=50, verbose_name="法人/负责人姓名")
    responsible_person_phone = models.CharField(max_length=11, verbose_name="法人/负责人电话", blank=True)
    responsible_person_sex = models.CharField(max_length=4, choices=SEX_CHOICES, verbose_name="法人/负责人性别", default="男")
    responsible_person_age = models.CharField(max_length=2, verbose_name="法人/负责人年龄", blank=True)
    responsible_person_politics_status = models.CharField(max_length=10, choices=POLITICS_CHOICES, verbose_name="法人/负责人政治面貌", default="群众")
    responsible_person_education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, verbose_name="法人/负责人文化程度", default="大专")
    contact_name = models.CharField(max_length=50, verbose_name="联系人姓名", blank=True)
    contact_phone = models.CharField(max_length=11, verbose_name="联系人电话", blank=True)
    contact_email = models.EmailField(verbose_name="联系人email", blank=True)
    company_web = models.URLField(verbose_name="网站地址", blank=True)
    contact_address = models.CharField(max_length=200, verbose_name="通讯地址", blank=True)
    company_cancel = models.IntegerField(choices=BOOL_CHOICES, verbose_name="企业是否注销", default=2)
    #company_tag = models.ManyToManyField(CompanyTag ,related_name="company_info_to_tag")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="录入系统时间")
    create_auth = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="录入信息的用户", default=1)

    def __str__(self):
        return self.company_name
        
    class Meta:
        ordering = ['-create_time', ]
        verbose_name_plural = "企业基础信息"

#创建外键值的序列化函数
class CompanyTagManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name = name)

#标签表
class CompanyTag(models.Model):
    
    LEVEL_CHOICES = (
        (1,"特别重要"),
        (2,"非常重要"),
        (3,"一般重要"),
    )

    tag_name = models.CharField(max_length=50, verbose_name="标签名称")
    tag_important_level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="重要级别", default=3)
    #company_info = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name='company_info_tag', verbose_name='企业基础信息')

    def __str__(self):
        return self.tag_name
    
    def natural_key(self):
        return self.tag_name
      
    class Meta:
        ordering = ['tag_important_level', ]
        verbose_name_plural = "企业标签"
        unique_together = (('tag_name',),)

#企业附加信息表
class CompanyInfoOverHead(models.Model):
    company_info_id = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE, verbose_name="所属企业")
    company_tag = models.ManyToManyField(CompanyTag, related_name="company_tag_for_company", verbose_name="企业标签")
    company_employee = models.IntegerField(verbose_name="从业人员规模", blank=True, default=0)
    company_senior_staff = models.IntegerField(verbose_name="大专及以上学历人数", blank=True ,default=0)
    company_job_title = models.IntegerField(verbose_name="中级及以上职称人数", blank=True ,default=0)
    company_patents_number = models.IntegerField(verbose_name="企业拥有专利个数", blank=True ,default=0)
    company_product = models.TextField(verbose_name="主要产品/服务", blank=True)
    company_annual_income = models.IntegerField(verbose_name="企业年产值", blank=True ,default=0)
    company_remark = models.TextField(verbose_name="备注", blank=True)

    # def __str__(self):
    #     return self.company_info_id

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
    notification_content = RichTextUploadingField(verbose_name="通知内容")
    notification_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="通知作者", default=1)
    notification_date = models.DateField(auto_now_add=True, verbose_name="通知生成日期")
    notification_auto_revocation = models.DateField(verbose_name="通知自动撤销日期")
    notification_revocation_flag = models.BooleanField(verbose_name="是否已主动撤销", default=False)

    def __str__(self):
        return self.notification_title

    class Meta:
        ordering = ['-notification_date', '-notification_auto_revocation']
        verbose_name_plural = "内置通知表"

#系统黑名单--企业黑名单
class SystemBlackList(models.Model):
    system_black_list = models.ManyToManyField(CompanyInfo, related_name="black_list_for_company", verbose_name="系统黑名单")
    black_list_datetime = models.DateField(auto_now_add=True, verbose_name="加入黑名单的日期")

    class Meta:
        ordering = ['-black_list_datetime', ]
        verbose_name_plural = "企业黑名单"

#系统配置表
class SystemConfig(models.Model):
    system_name = models.CharField(max_length=200, verbose_name="系统名称")
    system_database_name = models.CharField(max_length=200, verbose_name="系统数据库名称")
    system_open_or_close = models.BooleanField(default=True, verbose_name="系统是否开放")
    system_online_time = models.DateField(verbose_name="系统上线日期")

    def __str__(self):
        return "系统名称 : {}".format(self.system_name)

    class Meta:
        verbose_name_plural = "系统配置"