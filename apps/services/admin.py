from django.contrib import admin
from .models import Service, ServiceCategory, ConstitutionalFunction, EligibilityRule, RequiredDocument


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'ministry', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name']
    inlines = [ServiceInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'ministry', 'constitutional_function', 'fee_kes', 'is_popular', 'is_active', 'order']
    list_filter = ['is_active', 'is_popular', 'category', 'ministry', 'constitutional_function']
    search_fields = ['name', 'description', 'slug']
    filter_horizontal = ['eligibility_rules', 'required_documents', 'counties']


@admin.register(ConstitutionalFunction)
class ConstitutionalFunctionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'mandate_ref', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering = ['order', 'name']


@admin.register(EligibilityRule)
class EligibilityRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_age', 'max_age', 'kenyan_citizen_only']
    search_fields = ['name']


@admin.register(RequiredDocument)
class RequiredDocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'document_type', 'is_mandatory']
    list_filter = ['document_type', 'is_mandatory']
    search_fields = ['name']
