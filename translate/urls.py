#coding=utf-8
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# 静态文件处理
urlpatterns = patterns('translate.views',
    (r'^$', 'index'),                                       # 翻译首页
    (r'^add_category/$', 'add_category'),                   # 添加分类
    (r'^del_category/$', 'del_category'),                   # 删除分类
    (r'^edit_category/(?P<id>\d+)/$', 'edit_category'),     # 分类编辑
    (r'^cate_index/(?P<id>\d+)/$', 'cate_index'),           # 分类首页
    (r'^add_translate/(?P<id>\d+)/$', 'add_translate'),                 # 翻译
    (r'^translate/(?P<id>\d+)/$', 'translate'),                 # 内容
    (r'^manager/$', 'manager'),         # 翻译管理
    (r'^manager/manager_list/$', 'manager_list'),           # 翻译管理列表
    (r'^manager/del/$', 'delete'),                          # 翻译管理删除
)