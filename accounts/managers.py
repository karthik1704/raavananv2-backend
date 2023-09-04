from django.contrib.auth.models import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None):

        if not password:
            raise ValueError("Password is must !")

        user = self.model(
            username=username,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password):
        user = self.create_user(
            username=username,
            phone_number=phone_number,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomerManager(models.Manager):
    def create_user(self,  phone_number, password=None):
        if not phone_number or len(phone_number) <= 0:
            raise ValueError("Phone field is required !")

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_customer=True)
        return queryset


class StaffManager(models.Manager):
    def create_user(self,  phone_number, password=None):
        if not phone_number or len(phone_number) <= 0:
            raise ValueError("Phone field is required !")

        user = self.model( phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_staff=True)
        return queryset