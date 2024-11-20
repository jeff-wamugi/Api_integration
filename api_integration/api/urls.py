from django.urls import path
from .views import SendSMSView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send-sms/', SendSMSView.as_view(), name='send_sms'),
]