from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("register/",register),
    path("login/",login_view),
    path("logout/",logout_view),
    path("user-profile/",user_profile_view),
    path('accounts/', include('allauth.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)