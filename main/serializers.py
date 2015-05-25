from rest_framework import serializers

from custom_auth.models import User
from custom_auth.serializers import UserSerializer
from models import Employee, Company, Employment, Location, RosterEntry, Activity

class EmployeeSerializer(serializers.ModelSerializer):
    # Provides fairly full access
    class Meta:
        model = Employee
        fields = ('id', 'name', 'email',
                'address_line_1', 'address_line_2',
                'city', 'country')

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(EmployeeSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        # Explicitly state the data we want
        fields = ('id', 'name',)

class CompanyManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        depth = 1

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location

class EmploymentSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    class Meta:
        model = Employment

class RosterEntryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RosterEntry

class RosterEntryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RosterEntry
        depth = 1

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
