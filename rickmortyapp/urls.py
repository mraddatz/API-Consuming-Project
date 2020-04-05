from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^episode/(?P<episode_id>\d+)/$', views.episode, name='episode'),
    url(r'^character/(?P<character_id>\d+)/$', views.character, name='character'),
    url(r'^location/(?P<location_id>\d+)/$', views.location, name='location'),
    url(r'^search/$', views.search, name='search'),
]