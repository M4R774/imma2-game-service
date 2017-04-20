"""imma2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from gameservice import views
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as auth_views

admin.autodiscover()

# from gameservice import models
# from django.conf.urls import include
# from django.conf import settings
# from . import views as core_views
# from gameservice import usermanagement
# from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^register/$', views.registerUser, name='register'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^addgame/$', views.addgame, name='addgame'),
    url(r'^buygame/(?P<gameid>[0-99]+)/$', views.buyGame, name='buygame'),
    url(r'^$', views.mainPage, name='mainpage'),

]
