from django.db import models

# Create your models here.

#我司售卖产品列表
class MyCompanyProductList(models.Model):
    mproduct_name = models.CharField(max_length=200, verbose_name="产品名称")
    mproducts_makers = models.CharField(max_length=200, verbose_name="产商")
    mproduct_market_price = models.IntegerField(verbose_name="市场价")
    mproduct_internal_price = models.IntegerField(verbose_name="内部价")
    mproduct_in_storage_date = models.DateTimeField(auto_now_add=True, verbose_name="入库时间")
    mproduct_update_time = models.DateTimeField(auto_now=True, verbose_name="产品更新日期")
    mproduct_on_sale = models.BooleanField(verbose_name="是否在售", default=True)

    def __str__(self):
        return self.mproduct_name
    
    class Meta:
        ordering = ['-mproduct_in_storage_date', ]

#企业类型表
class CompanyType(models.Model):
    company_type_name = models.CharField(max_length=50, verbose_name="公司类型")

    def __str__(self):
        return self.company_type_name



#标签表
class CompanyTag(models.Model):
    tag_name = models.CharField(max_length=50, verbose_name="标签名称")
    tag_important_level = models.IntegerField(verbose_name="重要级别", default=3)

    def __str__(self):
        return self.tag_name
    
    class Meta:
        ordering = ['-tag_important_level', ]

#企业信息表
class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=200, verbose_name="公司名称")
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE, related_name="company_type_id", verbose_name="公司类型")
    responsible_person = models.CharField(max_length=50, verbose_name="企业法人/负责人")
    contact_name = models.CharField(max_length=50, verbose_name="企业联系人姓名")
    contact_phone = models.CharField(max_length=11, verbose_name="企业联系人电话")
    contact_email = models.EmailField(verbose_name="企业联系人email")
    contact_QQ = models.CharField(max_length=20, verbose_name="联系人QQ号")
    contact_Ding = models.CharField(max_length=50, verbose_name="企业联系人钉钉号")
    contact_address = models.CharField(max_length=200, verbose_name="企业通讯地址")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="录入系统时间")

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ['-create_time', ]

#企业产品列表
class CompanyProduct(models.Model):
    company_info_id = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, verbose_name="所属企业")
    cproduct_name = models.CharField(max_length=200, verbose_name="产品名称")
    cproducts_type = models.CharField(max_length=200, verbose_name="产品类别")
    cproduct_market_price = models.IntegerField(verbose_name="市场价")
    cproduct_internal_price = models.IntegerField(verbose_name="内部价")
    cproduct_in_storage_date = models.DateTimeField(auto_now_add=True, verbose_name="入库时间")
    cproduct_on_sale = models.BooleanField(verbose_name="是否在售", default=True)

    def __str__(self):
        return self.cproduct_name
    
    class Meta:
        ordering = ['-cproduct_in_storage_date', ]

#企业附加信息表
class CompanyInfoOverHead(models.Model):
    company_info_id = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE, verbose_name="所属企业")
    company_tag = models.ManyToManyField(CompanyTag, related_name="company_tag_for_company", verbose_name="企业标签")
    business_contact_flag = models.BooleanField(verbose_name="是否与我司有业务往来", default=False)
    from_mycompany_product = models.ManyToManyField(MyCompanyProductList, related_name="mycompany_from_product", verbose_name="正在使用的我司产品")
    company_product = models.ManyToManyField(CompanyProduct, related_name="company_for_product", verbose_name="企业产品清单")

    def __str__(self):
        return self.company_info_id


#内置通知表
class InternalCircular(models.Model):
    notification_title = models.CharField(max_length=200, verbose_name="通知标题")
    important_level = models.IntegerField(verbose_name="通知重要级别", default=3)
    notification_content = models.TextField(verbose_name="通知内容")
    notification_author = models.CharField(max_length=50, verbose_name="通知作者")
    notification_date = models.DateField(auto_now_add=True, verbose_name="通知生成日期")
    notification_auto_revocation = models.DateField(verbose_name="通知自动撤销日期")

    def __str__(self):
        return self.notification_title

    class Meta:
        ordering = ['-notification_date', ]
