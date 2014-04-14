#coding=utf-8
from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# 静态文件处理
urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_SITE}),
    (r'^theme_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.THEME_SITE}),
    (r'^upload_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
# 非调试模式时的404和500页面
if not settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
        url(r'^505/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
    )

urlpatterns += patterns('views',
    (r'^$','index'),                     # 首页
)
urlpatterns += patterns('',
    (r'^blog/', include('blog.urls')),      # 博客
    (r'^manager/', include('manager.urls')),    # 后台
    (r'^account/', include('account.urls')),    # 用户
    (r'^commons/', include('commons.urls')),      # 常用
    (r'^about/', include('about.urls')),    # 关于我
    (r'^translate/', include('translate.urls')),    # 翻译
    (r'^photo/', include('photo.urls')),    # 图册
)

