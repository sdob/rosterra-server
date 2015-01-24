from django.conf.urls import patterns, include, url
from rest_framework.authtoken import views as tokenviews

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
        # /authenticate/ s routed to the token authentication service
        url(r'^authenticate', tokenviews.obtain_auth_token, name='token-auth'),
        # everything else is routed to our main API app
        url(r'^', include('main.urls')),
        )
