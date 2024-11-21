from django.urls import path
from .views import SendNotificationsView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send-notifications/', SendNotificationsView.as_view(), name='send_notifications'),
]