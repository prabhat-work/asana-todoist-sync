from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.req, name='payload'),
    path('payload/', views.handle_payload,name='handle_payload')
]