#coding=utf-8
from django.db import models
TablePrefix = 'photo'

class PhotoCategory(models.Model):
    """相册分类"""
    TYPE = (
        (0, u'所有人可见'),
        (1, u'好友可见'),
        (2, u'回答问题可见'),
        (3, u'仅自己可见'),
    )
    title = models.CharField(u'类型名称', max_length=100)                 # 类型名称
    summary = models.CharField(u'相册描述', max_length=500, blank=True, null=True)               # 相册描述
    thumbnail = models.IntegerField(u'相册缩略图', null=True)             # 缩略图
    sequence = models.IntegerField(u'排序', default=1)                   # 排序
    count = models.IntegerField(default=0)                              # 该分类下图片数量
    is_show = models.IntegerField(u'权限', choices=TYPE, default=0)
    add_time = models.DateTimeField(auto_now=True, auto_now_add=True)   # 添加时间
    class Meta:
        db_table = TablePrefix + '_category'

    def __unicode__(self):
        return self.title


class Photo(models.Model):
    """图片"""
    category = models.ForeignKey(PhotoCategory, verbose_name=u'分类')
    title = models.CharField(u'标题', max_length=255, default=u'这张照片太美了……')
    summary = models.CharField(u'关于它的故事', max_length=500, null=True)   # 关于它的故事
    image = models.IntegerField(u'图片', null=True)             # 图片
    add_time = models.DateTimeField(auto_now=True, auto_now_add=True)
    class Meta:
        db_table = TablePrefix + '_photo'

    def __unicode__(self):
        return self.title



