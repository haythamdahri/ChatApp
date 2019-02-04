# chat/urls.py
from django.conf.urls import url
from django.urls import re_path, path

from . import views

app_name = "MSG"

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^chatters/?$', views.chatters, name="chatters"),
    re_path(r'^messages/(?P<user_id>\d+)/?$', views.messages, name="messages"),
    re_path(r'^unread_messages/(?P<user_id>\d+)/?$', views.unread_messages, name="unread_messages"),
    re_path(r'^read_messages/(?P<user_id>\d+)/?$', views.read_messages, name="read_messages"),
    path('disconnect/', views.disconnect, name="disconnect")
    #url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]