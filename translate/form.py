#coding=utf8
from django.forms import ModelForm
from django import forms
from translate.models import TransCategory, Translate
from django.forms.widgets import RadioFieldRenderer
from django.forms import RadioSelect
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class MyCustomRenderer(RadioFieldRenderer):
    def render(self):
        """自定义 RadioSelect 部件样式
            参考：http://hi.baidu.com/weiokx/item/d30e9b4a075e1cebbdf451a2
        """
        return mark_safe(u'&nbsp;&nbsp;'.join([u'%s' % force_unicode(w) for w in self]))


class TransCategoryForm(ModelForm):
    """翻译分类表单"""
    class Meta:
        model = TransCategory
        fields = ('title', 'summary', 'sequence')
        widgets = {
            'summary': forms.Textarea(),
            'sequence': forms.TextInput(attrs={'onkeyup': "this.value=this.value.replace(/\D/g,'')", 'onafterpaste': "this.value=this.value.replace(/\D/g,'')", 'style': "width:30px;"})
        }

class TransForm(ModelForm):
    """翻译表单"""
    status = forms.IntegerField(label=u'状态', required=False, widget=forms.RadioSelect(renderer=MyCustomRenderer, choices=Translate.STATUS))
    class Meta:
        model = Translate
        fields = ('title', 'category', 'authorship', 'content', 'original_url', 'istop', 'progress', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'span10', 'placeholder': u'标题'}),
            'progress': forms.TextInput(attrs={'onkeyup': "this.value=this.value.replace(/\D/g,'')", 'onafterpaste': "this.value=this.value.replace(/\D/g,'')", 'style': "width:30px;"}),
            'istop': forms.CheckboxInput(attrs={'value': '1'}, check_test=False),
            'status': forms.RadioSelect(renderer=MyCustomRenderer, choices=Translate.STATUS),
        }

