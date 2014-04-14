#coding=utf-8
from blog.models import Category, Tags, Blog, Sign
from django import forms
from django.forms import ModelForm
from wmd.widgets import MarkDownInput   # 从wmd编辑器导入html组件

class BlogForm(ModelForm):
    """
    ===============================================================================
    function：     博客编辑表单
    developer:    BeginMan
    add-time      2013/12/30
    ===============================================================================
    """
    STATUS = (
        ('1', u'发布'),
        ('0', u'草稿'),
    )
    ISTOP = (
        ('1', u'置顶'),
        ('0', u'不置顶'),
    )
    Can_Comment = (
        ('1', u'允许评论'),   # 分号不能少,否则会出错
        ('0', u'禁止评论'),   # 分号不能少,否则会出错
    )
    category_id = forms.ModelChoiceField(label=u'分类', queryset=Category.objects.order_by('sequence'), empty_label=None)
    tags = forms.CharField(max_length=100, required=False, label=u'标签', widget=forms.TextInput(attrs={'placeholder':u'多个标签用逗号隔开'}))
    title = forms.CharField(max_length=100, label=u'标题', widget=forms.TextInput(attrs={'class':'span11', 'placeholder':u"给文章起个牛逼的标题吧"}))
    summary = forms.CharField(max_length=500, label=u'概要', required=False, widget=forms.Textarea(attrs={'rows':'2', 'class':'span11', 'placeholder':u"文章重点内容概要"}))
    content = forms.CharField(widget=MarkDownInput, label=u'内容')
    status = forms.ChoiceField(choices=STATUS, label=u'状态', widget=forms.RadioSelect())
    istop = forms.ChoiceField(choices=ISTOP, label=u'置顶', widget=forms.RadioSelect())
    cancomment = forms.ChoiceField(choices=Can_Comment, label=u'评论', widget=forms.RadioSelect())
    password = forms.CharField(max_length=100, label=u'访问密码', required=False, widget=forms.PasswordInput())
    class Meta:
        model = Blog
        fields = ('category_id', 'tags', 'summary', 'title', 'content', 'status', 'istop', 'cancomment', 'password')

class SignForm(ModelForm):
    class Meta:
        model = Sign
        exclude = ('add_time',)







