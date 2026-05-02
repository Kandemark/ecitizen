from django.contrib import admin
from .models import Ministry, Department, Division


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'website', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    inlines = [DepartmentInline]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'ministry', 'director', 'is_active']
    list_filter = ['ministry', 'is_active']
    search_fields = ['name']


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department']
    list_filter = ['department__ministry']
    search_fields = ['name']
