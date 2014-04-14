#coding=utf-8
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# 静态文件处理
urlpatterns = patterns('blog.views',
    (r'^$', 'index'),           # 博客首页
    (r'^list/$', 'list'),       # 博客列表
    (r'^article/(?P<id>\d+)/$', 'view'),           # 博客详细
    (r'^search/$', 'search'),       # 搜索
    (r'^category/(?P<id>\d+)/$', 'category'), #分类搜索
    (r'^tag/(?P<id>\d+)/$', 'tag'), #标签搜索
    (r'^pigeonhole/$','pigeonhole'), #归档
)