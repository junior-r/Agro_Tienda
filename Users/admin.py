from django.contrib import admin
from Users.models import User
from Users.forms import SignUpForm


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email']
    search_fields = ['first_name', 'last_name', 'username']
    form = SignUpForm


admin.site.register(User, UserAdmin)
