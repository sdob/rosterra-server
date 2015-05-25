import sys
import datetime

from django import forms    
from django.db.models import Q
from django.utils import timezone
from django.utils import dateparse

import django_filters
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import views
from rest_framework import status
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from country_utils.countries import COUNTRY_CHOICES
from custom_auth.models import User
from custom_auth.serializers import UserSerializer
from .serializers import EmployeeSerializer, \
        CompanySerializer, LocationSerializer,\
        RosterEntryReadSerializer, RosterEntryWriteSerializer, \
        EmploymentSerializer, ActivitySerializer
from .models import Employee, Company, Location, Activity, RosterEntry, Employment
from .permissions import IsManagerOrReadOnly, IsOwnerOrReadOnly

class CountryListView(views.APIView):
    def get(self, request, format=None):
        countries = [{'id': c[0], 'name': unicode(c[1])} for c in COUNTRY_CHOICES]
        return Response(countries)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.none()
    serializer_class = ActivitySerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        return Activity.objects.filter(company__in=self.request.user.profile.companies.all())
    def list(self, request):
        queryset = self.get_queryset()
        if 'company' in request.query_params:
            queryset = queryset.filter(company=request.query_params['company'])
        serializer = ActivitySerializer(queryset, many=True)
        return Response(serializer.data)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.none() # overridden by get_queryset
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated, IsManagerOrReadOnly,)
    def get_queryset(self):
        """Default queryset."""
        return self.request.user.profile.companies.all()

    # TODO: We need to restrict the amount of info given out when listing
    # (to just company id and name), and then for detail views decide based
    # on the requesting user's role in the Company whether to hand out
    # things like lists of Employees.


# Employee objects are undeletable and uncreatable through the REST API,
# so we can't just inherit from ModelViewSet. Instead we explicitly mix
# in the behaviour we need.
class EmployeeViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    queryset = Employee.objects.none() # overridden by get_queryset
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    def get_queryset(self):
        """
        By default, users can view their own profile, plus those
        of employees of any company of which they themselves are
        employed. (Will require a refinement to handle managers having
        viewing rights that employees don't.)
        """
        companies = self.request.user.profile.companies.all()
        # Combining with Q() can return duplicates; an easy way to avoid this
        # is to call distinct() on the returned queryset
        return Employee.objects.filter(Q(user__id=self.request.user.id) | Q(companies__in=companies)).distinct()

    # Employees who are managers can get lists of employees of the companies
    # they manage. Non-employees get an empty list.
    def list(self, request):
        employee = Employee.objects.get(user__id=request.user.id)
        managed_employments = Employment.objects.filter(employee=employee, is_manager=True)
        companies = [e.company for e in managed_employments]
        queryset = Employee.objects.filter(companies__in=companies)
        if 'company' in request.query_params:
            queryset = queryset.filter(companies__in=request.query_params['company'])
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Restrict fields if requesting user isn't the owner.
        if not request.user == instance.user:
            existing = set(serializer.fields)
            allowed = set(['id', 'name'])
            for field in existing - allowed:
                serializer.fields.pop(field)
        return Response(serializer.data)


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.none() # overriden by get_queryset
    permission_classes = (IsAuthenticated, IsManagerOrReadOnly,)
    def get_queryset(self):
        """ Return all Locations owned by all companies
        of which the requesting user is an employee."""
        companies = self.request.user.profile.companies.all()
        return Location.objects.filter(company__in=companies)

    def list(self, request):
        """Return the list of locations for the company specified in the request."""
        queryset = self.get_queryset()
        # Optionally, filter on company if in query parameters
        if 'company' in request.query_params:
            queryset = queryset.filter(company=request.query_params['company'])
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        queryset = self.get_queryset()
        employee = request.user.profile
        company = Company.objects.get(id=request.data['company'])
        # Only managers can create Locations
        if company.is_managed_by(employee):
            return super(viewsets.ModelViewSet, self).create(request)
        return self.permission_denied(request)


class EmploymentViewSet(viewsets.ModelViewSet):
    serializer_class = EmploymentSerializer
    queryset = Employment.objects.none() # overriden by get_queryset
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        # Initial filtering reduces the set to those companies of which
        # the user is a member
        companies = self.request.user.profile.companies.all()
        return Employment.objects.filter(company__in=companies)
    def list(self, request):
        e = request.user.profile
        queryset = self.get_queryset()
        # Filter on a single company if it's in the query params
        if 'company' in request.query_params:
            queryset = queryset.filter(company=request.query_params['company'])
        # Filter on a single employee if it's in the query params
        if 'employee' in request.query_params:
            queryset = queryset.filter(employee=request.query_params['employee'])
        # Complex query here that we'll OR together --- only return
        # (a) employments involving this user, or
        # (b) employments involving companies of which they're a manager
        own_employments = Q(employee=e)
        employments_of_managed_companies = Q(
                company=Company.objects.filter(
                    employment__in=Employment.objects.filter(employee=e, is_manager=True)
                    )
                )
        queryset = queryset.filter(own_employments | employments_of_managed_companies)
        # Serialize and return
        s = self.serializer_class(queryset, many=True)
        return Response(s.data)


class RosterEntryViewSet(viewsets.ModelViewSet):
    serializer_class = RosterEntryWriteSerializer
    queryset = Location.objects.none() # overridden by get_queryset
    permission_classes = (IsAuthenticated, IsManagerOrReadOnly,)
    def get_queryset(self):
        """
        Default queryset: return all RosterEntries for all companies
        of which the requesting user is an employee.
        """
        companies = self.request.user.profile.companies.all()
        return RosterEntry.objects.filter(company__in=companies)
    
    def list(self, request):
        # Get the initial queryset
        queryset = self.get_queryset()
        # Filter by company if requested
        if 'company' in request.query_params:
            queryset = queryset.filter(company_id=request.query_params['company'])
        # Filter by location if requested
        if 'location' in request.query_params:
            queryset = queryset.filter(location=request.query_params['location'])
        # Filter by employee if requested
        if 'employee' in request.query_params:
            queryset = queryset.filter(employee=request.query_params['employee'])
        # Filter by start date if requested
        if 'start' in request.query_params:
            bad_request_response = Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'detail': u'Invalid start time'}
                    )
            # Check that the start time parses correctly
            start_time = dateparse.parse_datetime(request.query_params['start'])
            if not start_time:
                return bad_request_response
            try:
                queryset = queryset.filter(start__gte=start_time)
            except forms.ValidationError:
                return bad_request_response
        # Filter by end date if requested
        if 'end' in request.query_params:
            bad_request_response = Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'detail': u'Invalid start time'}
                    )
            end_time = dateparse.parse_datetime(request.query_params['end'])
            if not end_time:
                return bad_request_response
            try:
                queryset = queryset.filter(end__lte=end_time)
            except forms.ValidationError:
                return bad_request_response
        # Return the filtered queryset using the Read serializer
        serializer = RosterEntryReadSerializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request):
        try:
            # First of all, check that the data we have make sense
            company = Company.objects.get(id=request.data['company'])
            employee = Employee.objects.get(id=request.data['employee'])
            activity = Activity.objects.get(id=request.data['activity'])
            # Fail early if the requesting user isn't a manager of
            # this company
            if not company.is_managed_by(request.user.profile):
                return self.permission_denied(request)
            # Check that end time is after start time; if not, return
            # HTTP 400
            start_time = request.data['start']
            end_time = request.data['end']
            if not end_time > start_time:
                return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data = {
                            'detail': 'Start time is later than end time'
                            }
                        )
            # We've parsed the data and it's all OK; use the Write
            # serializer to create the instance and return it using
            # the Read serializer.
            serializer = RosterEntryWriteSerializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                serializer = RosterEntryReadSerializer(serializer.instance)
                return Response(serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        finally:
            pass
