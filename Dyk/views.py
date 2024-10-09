from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'app/home.html'

class ProfilePageView(TemplateView):
    template_name = 'app/profile.html'
    
class SettingsPageView(TemplateView):
    template_name = 'app/settings.html'