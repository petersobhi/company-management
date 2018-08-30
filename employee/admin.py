from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Employee


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (EmployeeInline,)
    list_display = UserAdmin.list_display + ('company', 'team', 'company_admin')

    def company(self, obj):
        return obj.employee.company

    def team(self, obj):
        return obj.employee.team

    def company_admin(self, obj):
        return obj.employee.is_admin

    company_admin.boolean = True

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
