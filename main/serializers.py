from rest_framework import serializers

from custom_auth.models import User
from custom_auth.serializers import UserSerializer
from models import Employee, Company, Employment, Location, RosterEntry

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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location

class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment

class RosterEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = RosterEntry
