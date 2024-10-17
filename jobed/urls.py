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
    path('user-data/', get_user_data, name='user_data'),
    path('user-profile/', user_profile, name='user-profile'),
    path('check-login/', check_login_status, name='check-login'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)