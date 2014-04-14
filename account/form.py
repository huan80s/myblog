#coding=utf-8
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from blog.models import Pic
from django.forms import ModelForm
from django import forms

class LoginForm(forms.Form):
    """
    ====================================================================
    ** 功能说明:        用户登录表单
    ** 添加时间:        2014/1/4
    ** 开发人员:        BeginMan
    ====================================================================
    """
    AUTO_LOGIN = (
        (1, u'下次自动登录'),
    )
    email = forms.EmailField(label=u'注册邮箱', max_length=100, widget=forms.TextInput(attrs={'placeholder': u'注册邮箱'}))
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput(attrs={'placeholder': u'密码',}))
    remember = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'rem_pwd'}), choices=AUTO_LOGIN, required=False)
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        auth_login = self.cleaned_data.get('remember', 0)  # 是否勾选

        if email and password:
            self.user_cache = authenticate(username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'邮箱或密码错误！')
            else:
                has_user = User.objects.filter(username=email)
                if has_user:
                    has_user = has_user[0]
                    print has_user.username
                    if has_user.type == 0:
                        raise forms.ValidationError(u'请稍等，该帐号正在审核中……')
                elif not self.user_cache.is_active:
                    raise forms.ValidationError(u'该帐号已被禁用！')

        user = self.request.user
        if user.is_authenticated() and user.is_active:
            raise forms.ValidationError(u'您已经登录了,请勿重复登录！')

        if auth_login:      # 如果用户勾选了自动登录
            pass
        return self.cleaned_data

    def get_user_id(self):
        """获取用户id"""
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        """获取用户实例"""
        return self.user_cache


class RegisterForm(forms.Form):
    """
    ====================================================================
    ** 功能说明:        用户注册
    ** 添加时间:        2014/1/4
    ** 开发人员:        BeginMan
    ====================================================================
    """
    email = forms.EmailField(label=u'你的邮箱', max_length=100, widget=forms.TextInput(attrs={'placeholder': u'邮箱方便登录和联系'}))
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput(attrs={'placeholder': u'密码',}))
    who = forms.CharField(label=u'你是谁', max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': u'在提出申请清楚我和你的关系'}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_type = None
        self.user_email = None
        super(RegisterForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleand_data = self.cleaned_data
        email = cleand_data.get('email')
        password = cleand_data.get('password')
        who = cleand_data.get('who', None)

        if who:
            who = who.strip()

        self.user_type = who
        self.user_email = email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'该邮箱已被注册')
        if password:
            password = password.strip()
            if len(password) < 5:
                raise forms.ValidationError(u'密码太短，至少6个字符')

        return cleand_data

    def getType(self):
        """取得用户分类"""
        type = 0    # 默认低粘度用户
        if self.user_type == u'指定用户':  # 如果是我指定的用户
            type = 1
        if self.user_type == 'admin' and self.user_email == '1126514581@qq.com':  # 第二管理员
            type = 2
        return type


class PasswordForm(forms.Form):
    """
    ===============================================================================
    function：    用户修改密码
    developer:    BeginMan
    add-time      2014/1/6
    ===============================================================================
    """
    oldpwd = forms.CharField(label=u'原始密码', widget=forms.PasswordInput(attrs={'placeholder': u'为了安全保障'}))
    password1 = forms.CharField(label=u'新密码', widget=forms.PasswordInput(attrs={'placeholder': u'密码长度在5-12位'}))
    password2 = forms.CharField(label=u'在输入一次', widget=forms.PasswordInput(attrs={'placeholder': u'为了防止输错'}))

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        oldpwd = cleaned_data.get("oldpwd")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not self.user.check_password(oldpwd):
            msg = u"原密码错误。"
            self._errors["oldpwd"] = self.error_class([msg])
            # raise forms.ValidationError(u'原密码错误')
        if password1 and password2:
            if password1!=password2:
                msg = u"两个密码字段不一致。"
                self._errors["password2"] = self.error_class([msg])
            if not 4 < len(password1) < 13:
                msg = u"密码要在5-12位之间。"
                self._errors["password1"] = self.error_class([msg])

        return cleaned_data






