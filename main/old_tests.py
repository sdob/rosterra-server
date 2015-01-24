import sys

#from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from models import Company, Employee, Employment, User
import views

import base64 as b64
from urls import B64_RE as bre

# HTTP status codes
MOVED_PERMANENTLY = 301

if False:
    class FindUserViewTestCase(TestCase):

        def test_unauthenticated_user_bounces_to_home(self):
            first = "john"
            last = "smith"
            name = first + "+" + last
            response = self.client.get('/find/' + b64.b64encode(name), follow=True)
            #self.assertRedirects(response, reverse('main.index'), status_code=MOVED_PERMANENTLY)
            #self.assertRedirects(response, '/')

        def test_authenticated_user_gets_right_response(self):
            u1 = User.objects.create_user(username='testuser1', first_name="Nosmo", last_name="King")
            u1.save()
            u2 = User.objects.create_user(username='testuser2', password='hunter2', first_name="Frank", last_name="Zappa")
            u2.save()
            response = self.client.login(username='testuser2', password='hunter2')
            self.assertTrue(response)
            u1name_encoded = b64.b64encode((u1.first_name + "+" + u1.last_name).encode('utf-8'))
            url = '/find/' + u1name_encoded + '/'
            print "url: '%s'" % url; sys.stdout.flush()
            response = self.client.get('/find/' + u1name_encoded + '/', follow=True)
            #self.assertTemplateUsed(response, views.FIND_USER_TEMPLATE)

class LoginViewTestCase(TestCase):

    def setUp(self):
        u = User.objects.create_user(username='testuser1', password='testpassword',
                first_name='Nosmo', last_name='King')
        u.save()

    def test_wrong_credentials(self):
        self.assertFalse(self.client.login(username='testuser1', password='wrong'))

    def test_right_credentials(self):
        self.assertTrue(self.client.login(username='testuser1', password='testpassword'))


class EmployeeModelTestCase(TestCase):

    #def test_creating_user_creates_employee(self):
        #"""Whenever an auth.User is created, a main.Employee must be
        #created to extend the user's profile."""
        #u = User(name="Nosmo King", email="nosmo@example.com")
        #u.save()
        #self.assertIsNotNone(Employee.objects.get(user=u))

    def test_creating_employee_creates_employee(self):
        name = "Nosmo King"
        e = Employee(name=name, email="nosmo@example.com")
        e.save()
        self.assertIsNotNone(Employee.objects.get(name=name))

    def test_non_member_employee_is_not_employee_of_company(self):
        """If no Employment exists between an Employee e
        and a Company c, then e.is_employee_of(c) should return False."""
        c = Company()
        e = Employee()
        self.assertFalse(e.is_employee_of(c))

    def test_non_member_employee_is_not_manager_of_company(self):
        """If no Employment exists between an Employee e
        and a Company c, then e is not a manager of c."""
        c = Company()
        e = Employee()
        self.assertFalse(e.is_manager_of(c))

    def test_member_employee_is_employee_of_company(self):
        """If an Employee e has accepted a relationship with a Company c,
        and vice versa, then e is an employee of c."""
        u = User(username="testuser"); u.save()
        c = Company(); c.save()
        e = u.employee
        m = Employment.objects.create(employee=e, company=c,
                accepted_by_employee=True, accepted_by_company=True)
        m.save()
        self.assertTrue(e.is_employee_of(c))

    def test_creating_employee_becomes_manager(self):
        """When an Employee e creates a Company c, e becomes a
        manager of c."""
        u = User.objects.create(name="testuser")
        u.save()
        c = Company.objects.create(name="testcompany")
        c.save()
        u.employee.create_company(c)
        self.assertTrue(u.employee.is_manager_of(c))
