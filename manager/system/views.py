#coding=utf-8
import logging, datetime
from django.http import HttpResponse, HttpResponseRedirect
from commons.common import render_template
from blog.models import Category,Tags,Blog
from manager.models import Carousel
from manager.system.form import AddCarousel
import simplejson as json
from markdown import markdown
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

log = logging.getLogger(__name__)
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
@csrf_protect
def carousel(request):
    """
    ===============================================================================
    function：            轮播管理
    developer:    BeginMan
    add-time      2013/12/29 
    ===============================================================================
    """
    context = {}
    try:
        if request.method == "POST":
            form = AddCarousel(request.POST, request.FILES)
            if form.is_valid():
                form.save()     # 保存
                return HttpResponseRedirect('/')
                
        else:
             form = AddCarousel()
                    
        context['form'] = form
    except Exception, e:
        log.error('carousel:%s' % e)
        return HttpResponse('err')
    return render_template(request,'manager/system/carousel.html',context)