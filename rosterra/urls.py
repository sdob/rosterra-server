from django.conf.urls import patterns, include, url
from custom_auth import views as tokenviews

urlpatterns = patterns('',
        # /authenticate/ is routed to our slight modification of the token authentication service
        url(r'^authenticate', tokenviews.obtain_auth_token, name='token-auth'),
        # everything else is routed to our main API app
        url(r'^', include('main.urls')),
        )
