from django.conf.urls import patterns, include, url
from django.contrib import admin
from transaction import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'spms_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.transaction_list, name="list")
    # url(r'^home/', include('transaction.urls', namespace="transaction")),
)

