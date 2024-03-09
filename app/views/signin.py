from django.shortcuts import render,redirect
from app.models import User

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# Create your views here.

def signin(request):
    
    username="anurag"
    password="anurag"
    try:
        users=User.objects.get(username=username)  
        if users.delete == False:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dasboard')
            else:
                messages.info(request, 'Check Password !')
                return redirect('signin')
        else:
            messages.info(request, 'User Not Register ')
            return redirect('signup')
    except:
        messages.info(request, 'User Not Register !')
        return redirect('/')



# @login_required(login_url='signin')
# def signout(request):
#     logout(request)
#     # messages.info(request, "Three credits remain in your account.")
#     return redirect('home')