from django.contrib import admin
from .models import User, UserConfirmation


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone_number', 'auth_type', 'auth_status']

class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'verify_type']


admin.site.register(User, UserAdmin)

admin.site.register(UserConfirmation, UserConfirmationAdmin)
