# -*- coding: utf-8 -*
"""
Django settings for metamap_django project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import logging
import django.utils.log
import logging.handlers

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nyps=8t#p69#1a$be^m^)c$_3k^*7aldic%p(8jnzh=@wcbk1w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENV_PRD = False
USE_ROOT = True

SESSION_COOKIE_NAME = 'xsid'
CSRF_COOKIE_NAME = 'xcsrftoken'
# email settings
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_USE_TLS = True

PUSH_URL = 'https://advert.jianlc.com/sendMessage.shtml?mobileNo=%s&content=%s'
PUSH_KEY = os.getenv('SMS_PUSH_KEY')
ADMIN_PHONE = 'PWy9rKUlzFLGO8Ry6v368w=='
ADMIN_EMAIL = 'chenxin@yinker.com'
ALLOWED_HOSTS = []

CLUTER_QUEUE = 'default'

HIVE_SERVER = {
    'host': '10.1.5.63',
    'port': 10000,
    'user': 'hdfs',
    'password': '',
}

PATH_AUTH_DICT = {
    'auth.access_etl': 'metamap',
}

# 设置cas服务器地址
CAS_SERVER_URL = "http://dev.will.com:8081/sso/"
# CAS_LOGOUT_COMPLETELY = True
CAS_PROVIDE_URL_TO_LOGOUT = True
# CAS_GATEWAY = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend',
)

import djcelery

djcelery.setup_loader()
DB_HUE = 'hue'
# Celery Beat 设置
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

BROKER_URL = 'redis://localhost:6379'
CELERY_REDIS_HOST = 'localhost'
CELERY_REDIS_PORT = '6379'
# CELERY_ROUTES = {
#     'metamap.tasks.exec_etl_cli': {
#         'queue': 'metamap',
#     },
#     'metamap.tasks.exec_etl': {
#         'queue': 'metamap',
#     },
# }

# Application definition

INSTALLED_APPS = [
    'cas',
    'will_common',
    'metamap.apps.MetamapConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'rest_framework',
]

MIDDLEWARE_CLASSES = [
    'will_common.middleware.viewexception.ViewException',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'will_common.middleware.viewexception.LoginRequire',
    'cas.middleware.CASMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'will_common.middleware.accesstracer.AuthTracer',
]

ROOT_URLCONF = 'metamap_django.metamap_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'metamap_django.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'metamap1',
        'PASSWORD': '',
        'USER': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'TEST': {
            'NAME': 'metamap1',
        },
    },
    'hivemeta': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hive',
        'PASSWORD': 'Zjy@yinker20150309',
        'USER': 'ambari',
        'HOST': '10.1.5.225',
        'PORT': '3306',
    },
    DB_HUE: {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hue',
        'PASSWORD': 'Zjy@yinker20150309',
        'USER': 'root',
        'HOST': '10.1.5.225',
        'PORT': '3306',
    },
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
        # 日志格式
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'metamap/log/metamap_all.log',  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'error_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'metamap/log/metamap_error.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'scprits_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'metamap/log/metamap_script.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'info': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'scripts': {
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'error': {
            'handlers': ['default', 'error_handler'],
            'level': 'ERROR',
            'propagate': True
        },
        'will_common.utils': {
            'handlers': ['error_handler'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}
