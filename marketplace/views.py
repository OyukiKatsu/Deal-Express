from django.shortcuts import render,redirect,get_object_or_404
from . import forms
from core import models
from django.urls import reverse_lazy

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
# Create your views here.


class index(TemplateView): 
    template_name='marketplace/index.html'


