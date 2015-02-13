from rest_framework import serializers

from custom_auth.models import User
from custom_auth.serializers import UserSerializer
from models import Employee, Company, Employment, Location, RosterEntry, Activity

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        #read_only_fields = ('user',)
        fields = ('id', 'name', )

class EmployeeFullSerializer(serializers.ModelSerializer):
    # This serializer provides much more information; use carefully.
    pass

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
