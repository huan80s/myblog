#coding=utf-8
from django import template
register = template.Library()
from blog.models import Category, Blog, Tags
from blog.common import tagsCloud


def sideInfo():
    context = {}
    category = Category.objects.all()      # 所有分类
    blog = Blog.objects.filter(status__gt=0, password__isnull=False)
    newblog = blog.order_by('-add_time')[:15]   # 最新前十条博客
    hotblog = blog.order_by('-hit')[:15]        # 最火前十条博客
    cloud = tagsCloud()                         # 标签云


    context['category'] = category
    context['newblog'] = newblog
    context['hotblog'] = hotblog
    context['cloud'] = cloud

    return context

register.inclusion_tag('common/sideinfo.html')(sideInfo)