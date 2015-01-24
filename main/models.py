import sys

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

# We're using our own custom user model
User = settings.AUTH_USER_MODEL

class Employee(models.Model):
    # Class Employee is an extension to the User model. All users are
    # nominally Employees.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')

    def __unicode__(self):
        return self.name
    
    @property
    def name(self):
        return self.user.name

    @name.setter
    def name(self, name):
        self.user.name = name
        self.user.save()

    def join(self, company):
        ecm, created = Employment.objects.get_or_create(employee=self,
                company=self)
        ecm.accepted_by_employee = True
        ecm.save()

    
class Company(models.Model):
    """A Company is a company/team/organization with multiple
    Locations and multiple employees.
    """
    class Meta:
        """Model metadata for the Company class."""
        verbose_name = 'company'
        verbose_name_plural = "companies" # for OCD's sake
    # Company's name
    name = models.CharField(max_length=200)
    # M2M relationship with Employee class. Each Company can have multiple
    # employees and vice versa.
    employees = models.ManyToManyField(Employee,
            related_name='companies',
            through='Employment')

    def hire(self, employee):
        ecm, created = Employment.objects.get_or_create(employee=employee,
                company=self)
        ecm.accepted_by_company = True
        ecm.save()


    def fire(self, employee):
        pass

    def __unicode__(self):
        return self.name

    def is_managed_by(self, employee):
        try:
            return Employment.objects.get(employee=employee, company=self).is_manager
        except Employment.DoesNotExist:
            return False



class Location(models.Model):
    """A Location is a single site or point of presence, belonging to
    exactly one company."""
    name = models.CharField(max_length=200)
    # Each location belongs to exactly one company, but companies can
    # have multiple locations.
    company = models.ForeignKey(Company, related_name="locations")

    def is_managed_by(self, employee):
        try:
            e = Employment.objects.get(employee=employee, company=self.company)
            return e.is_manager
        except Employment.DoesNotExist:
            return False

    def __unicode__(self):
        return self.name


class Employment(models.Model):
    """
    The through table for a many-to-many relationship between 
    Rosterra Employees (i.e., humans) and Rosterra Companies
    (i.e., groups, corporate entities, etc.). We need a through table
    because we may need to have start/end dates of employment, user role,
    and other attributes on the link between employee and company.
    """
    class Meta:
        unique_together = ('employee', 'company',)
    employee = models.ForeignKey(Employee)
    company = models.ForeignKey(Company)
    date_added = models.DateTimeField(auto_now_add=True)
    is_manager = models.BooleanField(default=False)
    accepted_by_company = models.BooleanField(default=False)
    accepted_by_employee = models.BooleanField(default=False)


class Activity(models.Model):
    """
    An Activity is whatever it is that an employee is doing during a
    shift.
    """
    name = models.CharField(max_length=72)
    company = models.ForeignKey(Company, related_name="activity_types")


class RosterEntry(models.Model):
    """
    A RosterEntry represents an unbroken period of time during which
    an Employee is doing precisely one thing.
    """
    class Meta:
        verbose_name = 'roster_entry'
        verbose_name_plural = 'roster_entries'

    employee = models.ForeignKey(Employee, related_name="activities")
    company = models.ForeignKey(Company, related_name="activities")
    start = models.DateTimeField()
    end = models.DateTimeField()
    activity = models.ForeignKey(Activity)

    def is_managed_by(self, employee):
        try:
            e = Employment.objects.get(employee=employee, company=self.company)
            return e.is_manager
        except Employment.DoesNotExist:
            return False
