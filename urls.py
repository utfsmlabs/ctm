from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'checkin.views.checkin', name='checkin'),
    url(r'^log/', 'checkin.views.log', name='logs'),
    url(r'^check/', 'checkin.views.check', name='check'),
    url(r'^uncheck/', 'checkin.views.uncheck', name='uncheck'),
    url(r'^absences/', 'checkin.views.absences', name='absences'),
    url(r'^private/time', 'tellthetime.views.get_time', name='get_time'),
    url(r'^schedule/', 'checkin.views.schedule', name='schedule'),
    # url(r'^CTM/', include('CTM.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
