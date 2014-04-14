#coding=utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('manager.blog_ms.views',
    # 分类管理
    (r'^categroy/$', 'categroy'),                               # 分类管理
    (r'^categroy/delete/$', 'categroy_delete'),                 # 分类删除
    (r'^categroy/update/$', 'categroy_update'),                 # 分类排序批量更新

    # 标签
    (r'^tags/$', 'tags'),                                       # 标签管理
    (r'^get_tags/$', 'get_tags'),                               # 获取标签

    # 文章
    (r'^blog_manage/$', 'blog_manage'),                         # blog管理
    (r'^add_blog/$', 'add_blog'),                               # 写或编辑博客
    (r'^blog_list/$', 'blog_list'),                             # 博客列表(异步加载)
    (r'^del/$', 'delete'),                                      # 删除博客

    # 图片
    (r'^pic/$', 'pic'),                                         # 图片管理
    (r'^add_pic/$', 'picAdd'),                                  # 上传图片
    (r'^del_pic/$', 'picDel'),                                  # 删除图片

    # 签名
    (r'^sign/$', 'sign'),                                       # 签名
)
