"""superpool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import notifications.urls
from chat.views import index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('',include('pool.urls')),
    path('groups/',include('groups.urls')),
    path('services/', include('services.urls')),
    path('chat/', include('chat.urls')),
    path('notification/', include('notification.urls')),
    path('notifications/', include(notifications.urls, namespace='notifications')),
    path('api/', include('api.urls')),
    path('activities/', include('activities.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('location/', include('location.urls'))
]
