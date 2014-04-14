#coding=utf-8
import logging, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from commons.common import render_template, ExecuteSql
from blog.models import Category, Tags, Blog, Pic, Sign
import simplejson as json
from markdown import markdown
from django.views.decorators.csrf import csrf_exempt
from blog.common import tagsCloud, get_neighbour
from commons.selfpage import get_page_result  # 获取分页
log = logging.getLogger(__name__)

def index(request):
    """
    ===============================================================================
    function：    博客列表
    developer:    BeginMan
    add-time      2014/1/3
    ===============================================================================
    """
    context = {}
    try:
        # 推荐博客
        topBlog = Blog.objects.filter(status=1, istop=1).order_by('-add_time').values('id', 'title', 'add_time')
        context['topBlog'] = topBlog

    except Exception, e:
        log.error('blog>index:%s' %e)
        return HttpResponse(e)
    return render_template(request, 'blog/index.html', context)


def list(request):
    """
    ===============================================================================
    function：    博客列表
    developer:    BeginMan
    add-time      2014/1/8
    ===============================================================================
    """
    context = {}
    if request.method == "POST":
        blog = Blog.objects.filter(status=1, istop=0).order_by('-add_time')
        page = request.POST.get('page')
        # 最新博客(12个一分页)

        new_blogs = get_page_result(page, blog, 12)

        blog_list = []
        for obj in new_blogs.object_list:
            dict = {}
            dict['blog'] = obj
            dict['category'] = obj.category_id
            dict['tags'] = [i for i in obj.tags.split('|') if i]
            blog_list.append(dict)
        context['blog_list'] = blog_list
        context['new_blogs'] = new_blogs
    return render_template(request, 'blog/list.html', context)



def view(request, id=None):
    """
    ===============================================================================
    function：    博客详细
    developer:    BeginMan
    add-time      2014/1/3
    ===============================================================================
    """
    context = {}
    try:
        if id:
            id = int(id)
            blog = get_object_or_404(Blog, pk=id)
            # 上一篇、下一篇
            for obj in get_neighbour(id):
                if get_neighbour(id)[obj]:
                    context['title_%s' %obj] = Blog.objects.get(pk=int(get_neighbour(id)[obj])).title
                context[obj] = get_neighbour(id)[obj]
            # 博客签名
            sign = Sign.objects.filter(is_active=1)
            if sign:
                sign = sign[0]
            context['sign'] = sign
            context['blog'] = blog
    except Exception, e:
        log.error('blog>view:%s' %e)
        return HttpResponse(e)
    return render_template(request, 'blog/views.html', context)


def search(request):
    """
    ===============================================================================
    function：    博客搜索
    developer:    BeginMan
    add-time      2014/1/7
    ===============================================================================
    """
    context = {}
    try:
        if request.method == 'GET':
            search_text = request.GET.get('search')
            page = request.GET.get('page', 1)
            sql = u"""select id, title from blog_article where title like '%%%%%s%%%%'""" % search_text
            fetchall = ExecuteSql(sql)

            result = get_page_result(page, fetchall, 20)
            search_result = []
            for obj in result.object_list:
                dic = {}
                dic['id'] = obj[0]
                dic['title'] = obj[1]
                search_result.append(dic)
            context['search_result'] = search_result
            context['result'] = result
            context['search_text'] = search_text

    except Exception, e:
        log.error('blog/search:%s' %e)
        return HttpResponse('err')
    return render_template(request, 'blog/search.html', context)


def category(request, id=None):
    """
    ===============================================================================
    function：    博客搜索
    developer:    BeginMan
    add-time      2014/1/7
    ===============================================================================
    """
    context = {}
    if request.method == "GET":
        if not id:
            return HttpResponseRedirect('/404/')
        category = Category.objects.get(pk=id)
        blogs = Blog.objects.filter(category_id__id=id, status=1).order_by('-add_time')
        page = request.GET.get('page', None)
        result = get_page_result(page, blogs, 20)
        context['result'] = result
        context['category_title'] = category.title
        context['num'] = len(blogs)

        blog_list = []
        for obj in result.object_list:
            dict = {}
            dict['blog'] = obj
            dict['category'] = obj.category_id
            dict['tags'] = [i for i in obj.tags.split('|') if i]
            blog_list.append(dict)
        context['blog_list'] = blog_list
    return render_template(request, 'blog/category.html', context)

def tag(request, id=None):
    """
    ===============================================================================
    function：    博客搜索
    developer:    BeginMan
    add-time      2014/1/7
    ===============================================================================
    """
    context = {}
    if request.method == "GET":
        if not id:
            return HttpResponseRedirect('/404/')
        tag = Tags.objects.get(pk=id)
        tag_name = tag.name
        b_list = []
        blogList = Blog.objects.filter(status=1).order_by('-add_time')
        for obj in blogList.extra(where=['length(tags)>0']):        # 获取标签不为空的
            if tag_name in [i for i in obj.tags.split('|') if i]:        # 如果该标签在其中则填充
                b_list.append(obj)

        page = request.GET.get('page', None)
        result = get_page_result(page, b_list, 20)
        context['result'] = result
        context['tag_name'] = tag_name
        context['num'] = len(b_list)

        blog_list = []
        for obj in result.object_list:
            dict = {}
            dict['blog'] = obj
            dict['category'] = obj.category_id
            dict['tags'] = [i for i in obj.tags.split('|') if i]
            blog_list.append(dict)
        context['blog_list'] = blog_list
    return render_template(request, 'blog/tag.html', context)


def pigeonhole(request):
    """
    ===============================================================================
    function：    文章归档
    developer:    BeginMan
    add-time      2014/1/10
    ===============================================================================
    """
    context = {}
    try:
        sql = u"""
        SELECT id,title,YEAR(add_time) as year ,MONTH(add_time) as month
        FROM blog_article WHERE `status` =1 ORDER BY year DESC,month DESC
        """
        fetchall = ExecuteSql(sql)
        blogs = []
        for obj in fetchall:
            dic = {}
            dic['id'] = obj[0]
            dic['title'] = obj[1]
            dic['year'] = obj[2]
            dic['month'] = obj[3]
            blogs.append(dic)
        context['blogs'] = blogs
    except Exception, e:
        log.error('blog>index:%s' %e)
        return HttpResponse(e)
    return render_template(request, 'blog/pigeonhole.html', context)












