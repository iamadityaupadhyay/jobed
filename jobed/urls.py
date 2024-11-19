from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("register/",register),
    path("login/",login_view),
    path("google-login/",google_login),
    path("logout/",logout_view),
    path('accounts/', include('allauth.urls')),
    path('get_companies/',get_companies),
    path('get_company_by_id/<int:id>',get_company_by_id),
    path('get_job/',get_job),
    path('get_job_by_id/<int:id>',get_job_by_id),
    path('applied_jobs/',applied_jobs),
    path("profile/<int:pk>",profile),
    path("profile-update/<int:id>",profile_update),
    path("get_profiles",get_profiles),
    path("get_profile_by_id/<int:id>",get_profile_by_id),
    path("skill_update/<int:id>",skill_update),
    path("skill_get/<int:id>",skill_get),
    path("about_update/<int:id>",about_update),
    path("about_get/<int:id>",about_get),
    path("education_update/<int:id>",education_update),
    path("experience_update/<int:id>",experience_update)
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)