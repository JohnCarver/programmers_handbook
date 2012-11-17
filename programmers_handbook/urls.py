from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'programmers_handbook.views.home', name='home'),
    # url(r'^programmers_handbook/', include('programmers_handbook.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^page/.*/$', 'handbook.views.page', name='page'),
    url(r'^page_edit/.*/$', 'handbook.views.page_edit', name='page_edit'),
    url(r'^page_preview/', 'handbook.views.preview', name='page_preview'),
    url(r'^$', 'handbook.views.index', name='index'),
)
