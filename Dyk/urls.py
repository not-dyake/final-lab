from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('Profile', ProfilePageView.as_view(), name='profile'),
    path('Settings', SettingsPageView.as_view(), name='settings'),
]