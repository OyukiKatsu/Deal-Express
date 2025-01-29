from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.


class index(LoginRequiredMixin,TemplateView): 
    template_name='marketplace_empresa/index_empresa.html'
    