from django.conf.urls import patterns, url
from transaction import views


urlpatterns = patterns(
    '',
    url(r'^$', views.transaction_list, name='list'),
    url(r'chart/$', views.chart, name='chart'),
    url(r'chart_retrieve/$', views.chart_retrieve, name='chart_retrieve'),
)