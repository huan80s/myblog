#coding=utf-8
from django.db import models
from manager import validation      # 自定义验证
from wmd import models as wmd_models

class Carousel(models.Model):
    """主页轮播"""
    TYPE = (
        (0, '网站公告'),     # 只展示重要信息，无连接
        (1, '博客推荐'),     # 链接推荐博客
        (2, '翻译推荐'),     # 链接翻译
    )
    SEQUENCE = (
        (1, 'No1'), (2, 'No2'), (3, 'No3'), (4, 'No4'),
    )
    STATUS = ((1, '有效'), (2, '待用'))
    
    title = models.CharField(u'标题', max_length=100)
    des = models.CharField(u'简介', max_length=500)
    pic = models.FileField(u'缩略图', upload_to='carousel/%Y/%m', null=True, blank=True, validators=[validation.image_valid])     # If the model field has blank=True, then required is set to False on the form field. Otherwise, required=True.
    type = models.IntegerField(u'方式', default=0, choices=TYPE)
    link = models.CharField(u'链接对象', max_length=100, null=True, blank=True, help_text=u'插入URL')
    sequence = models.IntegerField(u'排序', default=1, choices=SEQUENCE)
    status = models.IntegerField(u'状态', default=1, choices=STATUS)          # 状态，1显示，0无效
    html_bk_color = models.CharField(u'背景色', max_length=50, default='#eee')  # 背景色
    html_bk_img = models.FileField(u'背景图', upload_to='carousel/%Y/%m', null=True, validators=[validation.image_valid])    # 背景图片
    add_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    def __unicode__(self):
        return self.title

    class Meta:
       db_table = 'carousel'
    

class Link(models.Model):
    '''链接'''
    name = models.CharField(max_length=200, verbose_name=u'名称')
    url = models.URLField(verify_exists=False, verbose_name=u'链接')
    seq = models.IntegerField(default=0, db_index=True, verbose_name=u'排序')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['seq']
        verbose_name_plural = verbose_name = u'链接'