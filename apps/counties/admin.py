from django.contrib import admin
from .models import County, SubCounty, Ward, Constituency


class SubCountyInline(admin.TabularInline):
    model = SubCounty
    extra = 0


class WardInline(admin.TabularInline):
    model = Ward
    extra = 0


class ConstituencyInline(admin.TabularInline):
    model = Constituency
    extra = 0


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'capital', 'governor', 'population', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'capital']
    inlines = [SubCountyInline, ConstituencyInline]


@admin.register(SubCounty)
class SubCountyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'county']
    list_filter = ['county']
    search_fields = ['name']
    inlines = [WardInline]


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'sub_county']
    list_filter = ['sub_county__county']
    search_fields = ['name']


@admin.register(Constituency)
class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'county', 'mp_name']
    list_filter = ['county']
    search_fields = ['name']
