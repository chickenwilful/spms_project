from django.conf.urls import patterns, url
from transaction import views


urlpatterns = patterns(
    '',
    url(r'^$', views.transaction_list, name='list'),
)