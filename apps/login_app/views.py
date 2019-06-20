from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt


# Create your views here.
def index(request):
    # return render(request,'index.html')
    return render(request,'index.html')

def register(request):
    print("Errors include:")       
    errors = User.objects.register_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.warning(request,value)
        return redirect('/')
    else:
        hashedpw = bcrypt.hashpw(request.POST["pw"].encode(),bcrypt.gensalt())
        print(hashedpw)
        User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email = request.POST["email"],password = hashedpw)
        request.session["id"]= User.objects.last().id
        return redirect('/welcome')
    
def success(request):
    print('in success')
    if not "id" in request.session:
        return redirect('/')
    else:
        print(request.session["id"])
        context={
            'user': User.objects.get(id=request.session["id"])
        }
        return render(request,'home.html',context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        request.session["id"] = User.objects.get(email = request.POST["email"]).id
    return redirect('/welcome')

def logout(request):
    del request.session["id"]
    return redirect('/')