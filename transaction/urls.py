from django.conf.urls import patterns, url
from transaction import views


urlpatterns = patterns(
    '',
    url(r'^$', views.transaction_list, name='list'),
    url(r'^map/$', views.map, name='map'),
    url(r'^coordinate/$', views.coordinate, name='coordinate'),
)