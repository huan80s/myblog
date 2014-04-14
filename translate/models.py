#coding=utf-8
from django.db import models
from wmd import models as wmd_models        # 导入wmd的models
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
import markdown
from django.contrib.auth.models import User
TablePrefix = 'translate'

class TransCategory(models.Model):
    """分类管理"""
    parent_id = models.IntegerField(default=0)      # 父id
    title = models.CharField(u'类型名称', max_length=100)                 # 类型名称
    summary = models.CharField(u'简述', max_length=500, null=True, blank=True)        # 简述
    sequence = models.IntegerField(default=1)                       # 排序
    status = models.IntegerField(default=1)                         # 状态，1：正常；2：虚删
    count = models.IntegerField(default=0)                          # 该分类下文章数量
    add_time = models.DateTimeField(auto_now=True, auto_now_add=True)   # 添加时间
    class Meta:
        db_table = TablePrefix + '_category'
        verbose_name = u'翻译分类管理'
        verbose_name_plural = u'翻译分类管理'

    def __unicode__(self):
        return self.title


class Translate(models.Model):
    """翻译"""
    STATUS = (
        (0, u'草稿'),
        (1, u'发布'),
    )
    category = models.ForeignKey(TransCategory, verbose_name=u'分类', null=True, blank=True)
    user = models.ForeignKey(User, null=True)           # 译者
    authorship = models.CharField(u'原作者', max_length=50, default=u'来源网络') # 原作者
    summary = models.CharField(max_length=500, null=True)          # 概要
    title = models.CharField(u'标题', max_length=225)            # 标题
    content = wmd_models.MarkDownField(u'正文')                # 博客正文(Markdown编辑)
    content_show = wmd_models.MarkDownField(u'正文显示', null=True)                # 正文(用于显示)
    hit = models.IntegerField(default=1)                # 点击率
    comments = models.IntegerField(default=0)           # 评论数量
    goods = models.IntegerField(default=0)
    bads = models.IntegerField(default=0)
    istop = models.BooleanField(u'置顶', default=0)              # 置顶 1置顶；0否
    status = models.IntegerField(u'状态', default=1, choices=STATUS)             # 1发布；0草稿；2虚除
    original_url = models.URLField(u'原网址', max_length=255)      # 原网页
    progress = models.IntegerField(u'进度', null=True, blank=True)    # 进度
    add_time = models.DateTimeField(auto_now_add=True)  # 添加时间
    class Meta:
        db_table = TablePrefix + '_translate'
    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        self.content_show = mark_safe(markdown.markdown(force_unicode(self.content), ['codehilite'], safe_mode='escape'))
        super(Translate, self).save()



