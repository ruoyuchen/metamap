# -*- coding: utf-8 -*
import json
from operator import itemgetter

import redis
# from django.conf import settings
# from django.core.exceptions import ObjectDoesNotExist
from kombu.serialization import pickle
#
# from will_common.models import WillDependencyTask

# pool = redis.ConnectionPool(host=settings.CELERY_REDIS_HOST, port=settings.CELERY_REDIS_PORT, max_connections=2)
#
#
# def get_keys():
#     r = redis.StrictRedis(connection_pool=pool)
#     return [key for key in r.keys() if '_' not in key]
#
#
# def get_queue_info(queue_name, count=-1):
#     r = redis.StrictRedis(connection_pool=pool)
#     messages = r.lrange(queue_name, 0, count)
#     count_dict = {}
#     task_set = list()
#     for m in messages:
#         m = json.loads(m)
#         body_encoding = m['properties']['body_encoding']
#         body = pickle.loads(m['body'].decode(body_encoding))
#         task_name = body['task']
#         try:
#             if 'exec_etl_cli' in task_name:
#                 task_set.add(WillDependencyTask.objects.get(pk=int(body['args'][0])).name)
#             else:
#                 task_set.append(body['args'][0])
#         except ObjectDoesNotExist, e:
#             print ' args is %s ' % body['args'][0]
#         count_dict[task_name] = count_dict.get(task_name, 0) + 1
#     list_ = sorted(count_dict.items(), key=itemgetter(1), reverse=True)
#     return list_, task_set

str = 'gAJ9cQEoVQdleHBpcmVzcQJOVQN1dGNxA4hVBGFyZ3NxBFhKAAAAaGl2ZSAtZiAvdmFyL2F6a2FiYW4tbWV0YW1hcC8yMDE3MDQxOTEyNDYwMi1mYWN0X3Rpbnl2X19mYWN0X3VzZXJfaW5mby5ocWxxBVhCAAAAL3Zhci9hemthYmFuLW1ldGFtYXAvMjAxNzA0MTkxMjQ2MDItZmFjdF90aW55dl9fZmFjdF91c2VyX2luZm8ubG9ncQaGcQdVBWNob3JkcQhOVQljYWxsYmFja3NxCU5VCGVycmJhY2tzcQpOVQd0YXNrc2V0cQtOVQJpZHEMVSQ4M2NjNjBmMy1mYzY5LTRjY2EtOWU2OC1jOGU0NWU1NWVlZTdxDVUHcmV0cmllc3EOSwBVBHRhc2txD1UWbWV0YW1hcC50YXNrcy5leGVjX2V0bHEQVQl0aW1lbGltaXRxEU5OhlUDZXRhcRJOVQZrd2FyZ3NxE31xFHUu'
print(pickle.loads(str.decode('base64')))