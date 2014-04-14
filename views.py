#coding=utf-8
import logging, datetime
from django.http import HttpResponse, HttpResponseRedirect
from commons.common import render_template
from blog.models import Category, Tags, Blog, Pic
from manager.models import Carousel


log = logging.getLogger(__name__)

def index(request):
    """首页"""
    try:
        context = {}
        user = request.user

        blog = Blog.objects.filter(status=1).order_by('-add_time')
        newBlog = blog.filter(istop=0)
        topBlog = blog.filter(istop=1).values('id', 'title', 'add_time')
        context['topBlog'] = topBlog
        # 推荐博客

        # 最新博客(10条)
        blog_num = len(newBlog)
        if blog_num > 10:
            newBlog = newBlog[:10]
        blog_list = []
        for obj in newBlog:
            dict = {}
            dict['blog'] = obj
            dict['category'] = obj.category_id
            dict['tags'] = [i for i in obj.tags.split('|') if i]
            picUrl = '/upload_media/blog/love/default.jpg/'       # 缩略图
            if obj.pic:
                pic = Pic.objects.filter(id=obj.pic)
                if pic:
                    pic = Pic.objects.get(pk=obj.pic)
                    if pic.image:
                        picUrl = '/upload_media/%s' %pic.image

            dict['picUrl'] = picUrl
            blog_list.append(dict)
        context['blog_list'] = blog_list
        # 轮播展示
        c = Carousel.objects.all()
        carousels = Carousel.objects.filter(status=1).order_by('sequence')[:4]

        context['carousels'] = carousels
    except Exception, e:
        log.error('index:%s' % e)
    return render_template(request, 'index.html', context)
    

def demo(request, demo=None):
    """练兵场"""
    context = {}
    return render_template(request, 'demo/%s' % demo, context)
