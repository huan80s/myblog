#coding=utf-8
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# 静态文件处理
urlpatterns = patterns('photo.views',
    (r'^$', 'index'),           # 相册首页
    (r'^create/(?P<id>\d+)/$', 'create'),           # 相册类型创建
    (r'^cate_del/$', 'cate_del'),           # 相册删除
    (r'^photo_upload/$', 'photo_upload'),           # 图片上传界面
    (r'^upload/$', 'upload'),               # 图片上传处理
    (r'^del_pic/$', 'del_pic'),             # 删除图片
    ('^list/$', 'list'),                    # 相册图片列表
)