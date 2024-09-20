## hw/views.py
## description: write view functions to handle URL requests for the hw app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.
# def home(request):
#     '''Handle the main URL for the hw app.'''

#     response_text = f'''
#     <html>
#     <h1>Hello, world!</h1>
#     <p>This is our first django web application!</p>
#     <hr>
#     This page was generated at {time.ctime()}.
#     </html>
#     '''
#     # create and return a response to the client:
#     return HttpResponse(response_text)

from django.shortcuts import redirect, render
from django.http import HttpResponse
from random import randrange


images = ["../static/john-lennon-the-beatles.gif", "../static/john-lennon-eyebrows.gif", "../static/john-lennon-funny.gif"]
quotes = ["\"Everything will be okay in the end. If it's not okay, it's not the end.\"", "\"Reality leaves a lot to the imagination.\"", "\"A dream you dream alone is only a dream. A dream you dream together is reality.\""]

def quote(request):
    i = randrange(3)

    context = {
        "image_link": images[i],
        "quote": quotes[i],
        "person": "John Lennon",
    }
def quote(request):
    i = randrange(3)

    context = {
        "current_time" : time.ctime(),
        "image_link": images[i],
        "quote": quotes[i],
        "person": "John Lennon",
    }
    return render(request, "quotes/quote.html", context)

def show_all(request):
    context = {
        "current_time" : time.ctime(),
        "images": images,
        "quotes": quotes
    }
    return render(request, "quotes/show_all.html", context)

def about(request):
    context = {
        "current_time" : time.ctime(),
    }
    return render(request, "quotes/about.html", context)