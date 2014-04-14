#coding=utf-8
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from commons.common import render_template
from blog.models import Category,Tags
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

@user_passes_test(lambda u: u.is_superuser, login_url='/commons/prem_tip/1/')   # 只有管理员才能进
def index(request):
    """后台管理首页"""
    try:
        pass
    except Exception, e:
        return HttpResponse(e)
    return render_template(request, 'manager/index.html')
