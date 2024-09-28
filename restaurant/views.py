from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
import random
from datetime import datetime, timedelta
import pytz

def main(request):
    context = {}
    return render(request, "restaurant/main.html", context)

def order(request):
    list = ["Creeper Cake", "Wolve Sweet Waffles", "Panda Bamboo Boba Tea", "Trader Llama Tarts"]
    context = {
        "daily_special": list[random.randint(0, 3)]
    }
    return render(request, "restaurant/order.html", context)


def confirmation(request):
    if request.POST:
        print(request.POST)
        name = request.POST['name']
        email = request.POST['your_email']
        phone = request.POST['your_phone']

        food_list = request.POST.getlist('food_list')

        daily_special = request.POST.getlist('daily_special')

        sugar_cookie = request.POST.getlist('sugar_cookie')
        extra_milk = request.POST.getlist('extra_milk')
        sugar_pie = request.POST.getlist('sugar_pie')
        extra_pumpkin = request.POST.getlist('extra_pumpkin')
        comments = request.POST.getlist('comments')

        emeralds_required = 0

        item_list = [] 

        # Time to calculate!

        if ("carrot" in food_list):
            item_list.append("Carrot: + 5")
            emeralds_required += 5

        if ("cake" in food_list):
            item_list.append("Cake: + 10")
            emeralds_required += 10

        if ("cookie" in food_list):
            item_list.append("Cookie: + 7")
            emeralds_required += 7 
            if (len(sugar_cookie) > 1):
                item_list.append("Extra Cookie Sugar: + 1")
                emeralds_required += 1
            if (len(extra_milk) > 1):
                item_list.append("Extra Cookie Milk: + 2")
                emeralds_required += 2

        if ("pumpkin_pie" in food_list):
            item_list.append("Pumpkin Pie: + 9")
            emeralds_required += 9 
            if (len(sugar_pie) > 1):
                item_list.append("Extra Pumpkin Sugar: + 1")
                emeralds_required += 1
            if (len(extra_pumpkin) > 1):
                item_list.append("Extra Pumpkin Sugar: + 5")
                emeralds_required += 5

        if (len(daily_special) > 1):
            item_list.append("Daily Special: + 15")
            emeralds_required += 15


        # Get the current time in UTC
        now_utc = datetime.now(pytz.utc)

        # Convert to Eastern Time
        eastern_tz = pytz.timezone('US/Eastern') 
        now_eastern = now_utc.astimezone(eastern_tz) + timedelta(minutes=random.randint(30, 60 )) 

        # Format the output
        formatted_time = now_eastern.strftime("%Y-%m-%d %H:%M ")


        when_it_will_be_ready = formatted_time

        context = {
            "name": name,
            "email": email,
            "phone": phone,

            "item_list": item_list,
            
            "comments": comments[0],

            "emeralds_required": emeralds_required,

            "when_it_will_be_ready": when_it_will_be_ready
        }

        return render(request, 'restaurant/confirmation.html', context) 
    
    
    ######
    
    #if reload (same as order)
    list = ["Creeper Cake", "Wolve Sweet Waffles", "Panda Bamboo Boba Tea", "Trader Llama Tarts"]
    context = {
        "daily_special": list[random.randint(0, 3)]
    }
    return render(request, "restaurant/order.html", context)