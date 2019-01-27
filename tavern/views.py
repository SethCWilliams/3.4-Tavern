from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Lunch, Location

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        lunch = Lunch.objects.all()

        context = {
            'lunch': lunch

        }
        return context

