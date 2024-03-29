from __future__ import unicode_literals


from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import  PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from.tokens import generate_user_id




class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with given email and password
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)


        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)




class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=16, primary_key=True, default=generate_user_id(16))
    email = models.EmailField(_('email address'), unique=True)
    otp = models.CharField(max_length=6, blank=True)
    
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name= 'profile', on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=11)


#     def get_full_name(self):
#         """
#         Returns the first_name plus the last_name, with a space in-between
#         """
#         full_name = '%s %s' %(self.first_name, self.last_name)
#         return full_name.strip()

#     def get_short_name(self):
#         """
#         Returns the first_name of the user
#         """
#         return self.first_name


