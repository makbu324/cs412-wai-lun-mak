import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
import requests
from .models import *
# from bs4 import BeautifulSoup



def get_content(product):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    #https://tabs.ultimate-guitar.com/tab/passenger/let-her-go-chords-1235202
    # https://jguitar.com/chordsearch?chordsearch=
    # f'https://www.ultimate-guitar.com/search.php?search_type=title&value={product}'
    html_content = session.get('https://www.google.com/search?q=site%3Avimeo.com+virtual+isanity&ia=web').text
    return html_content.replace("&quot", "")


def home(request):
    product_info_list = []
    html_content = ""

    if 'product' in request.GET:
        product = request.GET.get('product')
        html_content = get_content(product)

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        audio_file = request.FILES.get('recorded_audio')
        Audio.objects.create(audio=audio_file)
        
    
    return render( request, "guitar_app/home.html", {'test': html_content})

