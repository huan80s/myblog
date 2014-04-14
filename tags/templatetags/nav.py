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

    
def keywords(parser, token):
    """
    功能说明：突出显示关键字
    ----------------------------------
    修改人        修改时间        修改原因
    ----------------------------------
    徐威        2010-02-23
    """
    try:
        bits = token.contents.split()
        content = bits[1]
        keyword = bits[2]
        truncate = bits[3]
        kwargs = {}
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requries exactly three arguments: path and text"
    return KeywordsTagNode(content, keyword, truncate, **kwargs) 
def cut_title(value, args):
    """
     ------------------------------------------------------------------------
    修改人            修改时间                    修改原因
    ------------------------------------------------------------------------
    杜祖永            2010-09-02                截取字符串,汉字当两个字符处理
    """
    try:
        sub_fix = '...'
        real_len = 0
        args = str(args)
        bits = args.split(' ')
        
        if len(bits) == 2:
            if bits[1] == '' or bits[1] == 'none':
                sub_fix = ''
            else:
                sub_fix = '...'
        cut_len = int(bits[0])
        ret_val = ""
        for s in value:
            if real_len >= cut_len:
                ret_val = ret_val+sub_fix
                break
            if not re.match("^[\u4E00-\u9FA5]+$", s):
                if real_len + 2 <= cut_len:
                    ret_val += s
                    real_len += 2
            else:
                if real_len + 1 <= cut_len:
                    ret_val += s
                    real_len += 1
        return ret_val
    except Exception, e:
        return value

def math_expression(value, args):
    """
    功能说明：比较大小
    """
    result = 0
    try:
        expression = "%s %s" % (value, args)
        result = eval(expression)
    except:
        pass
    return result


def get_user(user_id):
    """
    获取用户
    """
    try:
        from django.db import connections
        cursor = connections["slave"].cursor()
        query = "select real_name from auth_user where id=%s" % user_id
        cursor.execute(query)
        name = cursor.fetchone()
        return name[0]   
    except Exception,e:
        return ""
    
def get_username(user_id):
    """
    获取用户名
    """
    try:
        from django.db import connections
        cursor = connections["slave"].cursor()
        query = "select username from auth_user where id=%s" % user_id
        cursor.execute(query)
        name = cursor.fetchone()
        return name[0]   
    except Exception,e:
        return ""
    
def get_icon(user_id):
    """
    获取头像
    """
    try:
        #return 'http://www.bannei.com/site_media/images/profile/default-student.png'
        from django.db import connections
        cursor = connections["slave"].cursor()
        query = "select type, portrait from auth_user where id=%s" % user_id
        cursor.execute(query)
        result = cursor.fetchone()
        portrait = result[1].strip()
        if portrait:
            return '%s/upload_media/%s' % (_settings.FILE_WEB_URLROOT, portrait)
        else:
            if result[0] == 1:
                return '%s/site_media/images/profile/default-student.png' % _settings.URLROOT
            elif result[0] == 2:
                return '%s/site_media/images/profile/default-parents.png' % _settings.URLROOT
            elif result[0] == 3:
                return '%s/site_media/images/profile/default-teacher.png' % _settings.URLROOT
            elif result[0] == 4:
                return '%s/site_media/images/profile/default-teacher.png' % _settings.URLROOT
    except Exception,e:
        log.error("get_icon:%s" % e)
        return 'http://www.bannei.com/site_media/images/profile/default-student.png'
    
def get_anonymous_icon(user_id):
    """
    获取匿名用户头像
    """
    try: 
        from django.db import connections
        cursor = connections["slave"].cursor()
        query = "select type from auth_user where id=%s" % user_id
        cursor.execute(query)
        result = cursor.fetchone()
        if result[0] == 1:
            return '%s/site_media/images/profile/default-student.png' % _settings.URLROOT
        elif result[0] == 2:
            return '%s/site_media/images/profile/default-parents.png' % _settings.URLROOT
        elif result[0] == 3:
            return '%s/site_media/images/profile/default-teacher.png' % _settings.URLROOT
        elif result[0] == 4:
            return '%s/site_media/images/profile/default-teacher.png' % _settings.URLROOT
    except Exception,e:
        log.error("get_anonymous_icon:%s" % e)
        return 'http://www.bannei.com/site_media/images/profile/default-student.png'

def num_to_ch(num):
    """
    功能说明：讲阿拉伯数字转换成中文数字（转换[0, 10000)之间的阿拉伯数字 ）
    ----------------------------------------------------------------------------
    修改人                修改时间                修改原因
    ----------------------------------------------------------------------------
    陈龙                2012.2.9
    """
    _MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', ) 
    _P0 = (u'', u'十', u'百', u'千', ) 
    _S4= 10 ** 4  
    if 0 > num and num >= _S4:
        return None
    if num < 10: 
        return _MAPPING[num] 
    else: 
        lst = [ ] 
        while num >= 10: 
            lst.append(num % 10) 
            num = num / 10 
        lst.append(num) 
        c = len(lst) # 位数 
        result = u'' 
        for idx, val in enumerate(lst): 
            if val != 0: 
                result += _P0[idx] + _MAPPING[val] 
            if idx < c - 1 and lst[idx + 1] == 0: 
                result += u'零' 
        return result[::-1].replace(u'一十', u'十')   
def score_to_en(score):
    """
    功能说明：讲对应的分数转换为相应的基本A：100-80，B：80-70，C：70-60，D：60以下
    ----------------------------------------------------------------------------
    修改人                修改时间                修改原因
    ----------------------------------------------------------------------------
    陈龙                2012.2.9
    """
    try:
        score = int(score)
        if score>=80:
            return 'A'
        elif 70<=score < 80: 
            return 'B' 
        elif 40<=score < 70: 
            return 'C' 
        elif score < 40: 
            return 'D'  
    except Exception,e:
        log.error("score_to_en:%s" % e)
    return ''

def int_char(num):
    """
        功能说明：数字转换对应字母  1-A …… 26-Z,27-AA
        ----------------------------------------------------------------------------
        修改人                修改时间                修改原因
        ----------------------------------------------------------------------------
        陈龙                2012.2.9
    """
    rtn = ""
    iList = []
    while num/26 != 0 or num % 26 !=  0:
        iList.append(num % 26)
        num /= 26
    
    for index,obj in enumerate(iList):
        if obj <=0  and index+1!=len(iList):
            iList[index+1]-=1
            iList[index]=26+obj
    if iList[-1] == 0:
        iList.remove(iList[-1])
    for index,obj in enumerate(iList):
        c = chr(iList[index] + 64)
        rtn = str(c)+rtn;
    return rtn

def del_br(html):
    """
        功能说明：去掉<p>中最后的br，用于数理化题目渲染
        ----------------------------------------------------------------------------
        修改人                修改时间                修改原因
        ----------------------------------------------------------------------------
        陈龙                2013.12.17
    """
    try:
        del_br_p = re.compile(r'(\n*\s*<\s*br\s*\/?\s*>\n*\s*)+<\/+?p\s*>')
        del_br = re.compile(r'(\n*\s*<\s*br\s*\/?\s*>\n*\s*)+$')
        html = del_br_p.sub("</p>",html)
        html = del_br.sub("",html)
    except Exception,e:
        log.error("del_br:%s" % e)
    return html
def float_int(num):
    i = 0
    if num:
        i = int(round(num))
    return i

def format_time(_datetime):
    try:
        time=''
        last_time = datetime.datetime.now() - _datetime
        days = int(last_time.days)
        seconds = int(last_time.seconds)
        if last_time.days>0:
#             time = u"%d天前" % days
            time = u'%s月%s日' % (_datetime.strftime("%m"),_datetime.strftime("%d"))
        else:
            if seconds >= 3600:
                time = u"%d小时前" % int(seconds/3600)
            if seconds >= 60 and seconds <3600:
                time = u"%d分钟前" % int(seconds/60)
            if seconds < 60:
                time = u"%d秒前" % int(seconds)
        return time
    except Exception,e:
        log.error("format_time:%s" % e)
        return ''
        

register.filter('cut_title', cut_title)
register.tag('keywords', keywords)

register.tag('navtagitem', navtagitem)

register.filter('math_expression', math_expression)
register.filter('get_user', get_user)
register.filter('get_username', get_username)
register.filter('get_icon', get_icon)
register.filter('get_anonymous_icon', get_anonymous_icon)
register.filter('num_to_ch',num_to_ch)
register.filter('score_to_en',score_to_en)
register.filter('int_char',int_char)
register.filter('del_br',del_br)
register.filter('float_int',float_int)
register.filter('format_time',format_time)