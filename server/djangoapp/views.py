""" Djangoapp Views"""
# from datetime import datetime
import logging
# import json
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
#from django.contrib import messages

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    """ About View"""
    context = {}
    if request.method == "GET":
        about_view = render(request, 'djangoapp/about.html', context)
    return about_view

# Create a `contact` view to return a static contact page


def contact(request):
    """ Contact View """
    context = {}
    if request.method == "GET":
        contact_view = render(request, 'djangoapp/contact.html', context)
    return contact_view


# Create a `login_request` view to handle sign in request


def login_request(request):
    """ Login Request """
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            login_view = redirect('djangoapp:index')
        else:
            context['message'] = ("Please enter correct username and password!")
            login_view = render(request, 'djangoapp/index.html', context)
    else:
        login_view = render(request, 'djangoapp/index.html', context)
    return login_view

# Create a `logout_request` view to handle sign out request


def logout_request(request):
    """ Logout Request """
    logout(request)
    logout_view = redirect("djangoapp:index")
    return logout_view

# Create a `registration_request` view to handle sign up request


def registration_request(request):
    """ Registration Request """
    context = {}
    # if request.method == 'GET':
    #     return render(request, 'djangoapp/registration.html', context)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        if User.objects.filter(username=username).exists():
            context['message'] = ("Username {} already exists!".format(username))
            register_view = render(request, 'djangoapp/registration.html', context)
        else:
            user = User.objects.create_user(
            username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            register_view = redirect("djangoapp:index")
    elif request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    return register_view

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    """ Dealerships View """
    context = {}
    if request.method == "GET":
        get_dealerships_view = render(request, 'djangoapp/index.html', context)
    return get_dealerships_view

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
