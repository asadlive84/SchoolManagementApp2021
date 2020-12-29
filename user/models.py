from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin

from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _

from user.utils import validators_phone_number


class UserType(models.TextChoices):
    EX_STUDENT = 'ES', _('Ex Student')
    STUDENT = 'S', _('Student')
    Teacher = 'T', _('Teacher')
    PARENT = 'P', _('Parent')
    STAFF = 'St', _('Staff')
    GUEST = 'G', _('Guest')
    CURRENT_COMMITTEE = 'CC', _('Current Committee')
    ADMIN = 'A', _('Admin')
    EDITOR = 'E', _('Editor')
    SUPERVISOR = 'SV', _('Supervisor')


class CustomUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_approve_user = True
        user.user_type = UserType.ADMIN
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_approve_user = models.BooleanField(default=False)
    phone_number = models.IntegerField(unique=True, blank=True, null=True, validators=[validators_phone_number])
    user_type = models.CharField(max_length=3, choices=UserType.choices, default=UserType.GUEST)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
