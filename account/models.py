#coding=utf8
import logging,datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings as _settings

log = logging.getLogger('account.models')

class ProfileBase(type):
    def __new__(cls, name, bases, attrs): 
        module = attrs.pop('__module__')
       
        parents = [b for b in bases if isinstance(b, ProfileBase)]   
        
        if parents:
            fields = []
            for obj_name, obj in attrs.items():   
                if isinstance(obj, models.Field): fields.append(obj_name)   
                User.add_to_class(obj_name, obj)
            #UserAdmin.fieldsets = list(UserAdmin.fieldsets)   
            #UserAdmin.fieldsets.append((name, {'fields': fields}))   
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)

class ProfileUser(object):
    __metaclass__ = ProfileBase

class MyProfile(ProfileUser):
    """
    function: extend the attribute of User
    add_time:2013/12/25
    developer:BeginMan
    """

    nickname = models.CharField(max_length=80)
    type = models.IntegerField(default=0)       # 类型


class Profiles(models.Model):
    """
    function: user table
    add_time:2013/12/25
    developer:BeginMan
    """
    user = models.ForeignKey(User)
    real_name = models.CharField(max_length=255, null=True)
    portrait = models.IntegerField(null=True) # 头像
    intro = models.TextField(null=True) # 简介
    class Meta:
        db_table = "profiles"

    def __unicode__(self):
        return '%s' %real_name







