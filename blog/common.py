#coding=utf-8
from blog.models import Blog, Tags
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
import random
import logging
log = logging.getLogger(__name__)

def get_neighbour(id):
    """
    功能说明：获取上一篇、下一篇
  id:对应博客或爬取id
  type:方式，0表示博客，1表示爬取      
    """

    blog_list = Blog.objects.values_list('id', flat=True).order_by('id')
    dic = {}
    blog_list = list(blog_list)
    if blog_list:
        id_index = blog_list.index(id)  # 当前id的索引
        pre = next = 0

        if len(blog_list)>1:
            if id_index != 0 and id_index !=len(blog_list)-1:      # 如果不是第一篇或最后一篇
                pre = blog_list[id_index-1]
                next = blog_list[id_index+1]
            else:
                if id_index == 0:       # 第一篇
                    next = blog_list[id_index+1]
                if id_index == len(blog_list)-1:    # 最后一篇
                    pre = blog_list[id_index-1]
        elif len(blog_list) == 1:
            pre, next = 0, 0
        dic = {'pre': pre, 'next': next}

    return dic

def tagsCloud():
    """标签云"""
    
    tags = Tags.objects.all()
    tagscloud = []
    for obj in tags:
        size = random.randint(12,50)        # 随机字体
        R = random.randint(0,254)
        G = random.randint(0,254)
        B = random.randint(0,254)       # 没有白色
        RGB = 'rgb(%d,%d,%d)' %(R,G,B)      # 随机颜色
        dic = {}
        dic['name'] = obj.name
        dic['id'] = obj.id
        dic['size'] = size
        dic['rgb'] = RGB
        tagscloud.append(dic)
    return tagscloud




                
    
