#coding=utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('manager.views',
    (r'^$','index'),                            # 博客首页
)

# blog 管理
urlpatterns += patterns('',
    (r'^blog/',include('manager.blog_ms.urls')),    # blog管理 
    (r'^system/',include('manager.system.urls')),           # 系统管理                       
)