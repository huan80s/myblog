#coding=utf-8
import logging
import re, datetime
from django import template
from django.template import Node, TemplateSyntaxError,  resolve_variable
from django.conf import settings as _settings

log = logging.getLogger(__name__)

register = template.Library()


class NavTagNode(template.Node):
    def __init__(self, args, match):
        self.args = args.strip('"')
        self.match = match.strip('"')
    def render(self, context):
        try:         
            cur_path = context['request'].path           
            args_list = self.args.split()           
            path = args_list[0]            
            current = False
            if len(args_list)>1:
                self.match = args_list[1] 
                current = cur_path.startswith(path)
            else:
                if cur_path == path:
                    current = True
            
                
            return current and self.match or '' #如果current为真返回class_name否则返回''
        except Exception, e:
            return ""

def navtagitem(parser, token):
    try:
       
        match = ''
        bits = list(token.split_contents())
    
        tag_name = bits[0]
        args = bits[1]
        if len(bits) > 2:
            match = bits[2]
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requries exactly three arguments: path and text"
        token.split_contents[0]
    return NavTagNode(args, match)

    
