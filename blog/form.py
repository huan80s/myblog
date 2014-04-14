#coding=utf-8
from blog.models import Blog,Tags,Pic, Sign
from django.forms import ModelForm
from django import forms
import Image

class PicForm(forms.Form):
    """
    ===============================================================================
    function：    图片表单
    developer:    BeginMan
    add-time      2014/1/6
    ===============================================================================
    """
    image = forms.ImageField(label=u'上传图片')