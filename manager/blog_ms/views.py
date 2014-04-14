#coding=utf-8
import logging, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from commons.common import render_template, strip_tags, commonForm
from blog.models import Category, Tags, Blog, Pic, Sign
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from blog.common import tagsCloud
from manager.blog_ms.form import BlogForm
from manager.validation import DivErrorList
from django.db.models import F, Sum
from django.core.paginator import  EmptyPage, InvalidPage
from commons.selfpage import MyPaginator
from manager.blog_ms.form import SignForm
log = logging.getLogger(__name__)
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def categroy(request):
    """
    ===============================================================================
    function：            分类管理
    developer:    BeginMan
    add-time      2013/12/28 
    ===============================================================================
    """
    context = {}
    # 分类展示
    all = Category.objects.all() 
    p_categroes = Category.objects.filter(parent_id=0).order_by('sequence', '-id')       # 所有父分类
    categroy_list = []
    for obj in p_categroes:
        dict = {}
        p_id = obj.id
        dict['pc'] = obj
        dict['cc'] = all.filter(parent_id=p_id).order_by('sequence','-id')
        categroy_list.append(dict)
        
    if request.method == 'POST':
        try:
            type = request.POST.get('type')     # 表示方式 当0表示创建，当编辑是type值是编辑的id
            p_id = request.POST.get('p_id', 0)
            title = request.POST.get('title')
            des = request.POST.get('des', '')
            sequence = request.POST.get('sequence', 100)
            if type == '0':     # 创建
            
                if not sequence:
                    sequence = 100
                
                if not p_id:
                    if title in [i.title for i in p_categroes]:            # 如果父类存在相同的则提醒
                        return HttpResponse('0')
                else:                                   # 如果父类下的子类存在相同的则提醒
                    if title in [i.title for i in Category.objects.filter(parent_id=p_id)]:
                        return HttpResponse('0')   
                # create
                if p_id:
                    
                    Category.objects.create(parent_id=p_id, title=title, des=des, sequence=sequence)
                else:
                    Category.objects.create(title=title, des=des, sequence=sequence)
            else:           # 编辑
                category = Category.objects.filter(id=type).update(title=title, des=des, sequence=sequence)
            return HttpResponse(1)
        except Exception,e:
            log.error('categroy:%s' % e)
            return HttpResponse(e)
    context['p_categroes'] = p_categroes
    context['categroy_list'] = categroy_list
    return render_template(request, 'manager/blog/categroy.html', context)



@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def categroy_delete(request):
    """
    ===============================================================================
    function：            分类删除
    developer:    BeginMan
    add-time      2013/12/28 
    ===============================================================================
    """
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            category = Category.objects.get(pk=id)
            if category.parent_id:          # 如果该分类存在子分类 则删除自身
                Category.objects.filter(id=id).delete()
            else:                           # 否则删除全部
                Category.objects.filter(parent_id=id).delete()
                Category.objects.filter(id=id).delete()
            return HttpResponse('ok')
    except Exception, e:
        log.error('categroy_delete:%s' % e)
        return HttpResponse(e)



@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def categroy_update(request):
    """
    ===============================================================================
    function：            分类排序批量更新
    developer:    BeginMan
    add-time      2013/12/28 
    ===============================================================================
    """
    try:
        if request.method == 'POST':
            json_sequence = json.loads(request.POST.get('data'))
            for obj in json_sequence:
                Category.objects.filter(id=obj['id']).update(sequence=obj['sequence'])
                
            return HttpResponse('ok')
    except Exception,e:
        log.error('categroy_delete:%s' % e)
        return HttpResponse(e)




@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def tags(request):
    """
    ===============================================================================
    function：            标签管理
    developer:    BeginMan
    add-time      2013/12/28 
    ===============================================================================
    """
    context = {}
    try:
        tag_list = Tags.objects.all().order_by('-add_time')
        cloud = tagsCloud()
        
         # 操作
        if request.method == 'POST':
          name = request.POST.get('name')
          type = request.POST.get('type')
          id = request.POST.get('id',0)
          
          if Tags.objects.filter(name=name).exists():     # 如果存在该标签在返回提示
              return HttpResponse('0')
          if type == '0':               # create
              Tags.objects.create(name=name)
              
          elif type == '1':   # 删除
              Tags.objects.filter(pk=id).delete()
          else:                 # edit
              Tags.objects.filter(pk=id).update(name=name)
          return HttpResponse('1')
          
    except Exception,e:
        log.error('tags:%s' % e)
        return HttpResponse('err')
    context['tag_list'] = tag_list
    context['cloud'] = cloud
    return render_template(request, 'manager/blog/tags.html', context)



@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def get_tags(request):
    """
    ===============================================================================
    function：            获取标签
    developer:    BeginMan
    add-time      2013/12/28 
    ===============================================================================
    """
    context = {}
    tag_list = Tags.objects.all().order_by('-add_time')
    context['tag_list'] = tag_list
    return render_template(request, 'manager/blog/get_tags.html', context)



@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def add_blog(request):
    """
    ===============================================================================
    function：            发表博客
    developer:    BeginMan
    add-time      2013/12/28 
    ===============================================================================
    """
    context = {}
    user = request.user
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST, error_class=DivErrorList)
            if form.is_valid():
                formData = form.cleaned_data
                category_id = formData.get('category_id')   # Category实例
                tags = formData.get('tags', None)
                title = formData.get('title')
                summary = formData.get('summary', None)
                content = formData.get('content')
                status = formData.get('status', 1)
                istop = formData.get('istop', 0)
                cancomment = formData.get('cancomment', 1)
                password = formData.get('password', None)
                my_pic = request.POST.get('my_pic', None)       # 上传的图片id
                edit_or_creat = request.POST.get('edit_or_creat', None)     # 编辑还是创建

                if not summary:
                    count = len(content)                        # 摘要不得超过300字
                    cut_len = int(count*0.5)                    # 取50%
                    if count > 300:
                        cut_len = 300

                    summ_content = '%s....' % content[:cut_len]
                    summary = strip_tags(summ_content)       # 将markdown格式转换纯文本
                if not edit_or_creat:
                    # 创建blog
                    Blog.objects.create(category_id=category_id, tags=tags, summary=summary, title=title, content=content, status=status, istop=istop, cancomment=cancomment, password=password, pic=my_pic)
                else:
                    # 编辑博客
                    b_id = int(edit_or_creat)
                    Blog.objects.filter(id=b_id).update(category_id=category_id, tags=tags, summary=summary, title=title, content=content, status=status, istop=istop, cancomment=cancomment, password=password, pic=my_pic)

                # 创建标签
                tags_list = [i for i in tags.split('|') if i]
                all_tags = Tags.objects.all()
                if tags_list:
                    for obj in tags_list:
                        if obj not in all_tags:     # 标签唯一
                            Tags.objects.create(name=obj)
                # 更新分类
                category_id.count +=1
                category_id.save()
                return HttpResponseRedirect('/manager/blog/blog_manage/')        # 跳到管理页面
        else:
            id = request.GET.get('id', None)
            if id:      # 编辑状况
                blog = get_object_or_404(Blog, pk=int(id))
                form = BlogForm(auto_id='id_for_%s', label_suffix=u'：', instance=blog)
            else:
                form = BlogForm(auto_id='id_for_%s', label_suffix=u'：')
        tags_list = Tags.objects.order_by('-add_time')
        context['tags'] = tags_list
        context['form'] = form


    except Exception, e:
        log.error('add_blog:%s' % e)
        return HttpResponse(e)
    return render_template(request, 'manager/blog/add_blog.html', context)



@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
@csrf_exempt
def picAdd(request):
    """
    ===============================================================================
    function：    图片上传(图片没有关联对象则自动删除,写个脚本处理下。)
    developer:    BeginMan
    add-time      2013/12/31
    ===============================================================================
    """
    if request.method == 'POST':
        try:
            type = request.POST.get('type', 1)
            img = request.FILES['blogPic']
            pic = Pic(type=type, ori_image=img, image=img)
            pic.save(200)
            return HttpResponse('%s:%s' % (pic.id, pic.image))    # 返回上传图片的id和路径
        except Exception, e:
            log.error('picAdd:%s' % e)
            return HttpResponse('err')



@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def picDel(request):
    """
    ===============================================================================
    function：    图片删除
    developer:    BeginMan
    add-time      2013/12/31
    ===============================================================================
    """
    if request.method == 'POST':
        try:
            pic_id = request.POST.get('pic_id')
            Pic.objects.filter(id=pic_id).delete()
            return HttpResponse('ok')
        except Exception, e:
            log.error('picDel:%s' % e)
            return HttpResponse('err')



@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def blog_manage(request):
    """
    ===============================================================================
    function：    博客管理
    developer:    BeginMan
    add-time      2014/1/2
    ===============================================================================
    """
    context = {}
    try:
        tag = Tags.objects.order_by('-add_time')
        category_num = tag.aggregate(Sum('count'))
        category = Category.objects.order_by('sequence')
        p_cates = category.filter(parent_id=0)
        c_list = []
        for obj in p_cates:
            dic = {}
            dic['parent'] = obj
            dic['child'] = category.filter(parent_id=obj.id)
            c_list.append(dic)

        context['c_list'] = c_list
        context['category_num'] = category_num
        context['tag'] = tag
        return render_template(request, 'manager/blog/blog.html', context)
    except Exception ,e:
        log.error('blogManager:%s' %e)
        return HttpResponse('err')

@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def blog_list(request):
    """
    ===============================================================================
    function：    博客列表
    developer:    BeginMan
    add-time      2014/1/2
    ===============================================================================
    """
    try:
        context = {}
        if request.method == 'POST':
            categoryId = request.POST.get('categoryId')             # 分类
            cmms = request.POST.get('cmms')                         # 是否允许评论，2全部；1允许；0不允许
            date1 = request.POST.get('date1')                       # 日期1
            date2 = request.POST.get('date2')                       # 日期2
            is_top = request.POST.get('is_top')                  # 是否置顶 2全部 1置顶；0不置顶
            pwds = request.POST.get('pwds')                         # 密码，0全部；1正常；2加密
            status = request.POST.get('status')                     # 状态 2全部；1分布；0草稿
            tag = request.POST.get('tag')                           # 获取标签名称
            title = request.POST.get('title')                       # 搜索的标题


            blogList = Blog.objects.filter(status__lt=2).order_by('-add_time')

            if categoryId != '0':
                if Category.objects.get(pk=categoryId).parent_id == 0:     # 父分类
                    c_id_list = list(Category.objects.filter(parent_id=categoryId).values_list('id', flat=True))
                    c_id_list.append(int(categoryId))
                    blogList = blogList.filter(category_id__id__in=c_id_list, status__lt=2)
                else:
                    blogList = blogList.filter(category_id__id__in=categoryId, status__lt=2)

            if cmms != '2':
                blogList = blogList.filter(cancomment=cmms)
            if is_top != '2':
                blogList = blogList.filter(istop=is_top)
            if pwds == '2':
                blogList = blogList.filter(password__isnull=True)
            if pwds == '1':
                blogList = blogList.filter(password__isnull=False)
            if status != '2':
                blogList = blogList.filter(status=status)
            if title:
                blogList = blogList.filter(title__icontains=title)      # icontains 不区分大小写
            # 标签处理可能有些麻烦
            if tag != u'全部':
                b_list = []
                for obj in blogList.extra(where=['length(tags)>0']):        # 获取标签不为空的
                    if tag in [i for i in obj.tags.split('|') if i]:        # 如果该标签在其中则填充
                        b_list.append(obj)
                blogList = b_list

            # 日期
            start = datetime.date(2013, 1, 1)       # 起始时间
            if date1 and date2:
                split_date1 = date1.split('-')
                split_date2 = date2.split('-')
                d_date1 = datetime.date(int(split_date1[0]), int(split_date1[1]), int(split_date1[2]))
                d_date2 = datetime.date(int(split_date2[0]), int(split_date2[1]), int(split_date2[2]))
                blogList = blogList.filter(add_time__range=(d_date1, d_date2))
            else:
                if date1:
                    split_date1 = date1.split('-')
                    d_date1 = datetime.date(int(split_date1[0]), int(split_date1[1]), int(split_date1[2]))
                    blogList = blogList.filter(add_time__range=(start, d_date1))

                if date2:
                    split_date2 = date2.split('-')
                    d_date2 = datetime.date(int(split_date2[0]), int(split_date2[1]), int(split_date2[2]))
                    blogList = blogList.filter(add_time__range=(start, d_date2))

            try:
                page = request.POST.get('page', '1')
            except ValueError:      # Make sure page request is an int. If not, deliver first page.
                page = 1
            paginator = MyPaginator(blogList, 15)     # 15个一分页

            try:
                blog = paginator.page(page)
            except (EmptyPage, InvalidPage):    # # If page request (9999) is out of range, deliver last page of results
                blog = paginator.page(paginator.num_pages)
            context['blog'] = blog
            return render_template(request, 'manager/blog/blog_list.html', context)

    except Exception, e:
        log.error('blog_list:%s' %e)
        return HttpResponse('err')


@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def delete(request):
    """
    ===============================================================================
    function：    博客删除
    developer:    BeginMan
    add-time      2014/1/3
    ===============================================================================
    """
    try:
        if request.method == 'POST':
            id_str = request.POST.get('id_str', None)
            if id_str:
                id_list = [int(i) for i in id_str.split(',') if i]
                Blog.objects.filter(id__in=id_list).update(status=2)        # 虚删除
                return HttpResponse('ok')
    except Exception,e:
        log.error('delete:%s' %e)
        return HttpResponse('err')

@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def sign(request):
    """
    ===============================================================================
    function：    博客签名(创建和编辑)
    developer:    BeginMan
    add-time      2014/1/4
    ===============================================================================
    """
    context = {}
    try:
        # 调用自定义表单操作方法
        formCustom = commonForm(request, Sign, SignForm)
        if formCustom:
            for obj in formCustom:
                context[obj] = formCustom[obj]
        else:
            raise ValueError(u'表单自定义数据出错')
        signs = Sign.objects.order_by('-add_time')[:10]  # 显示已创建的签名最多10个
        context['signs'] = signs
    except Exception, e:
        log.error('blog_ms>sign:%s' %e)
        return HttpResponse('err')
    return render_template(request, 'manager/blog/sign.html', context)









    
    
    
    
    