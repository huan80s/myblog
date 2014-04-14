#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from manager import validation      # 自定义验证
TablePrefix = "blog_"
from wmd import models as wmd_models        # 导入wmd的models
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.core.files.base import ContentFile
from PIL import Image
from cStringIO import StringIO
import markdown


class Category(models.Model):
    """分类管理"""
    parent_id = models.IntegerField(default=0)      # 父id
    title = models.CharField(u'类型名称', max_length=100)                 # 类型名称
    des = models.CharField(u'一句话概括为什么创建这个类型',max_length=225, default='')                   # 简介
    sequence = models.IntegerField(default=1)                       # 排序
    count = models.IntegerField(default=0)                          # 该分类下博客数量
    add_time = models.DateTimeField(auto_now=True, auto_now_add=True)   # 添加时间
    class Meta:
        db_table = TablePrefix+'category'
        verbose_name = u'分类管理'
        verbose_name_plural = u'分类管理'
        
    def __unicode__(self):
        return self.title

                    
class Blog(models.Model):
    """博客文章数据模型"""
    user = models.ForeignKey(User,null=True)                      # 用户
    category_id = models.ForeignKey(Category, default=1)                       # 类型,默认状态是未分类
    tags = models.CharField(max_length=100, null=True)        # 博客标签,默认是未分类,逗号分隔
    summary = models.CharField(max_length=500, null=True)          # 概要
    title = models.CharField(max_length=225)            # 博客标题
    content = wmd_models.MarkDownField(u'正文')       # 用于编辑
    content_show = wmd_models.MarkDownField(u'正文显示', null=True)                # 博客正文(用于显示)
    hit = models.IntegerField(default=1)                # 点击率
    comments = models.IntegerField(default=0)             # 评论数量
    goods = models.IntegerField(default=0)                # 赞
    bads = models.IntegerField(default=0)                 # 踩
    status = models.IntegerField(default=1)            # 1发布；0草稿;2虚删
    istop = models.IntegerField(default=0)            # 置顶 1置顶；0否
    cancomment = models.IntegerField(default=1)        # 是否可以评论，1可；0不可
    password = models.CharField(max_length=80, null=True)            # 设置密码
    pic = models.IntegerField(null=True)                 # 博文导图
    add_time = models.DateTimeField(auto_now_add=True)   # 添加时间
    class Meta:
        db_table = TablePrefix+'article'
        verbose_name = u'文章管理'
        verbose_name_plural = u'文章管理'
    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        self.content_show = mark_safe(markdown.markdown(force_unicode(self.content), ['codehilite'], safe_mode='escape'))
        super(Blog, self).save()

    
class Tags(models.Model):
    """博客标签

    Django doctests测试模块
    #Create
    >>>tag1 = Tags.objects.create(name="tag1")
    >>>tag2 = Tags.objects.create(name="tag2")
    # test get_count
    >>>tag1.get_count()
    'tag1:0'
    >>>tag2.get_count()
    'tag2:0'
    """
    name = models.CharField(max_length=100)                 # 标签名称
    add_time = models.DateTimeField(auto_now=True, auto_now_add=True)   # 添加时间
    count = models.IntegerField(default=0)      # 对应博客数量
    class Meta:
        db_table = TablePrefix+'tags'
        verbose_name = u'标签管理'
        verbose_name_plural = u'标签管理'
    def __unicode__(self):
        return self.name
    def get_count(self):
        print '%s:%s' %(self.name, self.count)



class Message(models.Model):
    """留言"""
    name = models.CharField(max_length=225)                 # 标题
    email = models.EmailField()                             # 留言者
    content = models.TextField()                            # 留言内容
    reply_id=models.IntegerField(default=0)                 # 回复
    # 验证码
    add_time = models.DateTimeField(auto_now=True, auto_now_add=True)   # 添加时间
    class Meta:
        db_table = TablePrefix+'message'
        verbose_name = u'留言管理'
        verbose_name_plural = u'留言管理'
    def __unicode__(self):
        return self.title


class Pic(models.Model):
    """图片管理"""
    type = models.IntegerField(default=1)   # 1:博客缩略图;2:用户头像；类型
    ori_image = models.ImageField(u'原图', upload_to='system/uploadimg/original/%Y-%m', null=True, validators=[validation.image_valid])
    image = models.ImageField(u'上传图片', upload_to='system/uploadimg/%Y-%m', null=True, validators=[validation.image_valid])
    add_time = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        db_table = 'images'

    #自动缩略
    def save(self, size=300, *args, **kwargs):
        org_image = Image.open(self.image)
        if org_image.mode not in ('L', 'RGB'):
            org_image = org_image.convert('RGB')

        size = size
        width, height = org_image.size
        if width > size:
            delta = width / size
            height = int(height / delta)
            org_image.thumbnail((size, height), Image.ANTIALIAS)

        #获取文件格式
        split = self.image.name.rsplit('.', 1)
        format = split[1]
        if format.upper() == 'JPG':
            format = 'JPEG'

        # 将图片存入内存
        temp_handle = StringIO()
        org_image.save(temp_handle, format)
        temp_handle.seek(0)

        # 保存图像
        self.image.save(self.image.name, ContentFile(temp_handle.getvalue()), save=False)
        super(Pic, self).save(size, *args, **kwargs)

