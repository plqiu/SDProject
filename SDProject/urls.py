"""SDProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Single_data_upload_alarm_system import views as info_views
from fish import views as fishhome
from data_analysis import views as data_analysis
urlpatterns = [
    url(r'^$',info_views.home),
    url(r'^search/',info_views.search),
    url(r'^load',info_views.load),
    url(r'^readconf/',info_views.readconf),
    url(r'^modifyconf/',info_views.modifyconf),
    url(r'^modify/',info_views.modify),
    url(r'^admin/', admin.site.urls),
    url(r'fishhome/$', fishhome.fish_home),
    url(r'data_analysis/$', data_analysis.home),
    url(r'fishhome/get_data/$', fishhome.get_data),
    url(r'fishhome/set_data/$', fishhome.set_data),
]
