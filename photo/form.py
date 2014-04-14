#coding=utf8
from django.forms import ModelForm
from django import forms
from photo.models import PhotoCategory, Photo


class PhotoCategoryForm(ModelForm):
    """图册分类表单"""
    class Meta:
        model = PhotoCategory
        fields = ('title', 'summary', 'sequence', 'is_show')
        widgets = {
            'summary': forms.Textarea(attrs={'placeholder': u'说说这个相册的故事……非必填'}),
            'sequence': forms.TextInput(attrs={'onkeyup': "this.value=this.value.replace(/\D/g,'')", 'onafterpaste': "this.value=this.value.replace(/\D/g,'')", 'style': "width:30px;"}),
            'is_show': forms.Select(choices=(PhotoCategory.TYPE))
        }


