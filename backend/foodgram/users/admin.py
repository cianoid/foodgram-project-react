from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = (
        'email', 'is_staff', 'is_active',
    )
    list_filter = (
        'email', 'is_staff', 'is_active',
    )
    fieldsets = (
        (None,
         {'fields': (
             'username', 'first_name', 'last_name',
             'email', 'password',
         )}),
        ('Permissions',
         {'fields': ('is_staff', 'is_active',
                     )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'first_name', 'last_name',
                'email', 'password1', 'password2',
                'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
