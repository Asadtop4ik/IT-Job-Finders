from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    model = User
    form = UserChangeForm
    add_form = UserCreationForm
    ordering = ['-createdAt']
    list_display = ('phone', 'name', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')
    search_fields = ('phone', 'name', 'role')
    readonly_fields = ('createdAt', 'updatedAt')

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('createdAt', 'updatedAt')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name', 'password1', 'password2', 'role', 'is_staff', 'is_superuser', 'is_active')}
         ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created, set the password
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


# Register the UserAdmin
admin.site.register(User, UserAdmin)
