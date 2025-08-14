from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import login, authenticate, logout


def home(request):
    return render(request, 'home.html')

def gallery(request):
    return render(request, 'gallery.html')


