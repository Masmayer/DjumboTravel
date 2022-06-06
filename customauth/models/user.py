from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _


class Usermanager(BaseUserManager):
    """ User manager for user model """
    def _create_user(self, nif, password, **extra_fields):
        """ Create and save a user with given nif and password """
        if not nif:
            raise ValueError('userid must be set')
        user = self.model(nif=nif, **extra_fields)
        user.set_password(password)  # Encrypt password
        user.save(using=self._db)  # safe for multiple databases
        return user

    def create_user(self, nif, password=None, **extra_fields):
        """ Create and save a user with given nif and password """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(nif, password, **extra_fields)

    def create_staffuser(self, nif, password, **extra_fields):
        """ Create and save a staff user with given nif and password """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(nif, password, **extra_fields)

    def create_superuser(self, nif, password, **extra_fields):
        """ Create and save a superuser with given nif and password """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(nif, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('attendant', 'Attendant'),
        ('provider', 'Provider')
    )
    name = models.CharField(_('Name'), max_length=255)
    nif = models.PositiveIntegerField(
        _("UserID"), unique=True, db_index=True
    )
    is_staff = models.BooleanField(_("Staff Status"), default=False)
    is_active = models.BooleanField(_("Active Status"), default=True)
    user_type = models.CharField(
        _("User Type"), max_length=10, choices=USER_TYPE_CHOICES
    )
    accepted_terms = models.BooleanField(_("accepted terms"), default=False)
    read_terms = models.BooleanField(_("terms read"), default=False)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True)

    objects = Usermanager()  # Custom user manager

    USERNAME_FIELD = "nif"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "USERS"

    def __str__(self):
        return f"{self.nif}-{self.name}"
