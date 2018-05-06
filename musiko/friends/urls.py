from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_friends, name='friends'),
    path('add_friend', views.add_friend, name='add_friend'),
    path('change_seen', views.change_seen, name='change_seen')
]