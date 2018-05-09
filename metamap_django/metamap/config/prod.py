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
ENV_PRD = True

SESSION_COOKIE_NAME = 'runningdata_sid'
CSRF_COOKIE_NAME = 'runningdata_csrftoken'

from init_config import result
from celery_conf import *

DEBUG = result.get('DEBUG', False)
# email settings
EMAIL_HOST = result['EMAIL_HOST']
EMAIL_HOST_USER = result['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = result['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = result['EMAIL_USE_TLS']

EMAIL_CANDIDATES = result['EMAIL_CANDIDATES']

# use root to execute....
USE_ROOT = True

# push url
PUSH_URL = result['PUSH_URL']
PUSH_KEY = result['PUSH_KEY']
ADMIN_PHONE = 'PWy9rKUlzFLGO8Ry6v368w=='
ADMIN_EMAIL = result['ADMIN_EMAIL']
PROC_USER = 'metamap'

# ALLOWED_HOSTS = ['dev.will.com']
ALLOWED_HOSTS = result.get('ALLOWD_HOSTS',
                           ['127.0.0.1', '10.2.19.62',
                            '10.1.5.83', '10.2.19.124', '10.103.27.171', '10.103.70.27'])
CLUTER_QUEUE = 'xstorm'

NN_HOSTS = ['10.2.19.72', '10.2.19.106']
DEFAULT_PASSWD = 'qwer1234'
DB_HUE = 'hue'

HIVE_SERVER = {
    'host': result['HIVE_SERVER_HOST'],
    'port': result['HIVE_PORT'],
    'user': result['HIVE_USER'],
    'password': result['HIVE_PWD'],
}

# 设置cas服务器地址
CAS_SERVER_URL = "http://{server_name}/sso/".format(server_name=result['CAS_SERVER_URL'])
CAS_IDC_SERVER_URL = "http://10.2.19.113:8181/sso/"
# CAS_LOGOUT_COMPLETELY = True
CAS_PROVIDE_URL_TO_LOGOUT = True
# CAS_GATEWAY = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend',
)

# Application definition

INSTALLED_APPS = [
    'will_common',
    'cas',
    'metamap',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'rest_framework',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

PATH_AUTH_DICT = {
    'auth.access_etl': '/metamap',
    'auth.access_clean': '/clean',
    'auth.access_hadmin': '/hadmin',
}

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
    'will_common.middleware.accesstracer.AccessTracer',
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
        'NAME': result['MAIN_DB_NAME'],
        'PASSWORD': result['MAIN_DB_PWD'],
        'USER': result['MAIN_DB_USER'],
        'HOST': result['MAIN_DB_HOST'],
        'PORT': result['MAIN_DB_PORT'],
        'TEST': {
            'NAME': 'metamap1',
        },
    },
    'hivemeta': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': result['HIVEMETA_DB_NAME'],
        'PASSWORD': result['HIVEMETA_DB_PWD'],
        'USER': result['HIVEMETA_DB_USER'],
        'HOST': result['HIVEMETA_DB_HOST'],
        'PORT': result['HIVEMETA_DB_PORT'],
    },
    DB_HUE: {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': result['HUE_DB_NAME'],
        'PASSWORD': result['HUE_DB_PWD'],
        'USER': result['HUE_DB_USER'],
        'HOST': result['HUE_DB_HOST'],
        'PORT': result['HUE_DB_PORT'],
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

TIME_ZONE = 'Asia/Shanghai'

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
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/metamap_all.log',  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'error_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/metamap_error.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'scprits_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/metamap_script.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'info': {
            'handlers': ['default'],
            'level': 'INFO',
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
