import xadmin
from xadmin import views
from .models import UserLevel, UserPermissionProfile

class UserLevelAdmin(object):
    list_display = ['level_name', 'level_describe']

xadmin.site.register(UserLevel, UserLevelAdmin)

class UserPermissionProfileAdmin(object):
    list_display = ['user', 'user_level', 'user_phone', 'user_agent', 'user_ip']

xadmin.site.register(UserPermissionProfile, UserPermissionProfileAdmin)
