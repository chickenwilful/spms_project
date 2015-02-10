from django.conf.urls import patterns, url
from transaction import views


urlpatterns = patterns(
    '',
    url(r'^$', views.transaction_list, name='list'),
    url(r'^estimate/$', views.transaction_list_estimate, name='list_estimate'),
)