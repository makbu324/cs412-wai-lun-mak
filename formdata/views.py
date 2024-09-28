from django.shortcuts import render, redirect

# Create your views here.
def show_form(request):
    template_name = "formdata/form.html"
    return render(request, template_name)

def submit(request):
    template_name = 'formdata/confirmation.html'
    if request.POST:
        print(request.POST)
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']
        context = {
            'name': name,
            'favorite_color': favorite_color
        }
        return render(request, template_name, context) 
    template_name = "formdata/form.html"
    return redirect("show_form")