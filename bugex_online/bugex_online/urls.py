# -*- coding: utf-8 -*-

"""
Project: BugEx Online
Authors: Amir Baradaran
         Tim Krones
         Frederik Leonhardt
         Christos Monogios
         Akmal Qodirov
         Iliana Simova
         Peter Stahl
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bugex_online.views.home', name='home'),
    url(r'', include('bugex_webapp.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # This is for the captcha in the registration form
    #url(r'^captcha/', include('captcha.urls')),

    # This is for letting Django serve static files when debug mode is on.
    # IMPORTANT: This is for development purposes only!
    #            Never use Django's server in a production environment!
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# This is for letting Django serve static files when debug mode is off.
# IMPORTANT: This is for development purposes only!
#            Never use Django's server in a production environment!
if settings.DEBUG is False:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.STATIC_ROOT}
        ),
    )