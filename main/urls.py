from django.conf.urls import patterns, url

from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

import views


router = SimpleRouter()
#router.register(r'users', views.UserViewSet) # No reason to provide this endpoint
router.register(r'companies', views.CompanyViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'roster-entries', views.RosterEntryViewSet, base_name='roster_entry')
router.register(r'employments', views.EmploymentViewSet)
router.register(r'activities', views.ActivityViewSet)

urlpatterns = router.urls
