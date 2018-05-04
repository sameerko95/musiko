from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('post_content', views.post_content, name='post')
]