from django.contrib import admin
from Users.models import User
from Users.forms import SignUpForm


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser']
    search_fields = ['first_name', 'last_name', 'username']
    form = SignUpForm


admin.site.register(User, UserAdmin)
