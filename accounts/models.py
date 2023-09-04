from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator


from phonenumber_field.modelfields import PhoneNumberField


from .managers import CustomUserManager, CustomerManager, StaffManager

# Create your models here.
class MyUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    phone_number = PhoneNumberField(
        unique=True,
        null=False,
        blank=False,
        error_messages={
            "unique": "A user with that phone number already exists.",
        },
    )
    username = models.CharField(
        unique=True,
        validators=[username_validator],
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages={
            "unique": "A user already exists.",
        },
        null=True,
        blank=True
    )
    email =  models.EmailField(unique=True, null=True, blank=True,  error_messages={
            "unique": "A user with that email already exists.",
        }, 
        validators=[EmailValidator(message="Invalid Email")]
        )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    # is_sellar = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['phone_number',]

    objects = CustomUserManager()

    

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    # def get_email_field_name(self):
    #     return self.EMAIL_FIELD


    # def get_username(self):
    #     return self.username

    def __str__(self) -> str:
    
        return f'{self.phone_number}'


    # this methods are require to login super user from admin panel
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    # this methods are require to login super user from admin panel
    def has_module_perms(self, app_label):
        return self.is_superuser

class Customer(MyUser):

    class Meta:
        proxy = True,
    
    objects = CustomerManager()
    def save(self , *args , **kwargs):
        self.is_customer = True
        return super().save(*args , **kwargs)

class Staff(MyUser):

    class Meta:
        proxy = True,
    
    objects = StaffManager()
    def save(self , *args , **kwargs):
        self.is_staff = True
        return super().save(*args , **kwargs)