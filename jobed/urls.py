from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("register/",register),
    path("login/",login_view),
    path("logout/",logout_view),
    path('accounts/', include('allauth.urls')),
    path('user-data', get_user_data, name='user_data'),
    path('get_companies/',get_companies),
    path('get_company_by_id/<int:id>',get_company_by_id),
    path('get_job/',get_job),
    path('get_job_by_id/<int:id>',get_job_by_id),
    path('applied_jobs/',applied_jobs),
    path("profile/<int:pk>",profile)

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)