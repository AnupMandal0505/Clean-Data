from django.shortcuts import render,redirect
from app.models import User

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# Create your views here.

def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        try:
            users=User.objects.get(username=username)  
            try:
                user = authenticate(request, username=username, password=password)
                print(12)
                if user is not None:
                    login(request, user)
                    print(545)
                    return redirect('upload_csv')
                else:
                    messages.info(request, 'Check Password !')
                    return redirect('signin')
            except:
                print(78454)
                messages.info(request, 'User Not Register ')
                return redirect('signup')
        except:
            print(12)
            messages.info(request, 'User Not Register !')
            return redirect('signup')
    else:
        return render(request,'signin.html')


@login_required(login_url='signin')
def signout(request):
    logout(request)
    # messages.info(request, "Three credits remain in your account.")
    return redirect('/')