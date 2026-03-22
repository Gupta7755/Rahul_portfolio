from django.urls import path
from . import views
urlpatterns = [
    path('', views.viewers, name='viewers'),
    path("admins/login/", views.admin_login, name="admin_login"),
    path("admins/logout/", views.admin_logout, name="admin_logout"),
    path("admins/logout/", views.admin_logout, name="admin_logout"),
    path('admins/', views.admins, name='admins'),
    path('download-resume/<int:pk>/', views.download_resume, name='download_resume'),
    path('api/request-otp/', views.request_otp, name='request_otp'),
    path('api/verify-contact/', views.verify_contact, name='verify_contact'),
]