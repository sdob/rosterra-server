import sys

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from models import Employee, Company, Activity

#from forms import FindUserForm
import forms

# some strings
HOME_UNAUTHENTICATED_TEMPLATE = 'main/home_unauthenticated.html'
HOME_AUTHENTICATED_TEMPLATE_COMPANY =  'main/home_authenticated_company.html'
HOME_AUTHENTICATED_TEMPLATE_EMPLOYEE =  'main/home_authenticated_employee.html'
COMPANY_SIGNUP_TEMPLATE = 'main/signup_company.html'
EMPLOYEE_ROSTER_TEMPLATE = 'main/employee_roster.html'

def home(request):
    # If the user is logged in, return the 'homepage' view;
    # otherwise, show the default splash page
    if request.user.is_authenticated():
        try:
            employee = request.user.employee
            template = loader.get_template(HOME_AUTHENTICATED_TEMPLATE_EMPLOYEE)
            # Is this user a Company or Employee?
            context = RequestContext(request, {
                'employee': employee})
        except Employee.DoesNotExist:
            company = request.user.company
            template = loader.get_template(HOME_AUTHENTICATED_TEMPLATE_COMPANY)
            all_ecms = company.employeecompanymembership_set.all()
            context = RequestContext(request, {
                'company_name': company,
                'employees': [ecm.employee for ecm in all_ecms.filter(accepted_by_company=True,
                    accepted_by_employee=True)],
                'offers': [ecm.employee for ecm in all_ecms.filter(accepted_by_company=True,
                    accepted_by_employee=False)],
                'join_requests': all_ecms.filter(accepted_by_company=False,
                    accepted_by_employee=True),
                'locations': company.locations.all()
                })
    else:
        template = loader.get_template(HOME_UNAUTHENTICATED_TEMPLATE)
        context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def logout(request):
    # No need for @login_required; if the user is unauthenticated, then
    # this view should just do nothing
    auth_views.logout(request)
    return redirect('/')

###############################################################################
# Signup views
###############################################################################

# Step 1: user chooses account type
def signup_choose_user_type(request):
    if request.method == 'POST':
        # TODO: Handle form data
        pass
    else:
        # Show empty form
        form = forms.UserTypeSelectionForm()
        context = RequestContext(request, {'form': form})
        template = loader.get_template('main/signup_choose_user_type.html')
        return HttpResponse(template.render(context))

# Step 2a: individual user
def signup_individual(request):
    # TODO: build the initial individual signup page
    # and return it to the user
    if request.method == 'POST':
        # handle form data
        pass
    else:
        form = forms.IndividualSignupForm()
        context = RequestContext(request, {})
        template = loader.get_template('main/signup_individual.html')
        return HttpResponse(template.render(context))


# Step 2b individual user
def signup_company(request):
    if request.method == 'POST':
        # Data received
        form = UserCreationForm(request.POST)
        if form.is_valid():
            pass
    else:
        # Show empty form for signup
        form = UserCreationForm()
        context = RequestContext(request, {'form': form})
        template = loader.get_template(COMPANY_SIGNUP_TEMPLATE)
        return HttpResponse(template.render(context))


###############################################################################
# Employee rosters
###############################################################################

def show_employee_roster(request, username):
    def allowed_to_view(user, employee):
        # Users are allowed to view their own rosters
        if user == employee.user:
            return True
        # Companies by which a user is employed are allowed to view the rosters
        # that apply to that company
        try:
            company = user.company
            if employee.is_employee_of(company) or company.accepts_as_employee(employee):
                return True
            # user does not have the right to view this employee's roster at all
            return False
        except Company.DoesNotExist: # user is not a company
            return False

    if not request.user.is_authenticated():
        return redirect(HOME_UNAUTHENTICATED_TEMPLATE)
    user = request.user
    employee_user = User.objects.get(username=username)
    employee = Employee.objects.get(user=employee_user)
    if allowed_to_view(user, employee):
        print user.company
        print employee
        activities = Activity.objects.filter(employee=employee, company=user.company)
        context = RequestContext(request, {'activities': activities})
        template = loader.get_template(EMPLOYEE_ROSTER_TEMPLATE)
        return HttpResponse(template.render(context))
    return redirect(HOME_UNAUTHENTICATED_TEMPLATE)

###############################################################################
# Finding users
###############################################################################
@login_required
def find_user(request):
    if request.method == 'POST':
        form = FindUserForm(request.POST)
        if form.is_valid():
            print form
    else:
        form = FindUserForm()
        return render(request, 'main/find_user.html', {'form': form})

