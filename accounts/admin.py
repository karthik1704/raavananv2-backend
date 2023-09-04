from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField

from .models import MyUser, Customer, Staff
# Register your models here.

class MyUserForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        region="FR",
        widget=PhoneNumberPrefixWidget(initial='IN', country_choices=[
                 ("IN", "India"),
                 ("FR", "France"),
            ],)
    )
    class Meta:
        model = MyUser
        fields = "__all__"
        read_only_fields = ("password",)
       

class MyUserAdmin(AuthUserAdmin):
    form = MyUserForm
    AuthUserAdmin.list_display =   ["phone_number", "created_at", "updated_at"]

    AuthUserAdmin.fieldsets = (
        (None, {"fields": ("username", "phone_number" ,"email", "password")}),
        ("Permissions", {"fields": ("is_staff",)}),
    )

   


admin.site.register(MyUser, AuthUserAdmin)
admin.site.register(Customer)
admin.site.register(Staff)
