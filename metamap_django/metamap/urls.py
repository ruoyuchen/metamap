from django.conf.urls import url

from views import etls, metas

app_name = 'metamap'
urlpatterns = [
    url(r'^$', etls.IndexView.as_view(), name='index'),

    url(r'^etls/(?P<pk>[0-9]+)/$', etls.edit, name='edit'),
    url(r'^etls/add/$', etls.add, name='add'),
    url(r'^etls/blood/$', etls.blood_by_name, name='blood_by_name'),
    url(r'^etls/blood/(?P<etlid>[0-9]+)/$', etls.blood, name='blood'),

    url(r'^etls/exec/(?P<etlid>[0-9]+)/$', etls.exec_job, name='exec'),
    url(r'^etls/execlog/(?P<execid>[0-9]+)/$', etls.exec_log, name='execlog'),
    url(r'^etls/getexeclog/(?P<execid>[0-9]+)/$', etls.get_exec_log, name='getexeclog'),
    url(r'^etls/exec_list/(?P<jobid>[0-9]+)/$', etls.ExecLogView.as_view(), name='exec_list'),

    url(r'^etls/generate_job_dag/$', etls.generate_job_dag, name='generate_job_dag'),


    url(r'^meta/col_search/$', metas.MetaView.as_view(), name='col_list'),
    url(r'^meta/tbl_search/$', metas.TBLView.as_view(), name='tbl_list'),
    url(r'^meta/tbl_search/(?P<tblid>[0-9]+)/$', metas.get_table, name='tbl_info'),
]
