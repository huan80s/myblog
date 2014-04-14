#coding=utf-8
from manager.models import Carousel
from django import forms
from django.forms import ModelForm
from manager import validation      # 自定义验证
from wmd.widgets import MarkDownInput

class AddCarousel(ModelForm):
    """
    ===============================================================================
    function：    轮播表单
    developer:    BeginMan
    add-time      2013/12/28 
    ===============================================================================
    """
    html_bk_img = forms.FileField(required=False, label='背景图片')
    
    class Meta:
        model = Carousel
        fields = ('title', 'des', 'pic', 'type', 'link', 'sequence', 'status', 'html_bk_color', 'html_bk_img')
        widgets = {
            'des': forms.Textarea(attrs={'cols': 80, 'rows': 3, 'placeholder': u'轮播的重要信息'})
        }
