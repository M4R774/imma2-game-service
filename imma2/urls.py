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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()
from gameservice import views
#from gameservice import usermanagement
#from gameservice import models
#from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]


urlpatterns = [
    url(r'^pong/', "gameservice.usermanagement.pong"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^store/(?P<game_name>\w+)/?$', views.store_view),
    url(r'^store/', "gameservice.shop.shop"),
    url(r'^buy_item/(?P<game_name>\w+)/?$', "gameservice.shop.buy_item"),
    url(r'^register/', "gameservice.usermanagement.register"),
    url(r'^register_developer/', "gameservice.usermanagement.dev_register"),
    url(r'^account/', "gameservice.usermanagement.account"),
    url(r'^login/', "gameservice.usermanagement.login"),
    url(r'^gamelist/?$', views.game_list),
    url(r'^veryscore/', "gameservice.usermanagement.new_highscore"),
    url(r'^verysave/', "gameservice.usermanagement.new_save"),
    url(r'^veryload/', "gameservice.usermanagement.load_game"),
    url(r'^payment/success/(?P<game_name>\w+)/', "gameservice.usermanagement.get_owned"),
    url(r'^verification/', "gameservice.usermanagement.verification"),
    url(r'^gamelist/dev/', views.dev_game_list),
    url(r'^scores/(?P<game_name>\w+)/?$', views.global_highscore),
    url(r'^dev/remove/(?P<game_name>\w+)/?$', "gameservice.usermanagement.remove_game"),
    url(r'^import/', "gameservice.usermanagement.game_registration"),
    url(r'^game/(?P<game_name>\w+)/?$', "gameservice.usermanagement.play_game"),
    url(r'^$', "gameservice.usermanagement.home"),
    url(r'^logout/', "gameservice.usermanagement.logout"),
    #url(r'^game/(?P<game_id>\d+)/?$', "gameservice.usermanagement.play_game"),

]