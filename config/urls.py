from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

api_v1 = [
    path('auth/', include('apps.accounts.urls.api')),
    path('accounts/', include('apps.accounts.urls.api')),
    path('counties/', include('apps.counties.urls.api')),
    path('ministries/', include('apps.ministries.urls.api')),
    path('services/', include('apps.services.urls.api')),
    path('applications/', include('apps.applications.urls.api')),
    path('workflow/', include('apps.workflow.urls.api')),
    path('appointments/', include('apps.appointments.urls.api')),
    path('documents/', include('apps.documents.urls.api')),
    path('verification/', include('apps.verification.urls.api')),
    path('licenses/', include('apps.licenses.urls.api')),
    path('land/', include('apps.land.urls.api')),
    path('immigration/', include('apps.immigration.urls.api')),
    path('transport/', include('apps.transport.urls.api')),
    path('health/', include('apps.health.urls.api')),
    path('education/', include('apps.education.urls.api')),
    path('judiciary/', include('apps.judiciary.urls.api')),
    path('taxes/', include('apps.taxes.urls.api')),
    path('civil-registry/', include('apps.civil_registry.urls.api')),
    path('elections/', include('apps.elections.urls.api')),
    path('procurement/', include('apps.procurement.urls.api')),
    path('payments/', include('apps.payments.urls.api')),
    path('notifications/', include('apps.notifications.urls.api')),
    path('messaging/', include('apps.messaging.urls.api')),
    path('feedback/', include('apps.feedback.urls.api')),
    path('analytics/', include('apps.analytics.urls.api')),
    path('reports/', include('apps.reports.urls.api')),
    path('audit/', include('apps.audit.urls.api')),
    path('search/', include('apps.search.urls.api')),
    path('gateway/', include('apps.api_gateway.urls.api')),
    path('emergency/', include('apps.emergency.urls.api')),
    path('public-participation/', include('apps.public_participation.urls.api')),
    path('developer/', include('apps.developer_portal.urls.api')),
    path('integration/', include('apps.integration.urls.api')),
    path('news/', include('apps.news.urls.api')),
    path('legislature/', include('apps.legislature.urls.api')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1)),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', include('apps.accounts.urls.web')),
    path('onboarding/', include('apps.onboarding.urls.web')),
    path('services/', include('apps.services.urls.web')),
    path('ministries/', include('apps.ministries.urls.web')),
    path('counties/', include('apps.counties.urls.web')),
    path('applications/', include('apps.applications.urls.web')),
    path('appointments/', include('apps.appointments.urls.web')),
    path('documents/', include('apps.documents.urls.web')),
    path('civil-registry/', include('apps.civil_registry.urls.web')),
    path('immigration/', include('apps.immigration.urls.web')),
    path('land/', include('apps.land.urls.web')),
    path('transport/', include('apps.transport.urls.web')),
    path('health/', include('apps.health.urls.web')),
    path('education/', include('apps.education.urls.web')),
    path('taxes/', include('apps.taxes.urls.web')),
    path('judiciary/', include('apps.judiciary.urls.web')),
    path('licenses/', include('apps.licenses.urls.web')),
    path('procurement/', include('apps.procurement.urls.web')),
    path('participation/', include('apps.public_participation.urls.web')),
    path('reports/', include('apps.reports.urls.web')),
    path('constitution/', include('apps.constitution.urls.web')),
    path('legislature/', include('apps.legislature.urls.web')),
    path('authorities/', include('apps.authorities.urls.web')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
        urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))
    except ImportError:
        pass
