#coding=utf-8
import os, datetime, logging
DEBUG = True
TEMPLATE_DEBUG = DEBUG


DIRNAME = os.path.dirname(__file__)


ADMINS = (
    ('BeginMan', 'xinxinyu2011@163.com'),
)

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'GTM-8'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-cn'     # 语言设置为中文简体，admin后台显示语言及form表单验证信息提示使用



SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v3t)(_jc8cb8ad1svj9@u02=o!%k61*v-e=#3^n1)2)s48+5bn'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'commons.middleware.SideBarMiddleware',

)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
    #'common.setting_process.settings',       # 在common中
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
     os.path.join(DIRNAME, "themes"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    #'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'tags',     # 自定义标签或过滤器
    'account',  # 用户
    'blog',     # 博客文章
    'manager',  # 后台管理
    'django.contrib.markup',    # markdown editor
    'wmd',                      # A WMD-Editor wrapper for Django applications.
    'commons',   # 常用
    'about',      # 关于我；日志
    'translate',  # 翻译
    'push',         # 推送
    'photo',    # 图册

)

URLROOT = "http://127.0.0.1:8000"

# 用户上传文件路径
MEDIA_ROOT = os.path.join(DIRNAME, 'upload/')
MEDIA_SITE = os.path.join(DIRNAME, 'media/')
THEME_SITE = os.path.join(DIRNAME, 'themes/')


MEDIA_URL = '/upload_media/'

# wmd编辑器配置
# 项目地址：https://github.com/jpartogi/django-wmd-editor
WMD_SHOW_PREVIEW = True             # 是否显示预览
WMD_ADMIN_SHOW_PREVIEW = False      # 是否显示预览在admin管理

# 日志配置
LOGDIR = os.path.join(DIRNAME, "log")
LOGFILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=os.path.join(LOGDIR, LOGFILE),
                    filemode='a')

# define a Handler which writes INFO messages or higher to the sys.stderr
fileLog = logging.FileHandler(os.path.join(LOGDIR, LOGFILE), 'w')
#from logging import handlers
#fileLog = logging.handlers.TimedRotatingFileHandler( os.path.join(LOGDIR, 'LOGFILE.log') , 's' ,10)

# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
fileLog.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('blog').addHandler(fileLog)
logging.getLogger('blog').setLevel(logging.DEBUG)
logging.getLogger('blog').info("blog.com Started")
