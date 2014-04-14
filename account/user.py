#coding=utf-8
import logging, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from commons.common import render_template
from account.form import LoginForm, RegisterForm, PasswordForm
from account.models import Profiles
from blog.models import Pic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as logout_
from manager.validation import DivErrorList
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
import simplejson as json
from django.views.decorators.csrf import csrf_exempt

log = logging.getLogger(__name__)


def user_login(request):
    """
    ===============================================================================
    function：    登录
    developer:    BeginMan
    add-time      2014/1/4
    ===============================================================================
    """
    context = {}
    try:
        if request.method == 'POST':
            form = LoginForm(request, request.POST)
            if form.is_valid():
                user = form.get_user()  # 获取用户实例
                login(request, user)
                if user.is_superuser:   # 管理员跳转到管理页面
                    return HttpResponseRedirect('/manager/')
                else:                   # 非管理员跳转首页
                    return HttpResponseRedirect('.')

        else:
            form = LoginForm(error_class=DivErrorList)
        context['form'] = form
    except Exception, e:
        log.error('account>index:%s' %e)
        return HttpResponse(e)
    return render_template(request, 'account/login.html', context)

def logut(request):
    """退出"""
    logout_(request)
    return HttpResponseRedirect('/')

def register(request):
    """
    ===============================================================================
    function：    申请注册
    developer:    BeginMan
    add-time      2014/1/4
    ===============================================================================
    """
    context = {}
    try:
        if request.method == 'POST':
            form = RegisterForm(request, request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data.get('password')
                user = User.objects.create_user(username=email, email=email, password=password)
                type = form.getType()  # 获取注册用户类型
                user.type = type
                user.save()
                # 创建用户信息表
                profiles = Profiles.objects.create(user=user)
                return HttpResponseRedirect('/account/register_ok/%s/' %type)

        else:
            form = RegisterForm()
        context['form'] = form
    except Exception, e:
        log.error('account>index:%s' %e)
        return HttpResponse(e)
    return render_template(request, 'account/register.html', context)


def register_ok(request, type=None):
    """注册成功"""
    try:
        if type:
                context = {}
                context['type'] = type
        else:
            return HttpResponseRedirect('/404/')
    except Exception, e:
        log.error('account>register_ok:%s' %e)
        return HttpResponse(e)
    return render_template(request, 'account/register_ok.html', context)



@user_passes_test(lambda u: u.is_active, login_url='/account/login/')
def index(request, id=None):
    """
    ===============================================================================
    function：    用户首页
    developer:    BeginMan
    add-time      2014/1/6
    ===============================================================================
    """
    context = {}
    try:
        if id:
            user = User.objects.filter(pk=id, type__gt=0)
            if user:
                user = user[0]
                profiles = Profiles.objects.filter(user=user)   # 用户额外信息
                if profiles:
                    profiles = profiles[0]
                    user_portrait = "/site_media/images/user/01.png"     # 默认头像
                    if profiles.portrait:       # 头像
                        portrait = Pic.objects.filter(id=profiles.portrait)
                        if portrait:
                            portrait = Pic.objects.get(pk=profiles.portrait).image
                            user_portrait = '/upload_media/%s' %portrait
                    context['profiles'] = profiles
                    context['portrait'] = user_portrait
                context['user'] = user

    except Exception, e:
        log.error('account/index:%s' %e)
        return HttpResponse('err')
    return render_template(request, 'manager/user/index.html', context)

def update_nickname(request):
    """
    ===============================================================================
    function：    用户修改昵称
    developer:    BeginMan
    add-time      2014/1/6
    ===============================================================================
    """
    context ={}
    user = request.user
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        if nickname:
            if User.objects.filter(nickname=nickname).exists():
                return HttpResponse(0)
            else:
                user.nickname = nickname
                user.save()
                return HttpResponse(1)
    return render_template(request, 'manager/user/nickname.html', context)

def update_pwd(request):
    """
    ===============================================================================
    function：    用户修改密码
    developer:    BeginMan
    add-time      2014/1/6
    ===============================================================================
    """
    context = {}
    user = request.user
    if request.method == 'POST':
        form = PasswordForm(user, request.POST)     # 参数位置不能出错
        if form.is_valid():
            pwd = form.cleaned_data['password1']
            user.set_password(pwd)
            return HttpResponseRedirect('/account/user/%s/' % user.id)
    else:
        form = PasswordForm()
    context['form'] = form
    return render_template(request, 'manager/user/pwd.html', context)

@user_passes_test(lambda u: u.is_active, login_url='/account/login/')
def update_pro(request):
    """
    ===============================================================================
    function：    用户修改头像
    developer:    BeginMan
    add-time      2014/1/6
    ===============================================================================
    """
    context = {}
    from blog.form import PicForm
    user = request.user
    profiles = Profiles.objects.filter(user=user)   # 用户额外信息
    if profiles:
        profiles = profiles[0]
    else:
        return HttpResponseRedirect('/404/')

    try:
        user_portrait = "/site_media/images/user/01.png"     # 默认头像
        if request.method == 'POST':
            form = PicForm(request.POST, request.FILES)
            if form.is_valid():
                image = request.FILES['image']
                pic = Pic(type=2, image=image)
                pic.save(120)   # 用户头像120宽度
                profiles.portrait = pic.id
                profiles.save()
                user_portrait = '/upload_media/%s' %pic.image

        else:
            form = PicForm()
            if profiles.portrait:       # 头像
                portrait = Pic.objects.filter(id=profiles.portrait)
                if portrait:
                    portrait = Pic.objects.get(pk=profiles.portrait).image
                    user_portrait = '/upload_media/%s' %portrait


        context['form'] = form
        context['profiles'] = profiles
        context['portrait'] = user_portrait
    except Exception, e:
        log.error('account/index:%s' %e)
        return HttpResponse(e)
    return render_template(request, 'manager/user/portrait.html', context)


