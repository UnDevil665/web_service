"""ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include, re_path
import qa.views


urlpatterns = [
    path('', qa.views.get_main_page),
    path(r'admin/', admin.site.urls, name='admin'),
    path(r'auth/', include('django.contrib.auth.urls')),
    path(r'signup/', qa.views.signup, name='signup'),
    path(r'main/', qa.views.get_main_page, name='main'),
    path(r'account/', qa.views.get_account_page, name='account'),
    path(r'account/request/', qa.views.send_request, name='send_request'),  # TODO
    path(r'account/answer/', qa.views.send_message, name='send_message'),
]
