#coding=utf-8
import logging, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from commons.common import render_template, ExecuteSql, strip_tags
from translate.models import TransCategory, Translate
from translate.form import TransCategoryForm, TransForm
import simplejson as json
from markdown import markdown
from django.views.decorators.csrf import csrf_exempt
from blog.common import get_neighbour
from commons.selfpage import get_page_result  # 获取分页
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
log = logging.getLogger(__name__)

def index(request):
    """
    ===============================================================================
    function：    翻译首页
    developer:    BeginMan
    add-time      2014/1/8
    ===============================================================================
    """
    context = {}
    try:
        t_category = TransCategory.objects.filter(parent_id=0, status=1).order_by('sequence', '-add_time')
        context['t_category'] = t_category
    except Exception, e:
        log.error('translatate/index:%s' %e)
        return HttpResponse(e)
    return render_template(request, 'translate/index.html', context)

def add_category(request):
    """
    ===============================================================================
    function：    创建分类
    developer:    BeginMan
    add-time      2014/1/13
    ===============================================================================
    """
    try:
        if request.method == 'POST':
            title = request.POST.get('title', None)
            summary = request.POST.get('summary', None)
            sequence = request.POST.get('sequence', 1)
            id = request.POST.get('id', None)

            if title:
                title = title.strip()
                sequence = 1
                if sequence:
                    sequence = int(sequence)
                if TransCategory.objects.filter(title=title).exists():
                    return HttpResponse('2')
                else:
                    trans = TransCategory.objects.create(title=title, sequence=sequence, summary=summary)
                    if id:
                        trans.parent_id = int(id)
                        trans.save()
                    return HttpResponse('1')

    except Exception, e:
        log.error('translatate/add:%s' %e)
        return HttpResponse(e)

def del_category(request):
    """
    ===============================================================================
    function：    删除分类
    developer:    BeginMan
    add-time      2014/1/13
    ===============================================================================
    """
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            cate = TransCategory.objects.get(pk=id)
            if cate.parent_id == 0:     # 一级分类
                chlid_categories = TransCategory.objects.filter(parent_id=id)
                chlid_categories.filter(parent_id=id).update(status=2)
                Translate.objects.filter(category__in=chlid_categories).update(status=2)
            else:
                cate.status = 2
                cate.save()
                Translate.objects.filter(category=cate).update(status=2)
            return HttpResponse('ok')

    except Exception, e:
        log.error('translatate/del:%s' % e)
        return HttpResponse(e)

def cate_index(request, id=None):
    """
    ===============================================================================
    function：    专题主页
    developer:    BeginMan
    add-time      2014/1/13
    ===============================================================================
    """
    context = {}
    from django.db.models import Sum
    try:
        if id:
            category = TransCategory.objects.get(pk=id)
            sub_categories = TransCategory.objects.filter(parent_id=id, status=1)     # 属下分类
            translates = Translate.objects.filter(category=category, status=1)        # 直属翻译
            all_trans = sub_categories.aggregate(Sum('count'))
            if all_trans.values()[0]:
                all_trans = all_trans.values()[0]+len(translates)   # 该分类下所有翻译数目
            else:
                all_trans = len(translates)
            context['category'] = category
            context['sub_categories'] = sub_categories
            context['translates'] = translates
            context['all_trans'] = all_trans

        else:
            return HttpResponseRedirect('/404/')
    except Exception, e:
        log.error('translate/cate_index:%s' % e)
        return HttpResponse(e)
    return render_template(request, 'translate/cate_index.html', context)


def edit_category(request, id=None):
    """
    ===============================================================================
    function：    编辑分类
    developer:    BeginMan
    add-time      2014/1/13
    ===============================================================================
    """
    context = {}
    try:
        if id:
            context['id'] = id
            cate = TransCategory.objects.get(pk=id)
        else:
            return HttpResponseRedirect('/404/')

        if request.method == 'POST':
            form = TransCategoryForm(request.POST, instance=cate)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/translate/cate_index/%s/' %id)
        else:
            form = TransCategoryForm(instance=cate)

        context['form'] = form
    except Exception, e:
        log.error('translate/edit_category:%s' % e)
        return HttpResponse(e)
    return render_template(request, 'translate/edit_category.html', context)

def add_translate(request, id=None):
    """
    ===============================================================================
    function：    编撰翻译
    developer:    BeginMan
    add-time      2014/1/13
    ===============================================================================
    """
    context = {}
    try:
        trans = None
        url = request.get_full_path()
        if id and id != '0':
            trans = Translate.objects.get(pk=id)

        if request.method == "POST":
            form = TransForm(request.POST, instance=trans)
            if form.is_valid():
                temp = form.save(commit=False)
                temp.user = request.user
                content = form.cleaned_data['content']
                count = len(content)                        # 摘要不得超过300字
                cut_len = int(count*0.3)                    # 取50%
                if count > 200:
                    cut_len = 200

                summ_content = '%s....' %content[:cut_len]
                summary = strip_tags(summ_content)       # 将markdown格式转换纯文本
                temp.summary = summary
                form.save()
                return HttpResponseRedirect('/translate/')
        else:
            cate_id = request.GET.get('cate', None)
            form = TransForm(instance=trans)
            context['cate_id'] = cate_id

        context['url'] = url
        context['form'] = form

    except Exception, e:
        log.error('translate/add_translate:%s' % e)
        return HttpResponse(e)
    return render_template(request, 'translate/add_translate.html', context)


def translate(request, id=None):
    """
    ===============================================================================
    function：    翻译详细页
    developer:    BeginMan
    add-time      2014/1/13
    ===============================================================================
    """
    context = {}
    try:
        if id:
            translate = Translate.objects.get(pk=id)
            context['translate'] = translate
        else:
            return HttpResponseRedirect('/404/')
    except Exception, e:
        log.error('translate/translate:%s' % e)
        return HttpResponse(e)
    return render_template(request, 'translate/translate.html', context)

def manager(request):
    """
    ===============================================================================
    function：    翻译管理
    developer:    BeginMan
    add-time      2014/1/14
    ===============================================================================
    """
    context = {}
    try:
        category = TransCategory.objects.filter(status=1).order_by('sequence')
        p_cates = category.filter(parent_id=0)
        c_list = []
        for obj in p_cates:
            dic = {}
            dic['parent'] = obj
            dic['child'] = category.filter(parent_id=obj.id)
            c_list.append(dic)

        context['c_list'] = c_list
    except Exception, e:
        log.error('translate/manager:%s' % e)
        return HttpResponse(e)
    return render_template(request, 'translate/manager.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def manager_list(request):
    """
    ===============================================================================
    function：    博客列表
    developer:    BeginMan
    add-time      2014/1/14
    ===============================================================================
    """
    try:
        context = {}
        if request.method == 'POST':
            categoryId = request.POST.get('categoryId')             # 分类
            date1 = request.POST.get('date1')                       # 日期1
            date2 = request.POST.get('date2')                       # 日期2
            is_top = request.POST.get('is_top')                     # 是否置顶 2全部 1置顶；0不置顶
            status = request.POST.get('status')                     # 状态 2全部；1分布；0草稿
            title = request.POST.get('title')                       # 搜索的标题


            transList = Translate.objects.filter(status__lt=2).order_by('-add_time')
            if categoryId != '0':
                if TransCategory.objects.get(pk=categoryId).parent_id == 0:     # 父分类
                    c_id_list = list(TransCategory.objects.filter(parent_id=categoryId).values_list('id', flat=True))
                    c_id_list.append(int(categoryId))
                    transList = Translate.objects.filter(category__id__in=c_id_list, status__lt=2)
                else:
                    transList = Translate.objects.filter(category__id=categoryId, status__lt=2)

            if is_top != '2':
                transList = transList.filter(istop=is_top)

            if status != '2':
                transList = transList.filter(status=status)
            if title:
                transList = transList.filter(title__icontains=title)      # icontains 不区分大小写


            # 日期
            start = datetime.date(2013, 1, 1)       # 起始时间
            if date1 and date2:
                split_date1 = date1.split('-')
                split_date2 = date2.split('-')
                d_date1 = datetime.date(int(split_date1[0]), int(split_date1[1]), int(split_date1[2]))
                d_date2 = datetime.date(int(split_date2[0]), int(split_date2[1]), int(split_date2[2]))
                transList = transList.filter(add_time__range=(d_date1, d_date2))
            else:
                if date1:
                    split_date1 = date1.split('-')
                    d_date1 = datetime.date(int(split_date1[0]), int(split_date1[1]), int(split_date1[2]))
                    transList = transList.filter(add_time__range=(start, d_date1))

                if date2:
                    split_date2 = date2.split('-')
                    d_date2 = datetime.date(int(split_date2[0]), int(split_date2[1]), int(split_date2[2]))
                    transList = transList.filter(add_time__range=(start, d_date2))


            page = request.POST.get('page', '1')
            trans = get_page_result(page, transList, 20)
            context['trans'] = trans
            return render_template(request, 'translate/manager_list.html', context)

    except Exception, e:
        log.error('translate/manager_list:%s' % e)
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
                Translate.objects.filter(id__in=id_list).update(status=2)        # 虚删除
                return HttpResponse('ok')
    except Exception, e:
        log.error('delete:%s' % e)
        return HttpResponse('err')



