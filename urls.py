from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'app.views.index', name='home'),
    url(r'^job-file/(?P<jobid>\d+)/(?P<file>.+)/', 'app.views.job_file', name='job-file'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
