#coding=utf-8
from django.conf.urls.defaults import *

#
urlpatterns = patterns('account.user',
    (r'^login/$', 'user_login'),           # 登录
    (r'^logout/$', 'logut'),   # 退出
    (r'^register/$', 'register'),  # 注册
    (r'^register_ok/(?P<type>\d+)/$', 'register_ok'),  # 注册成功

    (r'^user/(?P<id>\d+)/$', 'index'),          # 用户首页
    (r'^user/update_nickname/$', 'update_nickname'), # 修改昵称
    (r'^user/update_pwd/$', 'update_pwd'), # 修改密码
    (r'^user/update_pro/$', 'update_pro'), # 修改头像
)

