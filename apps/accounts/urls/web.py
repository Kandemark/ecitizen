from django.urls import path
from ..views import web

urlpatterns = [
    path('', web.dashboard, name='dashboard'),
    path('login/', web.login_view, name='login'),

    path('logout/', web.logout_view, name='logout'),
    path('profile/', web.profile_view, name='profile'),
    path('account-security/', web.account_security, name='account_security'),
    path('privacy-settings/', web.privacy_settings, name='privacy_settings'),
    path('user-roles/', web.user_roles_access, name='user_roles_access'),
    path('about/', web.about_view, name='about'),
    path('contact/', web.contact_view, name='contact'),
    path('applications/', web.applications_list, name='applications_list'),
    path('payments/', web.payments_list, name='payments_list'),
    path('services/', web.services_list, name='services_list'),
    path('notifications/latest/', web.latest_notifications, name='latest_notifications'),
]
