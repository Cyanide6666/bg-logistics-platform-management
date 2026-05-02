from django.contrib import admin
from django.urls import path, include
from web_app import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('panel/', include('web_app.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='home.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
]