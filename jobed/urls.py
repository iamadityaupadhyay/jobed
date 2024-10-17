from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("register/",register),
    path("login/",login)
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)