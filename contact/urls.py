from . import views
from django.urls import path

urlpatterns = [
    path('', views.reach_out, name='contact'),
]