import xadmin
from xadmin import views
from .models import UserLevel, UserPermissionProfile

@xadmin.sites.register(UserLevel)
class UserLevelAdmin(object):
    list_display = ['level_name', 'level_describe']

@xadmin.sites.register(UserPermissionProfile)
class UserPermissionProfileAdmin(object):
     list_display = ['user', 'user_level', 'user_phone', 'user_agent', 'user_ip']

