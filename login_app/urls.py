from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('trips/new', views.new),
    path('trips/create', views.create),
    path('trips/<int:id>', views.show),
    path('trips/edit/<int:id>', views.edit),
    path('trips/<int:id>/update', views.update),
    path('trips/<int:id>/join', views.join),
    path('trips/<int:id>/delete', views.delete),
    path('trips/<int:id>/cancel', views.cancel),
    path('logout', views.logout),
]