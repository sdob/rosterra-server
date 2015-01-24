from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

from main.models import Employee, Company

class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **kwargs):
        """Create and save a custom user with the given email and password."""
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                is_superuser=is_superuser, last_login=now,
                date_joined=now, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        """Create a non-superuser with the given email and password."""
        return self._create_user(email, password, False, False, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        """Create a superuser with the given email and password."""
        return self._create_user(email, password, True, True, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """A custom User model with admin-compliant permissions that uses
    a full-length email field as the username. Taken from:
    http://www.caktusgroup.com/blog/2013/08/07/migrating-custom-user-model-django/
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
            help_text=_('Designates whether the user can log into this '
                'site.'))
    is_active = models.BooleanField(_('active'), default=True,
            help_text=_('Designates whether this user should be treated '
            'as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = UserManager()
    name = models.CharField(max_length=200)

    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.email

    def get_absolute_url(self):
        return '/users/%s/' % urlquote(self.email)
    
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

