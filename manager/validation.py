#coding=utf-8
#*********************************************
# state: 表单扩展
# developer:BeginMan
#*********************************************

from django.core.exceptions import ValidationError
from django.forms.util import ErrorList
from django import forms


def image_valid(value):
    """
    ===============================================================================
    function：            上传图片的验证(django默认配置，任何文件不能大于2.5Mb)
    developer:    BeginMan
    add-time      2013/12/29 
    ===============================================================================
    """
    name = value.name
    # 格式(读文件头判断图片类型)
    data = value.read(10).encode('hex')
    filetype = None
    if data.startswith("ffd8ffe"):
        filetype = "jpg"
    elif data.startswith("474946"):
        filetype = "jpg"
    elif data.startswith("424d"):
        filetype="bmp"
    elif data.startswith('89504e470d0a1a0a'):
        filetype="png"

    if not filetype:
        raise ValidationError(u'文件名为%s的图片格式不对' %name)
    # 大小
    size = value.size
    # 1kb=1024 B,1Mb=1024Kb,这里我设置不能大于2Mb
    if size>2*1024*1024:
        raise ValidationError(u'文件名为%s的图片文件太大，不能超过2Mb' %name)
    
def text_valid(value):
    """
    ===============================================================================
    function：            相关文字类型的验证
    developer:    BeginMan
    add-time      2013/12/29 
        注意：这个不等同于“这个字段是必填项。”，因为要传入值
    ===============================================================================
    """
    if value == 'aa':
        raise forms.ValidationError(u'%s 不能是aa' %value)

class DivErrorList(ErrorList):
    """
    ===============================================================================
    function：    自定义错误列表格式
    developer:    BeginMan
    add-time      2014/1/1
    ===============================================================================
    """
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self:
            return u''
        return u'<div class="text-error">%s</div>'%''.join([u'<p class="error">%s</p>' %e for e in self])



    

    
