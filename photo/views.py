#coding=utf-8
import logging, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from commons.common import render_template, ExecuteSql
from photo.models import Photo, PhotoCategory
from photo.form import PhotoCategoryForm
from blog.models import Pic
import simplejson as json
from markdown import markdown
from django.views.decorators.csrf import csrf_exempt
from commons.selfpage import get_page_result  # 获取分页
log = logging.getLogger(__name__)

def index(request):
    """
    ===============================================================================
    function：    图册首页
    developer:    BeginMan
    add-time      2014/1/8
    ===============================================================================
    """
    context = {}
    try:
        photo_cates = PhotoCategory.objects.order_by('sequence')
        context['photo_cates'] = photo_cates
    except Exception, e:
        log.error('photo>index:%s' %e)
        return HttpResponse(e)
    return render_template(request, 'photo/index.html', context)

def create(request, id=None):
    """
    ===============================================================================
    function：    相册分类创建
    developer:    BeginMan
    add-time      2014/1/17
    ===============================================================================
    """
    context = {}
    try:
        p_cate = None       # 分类实例
        if id and id != '0':
            p_cate = PhotoCategory.objects.get(id=id)
        if request.method == 'POST':
            form = PhotoCategoryForm(request.POST, instance=p_cate)
            if form.is_valid():
                f = form.save()
                return HttpResponse(u'创建成功！')
        else:
            form = PhotoCategoryForm(instance=p_cate)
        context['form'] = form
    except Exception, e:
        log.error('photo>index:%s' % e)
        return HttpResponse(e)
    return render_template(request, 'photo/cate_create.html', context)

def cate_del(request):
    """
    ===============================================================================
    function：    相册分类删除
    developer:    BeginMan
    add-time      2014/1/18
    ===============================================================================
    """
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            Photo.objects.filter(category__id=id).delete()
            PhotoCategory.objects.filter(pk=id).delete()
            return HttpResponse('ok')
    except Exception, e:
        log.error(e)
        return HttpResponse(e)


def photo_upload(request):
    """
    ===============================================================================
    function：    图片上传首页
    developer:    BeginMan
    add-time      2014/1/18
    ===============================================================================
    """
    context = {}
    try:
        cates = PhotoCategory.objects.order_by('sequence')
        context['cates'] = cates
        if request.method == 'POST':
            pic_id = request.POST.get('pic_id')
            c_id = request.POST.get('c_id')
            pic_id_list = [i for i in pic_id.split(';') if i]
            if pic_id_list:
                for obj in pic_id_list:
                    Photo.objects.create(category_id=c_id, image=obj)
            return HttpResponseRedirect('/photo/list/')
    except Exception, e:
        log.error(e)
        return HttpResponse(e)
    return render_template(request, 'photo/photo_upload.html', context)


@csrf_exempt
def upload(request):
    """
    ===============================================================================
    function：    图片上传处理
    developer:    BeginMan
    add-time      2014/1/18
    ===============================================================================
    """
    try:
        if request.method == 'POST':
            print request.POST
            type = request.POST.get('type', 3)      # 表示相册
            img = request.FILES['photo']
            pic = Pic(type=type, ori_image=img, image=img)
            pic.save(180)
            return HttpResponse('%s:%s' % (pic.id, pic.image))    # 返回上传图片的id和路径
    except Exception, e:
        log.error(e)
        return HttpResponse(e)

def del_pic(request):
    """
    ===============================================================================
    function：    删除图片
    developer:    BeginMan
    add-time      2014/1/18
    ===============================================================================
    """
    if request.method == "POST":
        id = request.POST.get('pic_id')
        Pic.objects.filter(id=id).delete()
        return HttpResponse('ok')

def list(request):
    """
    ===============================================================================
    function：    相册图片列表
    developer:    BeginMan
    add-time      2014/1/18
    ===============================================================================
    """
    context = {}
    try:
        pass
    except Exception, e:
        log.error(e)
        return HttpResponse(e)
    return render_template(request, '/photo/list/', context)



