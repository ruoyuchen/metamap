# !/usr/bin/env python
# -*- coding: utf-8 -*
'''
created by will
'''

from __future__ import absolute_import

import json
import os
import random
import traceback

import time

import django
from celery import shared_task
#
from celery.utils.log import get_task_logger
from django.conf import settings
from marathon import MarathonApp
from marathon import MarathonClient
from marathon.models.container import MarathonContainer, MarathonDockerContainer, MarathonContainerPortMapping

from running_alert.models import MonitorInstance, SparkMonitorInstance
from running_alert.utils import prometheusutils
from running_alert.utils.consts import *
from will_common.utils import PushUtils
from will_common.utils import redisutils

logger = get_task_logger('running_alert')
ROOT_PATH = os.path.dirname(os.path.dirname(__file__)) + '/running_alert/'

c = MarathonClient('http://10.1.5.190:8080')

metric_files = dict()
metric_files['flume'] = '/flume_sample.yaml'
metric_files['kafka'] = '/kafka_sample.yaml'
metric_files['zookeeper'] = '/zookeeper_sample.yaml'
CONTAINER_PORT = 1234
prometheus_container = 'my-prometheus'


def get_avaliable_port():
    rxe = remote_cmd(
        'netstat -lntu | awk \'{print($4)}\' | grep : | awk -F \':\' \'{print $NF}\' | sort -nru ',
        settings.MARATHON_HOST)
    used_ports = [int(i) for i in rxe.split('\r\n')]
    min_port = used_ports[-1]
    start_port = min_port if min_port > settings.START_PORT else settings.START_PORT
    start_port = start_port + random.randint(1, 30000)
    while start_port in used_ports:
        start_port = start_port + 1
    return start_port


@shared_task(queue='running_alert')
def check_new_inst(name='check_new_inst'):
    try:
        last_run = redisutils.get_val(REDIS_KEY_JMX_CHECK_LAST_ADD_TIME)
        insts = MonitorInstance.objects.filter(utime__gt=last_run, valid=1)
        reset_last_run_time(REDIS_KEY_JMX_CHECK_LAST_ADD_TIME)
        if len(insts) > 0:
            running_ids = [app.id for app in c.list_apps()]
        else:
            return
        need_restart = False
        for inst in insts:
            tmp_id = get_jmx_app_id(inst)
            host_port = get_avaliable_port()
            service_port = 0
            if tmp_id not in running_ids:
                '''
                run the docker container in marathon
                '''
                port_maps = [
                    MarathonContainerPortMapping(container_port=CONTAINER_PORT, host_port=host_port,
                                                 service_port=service_port)
                ]
                parameters = [{"key": "add-host", "value": "datanode02.yinker.com:10.2.19.83"}, ]
                docker = MarathonDockerContainer(image='ruoyuchen/jmxexporters', network='BRIDGE',
                                                 port_mappings=port_maps, force_pull_image=True, parameters=parameters)
                container = MarathonContainer(docker=docker)
                cmd = 'sh /entrypoint.sh ' + inst.host_and_port + CONTAINER_PORT + ' ' + metric_files[
                    inst.service_type] + tmp_id
                # domain_name = hp_inst + '.' + inst.service_type + '.moniter.com'
                # labels = {'HAPROXY_GROUP': 'external',
                #           'HAPROXY_0_VHOST': domain_name}
                # new_app = MarathonApp(cmd=cmd, mem=32, cpus=0.25, instances=1, container=container, labels=labels)
                #
                # new_result = c.create_app(tmp_id, new_app)
                # logger.info('new app %s has been created' % new_result.id)
                #
                # '''
                # add new target and alert rule file to prometheus
                # '''
                # echo_command = 'echo "10.1.5.190 %s">> /tmp/prometheus/hosts  ' % domain_name
                # target_command = ' && echo \'[ {"targets": [ "%s"] }]\' > /tmp/prometheus/sds/%s_online.json ' % (domain_name, domain_name)
                # rule_command = ' && sed -e \'s/${alert_name}/%s/g\' -e \'s/${target}/%s/g\' -e \'s/${srv_type}/%s/g\' /tmp/prometheus/rules/simple_jmx.rule_template > /tmp/prometheus/rules/%s.rules ' % (
                #     tmp_id, domain_name, inst.service_type, domain_name)
                # restart_command = ' && docker restart %s' % prometheus_container
                labels = {}
                new_app = MarathonApp(cmd=cmd, mem=32, cpus=0.25, instances=1, container=container, labels=labels)

                new_result = c.create_app(tmp_id, new_app)
                logger.info('new app %s has been created' % new_result.id)

                '''
                add new target and alert rule file to prometheus
                '''
                echo_command = ' echo ccc'
                target_command = ' && echo \'[ {"targets": [ "%s"] }]\' > /tmp/prometheus/sds/%s_online.json ' % (
                    inst.host_and_port, tmp_id)
                rule_command = ' && sed -e \'s/${alert_name}/%s/g\' -e \'s/${target}/%s/g\' -e \'s/${srv_type}/%s/g\' /tmp/prometheus/rules/simple_jmx.rule_template > /tmp/prometheus/rules/%s.rules ' % (
                    tmp_id, inst.host_and_port, inst.service_type, tmp_id)
                remote_cmd(echo_command + target_command + rule_command)
                logger.info('domain %s has been registered to %s' % (tmp_id, settings.PROMETHEUS_HOST))
                need_restart = True
            else:
                c.scale_app(id, delta=-1)
                time.sleep(10)
                c.scale_app(id, delta=1)
            inst.exporter_uri = host_port
            inst.save()

        if need_restart:
            restart_command = 'docker restart %s' % prometheus_container
            remote_cmd(restart_command)
            logger.info('prometheus has been restarted')
    except Exception, e:
        logger.error('ERROR: %s' % traceback.format_exc())


def get_jmx_app_id(inst):
    hp_inst = inst.host_and_port.replace('.', '_').replace(':', '_')
    tmp_id = '/' + inst.service_type + '__' + hp_inst
    return tmp_id


@shared_task
def check_new_spark(name='check_new_spark'):
    last_run = redisutils.get_val(REDIS_KEY_SPARK_CHECK_LAST_ADD_TIME)
    print('last run is {ll}'.format(ll=last_run))
    insts = SparkMonitorInstance.objects.filter(utime__gt=last_run, valid=1)
    reset_last_run_time(REDIS_KEY_SPARK_CHECK_LAST_ADD_TIME)
    need_restart = False
    for inst in insts:
        if not is_spark_rule_exist(inst.instance_name):
            '''
            add new alert rule file to prometheus
            '''
            echo_command = ' echo ------------------------'
            rule_command = ' && sed -e \'s/${alert_name}/%s/g\' -e \'s/${target}/%s/g\' /tmp/prometheus/rules/simple_spark.rule_template > /tmp/prometheus/rules/%s.rules ' % (
                inst.instance_name, inst.instance_name, inst.instance_name)
            remote_cmd(echo_command + rule_command)
            need_restart = True
            logger.info('spark streaming %s has been registered to %s' % (inst.instance_name, settings.PROMETHEUS_HOST))
    if need_restart:
        restart_command = 'docker restart %s' % prometheus_container
        remote_cmd(restart_command)
        logger.info('prometheus has been restarted')


def reset_last_run_time(k):
    redisutils.set_val(k, django.utils.timezone.now())


@shared_task
def check_disabled_spark(name='check_disabled_spark'):
    last_run = redisutils.get_val(REDIS_KEY_SPARK_CHECK_LAST_MINUS_TIME)
    insts = SparkMonitorInstance.objects.filter(utime__gt=last_run, valid=0)
    reset_last_run_time(REDIS_KEY_SPARK_CHECK_LAST_MINUS_TIME)
    need_restart = False
    for inst in insts:
        '''
        delete alert rule file to prometheus
        '''
        remote_cmd('rm -vf /tmp/prometheus/rules/%s.rules'
                   % (inst.instance_name))
        need_restart = True
        logger.info('spark streaming %s has been unregistered to %s' % (inst.instance_name, settings.PROMETHEUS_HOST))
    if need_restart:
        restart_command = 'docker restart %s' % prometheus_container
        remote_cmd(restart_command)
        logger.info('prometheus has been restarted')


@shared_task
def check_disabled_jmx(name='check_disabled_jmx'):
    last_run = redisutils.get_val(REDIS_KEY_JMX_CHECK_LAST_MINUS_TIME)
    insts = MonitorInstance.objects.filter(utime__gt=last_run, valid=0)
    reset_last_run_time(REDIS_KEY_JMX_CHECK_LAST_MINUS_TIME)
    to_del = set()
    for inst in insts:
        try:
            '''
            delete target file to prometheus
            '''
            remote_cmd = 'rm -vf /tmp/prometheus/sds/%s_online.json' % inst.instance_name
            remote_cmd(remote_cmd)
            logger.info('jmx %s has been unregistered to %s' % (inst.instance_name, settings.PROMETHEUS_HOST))

            to_del.add(inst.instance_name)
            logger.info('jmx {inst_name} alert has been unregistered to {host}'.format(inst_name=inst.instance_name,
                                                                                       host=settings.PROMETHEUS_HOST))
            '''
            delete marathon app
            '''
            app_id = get_jmx_app_id(inst)
            resp = json.loads(c.delete_app(app_id=app_id))
            logger.info('del %s response message: %s' % (app_id, json.dumps(resp)))
        except Exception, e:
            print traceback.format_exc()
            PushUtils.push_to_admin('msg is {message}'.format(message=e.message))
    if len(to_del) > 0:
        '''
        delete alert rule file to prometheus
        '''
        restart_command = 'docker restart %s' % prometheus_container
        to_del.add(restart_command)
        cmd = (' && ').join(['rm -vf /tmp/prometheus/rules/%s.rules' % ii for ii in to_del])
        logger.info(remote_cmd(cmd))
        logger.info('prometheus has been restarted')


def is_spark_rule_exist(app_name):
    result = remote_cmd(
        'if [ -f /tmp/prometheus/rules/{app_name}.rules ]; then echo exist; fi'.format(app_name=app_name))
    if result == 'exist':
        return True
    return False


def remote_cmd(remote_cmd, target_host=settings.PROMETHEUS_HOST):
    '''
    run command on the prometheus remote host useing fabric
    :param remote_cmd:
    :return:
    '''
    from fabric.api import run
    from fabric.api import env
    env.host_string = target_host
    result = run(remote_cmd)
    env.host_string = ''
    return result