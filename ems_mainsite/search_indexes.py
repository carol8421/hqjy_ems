#coding=utf-8
from haystack import indexes
from .models import CompanyInfo, CompanyTag, CompanyType, CompanySecondType

#指定对于某个类的某些数据建立索引
class CompanyInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    contact_phone = indexes.CharField(model_attr='contact_phone')
    contact_name = indexes.CharField(model_attr='contact_name')
    responsible_person = indexes.CharField(model_attr='responsible_person')

 
    def get_model(self):
        return CompanyInfo
 
    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class CompanyTagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return CompanyTag
 
    def index_queryset(self, using=None):
        return self.get_model().objects.all()