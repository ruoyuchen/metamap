# !/usr/bin/env python
# -*- coding: utf-8 -*
'''
created by will 
'''
import logging
import traceback
from time import timezone

from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from rest_framework import viewsets

from metamap.helpers import etlhelper
from metamap.models import AnaETL
from metamap.serializers import AnaETLSerializer
from metamap.utils import httputils
from metamap.utils.constants import DEFAULT_PAGE_SIEZE

logger = logging.getLogger('django')

class AnaETLViewSet(viewsets.ModelViewSet):
    queryset = AnaETL.objects.filter(valid=1).order_by('-ctime')
    serializer_class = AnaETLSerializer

class IndexView(generic.ListView):
    template_name = 'export/list.html'
    context_object_name = 'objs'
    model = AnaETL

    def get_queryset(self):
        if 'search' in self.request.GET and self.request.GET['search'] != '':
            tbl_name_ = self.request.GET['search']
            return AnaETL.objects.filter(valid=1, name__contains=tbl_name_).order_by('-ctime')
        self.paginate_by = DEFAULT_PAGE_SIEZE
        return AnaETL.objects.filter(valid=1).order_by('-ctime')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if 'search' in self.request.GET and self.request.GET['search'] != '':
            context['search'] = self.request.GET['search']
        return context

@transaction.atomic
def add(request):
    if request.method == 'POST':
        obj = AnaETL()
        httputils.post2obj(obj, request.POST, 'id')
        obj.save()
        logger.info('ETL has been created successfully : %s ' % obj)
        return HttpResponseRedirect(reverse('export:index'))
    else:
        return render(request, 'export/edit.html')

def review_sql(request, pk):
    try:
        obj = AnaETL.objects.get(id=pk)
        hql = etlhelper.generate_sql(obj.variables, obj.query)
        return HttpResponse(hql.replace('\n', '<br>'))
    except Exception, e:
        logger.error(e)
        return HttpResponse(e)

def edit(request, pk):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                obj = AnaETL.objects.get(pk=int(pk))
                httputils.post2obj(obj, request.POST, 'id')
                obj.save()
                return HttpResponseRedirect(reverse('export:index'))
        except Exception, e:
            return render(request, 'common/500.html', {'msg': traceback.format_exc().replace('\n', '<br>')})
    else:
        obj = AnaETL.objects.get(pk=pk)
        return render(request, 'export/edit.html', {'obj': obj})