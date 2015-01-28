import sys

from django.db.models import Q

import django_filters
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from custom_auth.models import User
from custom_auth.serializers import UserSerializer
from .serializers import EmployeeSerializer, CompanySerializer, LocationSerializer,\
        RosterEntrySerializer
from .models import Employee, Company, Location
from .permissions import IsManagerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.none() # overridden by get_queryset
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated, IsManagerOrReadOnly,)
    def get_queryset(self):
        """Default queryset."""
        return self.request.user.profile.companies.all()


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.none() # overridden by get_queryset
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        """
        By default, users can view their own profile, plus those
        of employees of any company of which they themselves are
        employed. (Will require a refinement to handle managers having
        viewing rights that employees don't.)
        """
        companies = self.request.user.profile.companies.all()
        return Employee.objects.filter(Q(user__id=self.request.user.id) | Q(companies__in=companies))

    @detail_route(methods=['get'])
    def profile(self, request, pk=None):
        """Return the requesting user's profile JSON."""
        # Get the requesting user's profile
        e = Employee.objects.get(user__id=request.user.id)
        # Serialize it
        serializer = EmployeeSerializer(instance=e)
        return Response(serializer.data)


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.none() # overriden by get_queryset
    permission_classes = (IsAuthenticated, IsManagerOrReadOnly,)
    def get_queryset(self):
        """
        Default queryset: return all Locations owned by all companies
        of which the requesting user is an employee.
        """
        companies = self.request.user.profile.companies.all()
        return Location.objects.filter(company__in=companies)

    def list(self, request):
        """
        Return the list of locations for the company specified in the request.
        """
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


class RosterEntryViewSet(viewsets.ModelViewSet):
    serializer_class = RosterEntrySerializer
    queryset = Location.objects.none() # overridden by get_queryset
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        """
        Default queryset: return all RosterEntries for all companies
        of which the requesting user is an employee.
        """
        companies = self.request.user.profile.companies.all()
        return RosterEntry.objects.get(company__in==companies)
