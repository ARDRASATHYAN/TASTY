from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse


# Create your views here.

def login(request):
    print(request)
    if request.method=="POST":
        print("hi")
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            print("hello6")
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'invalid details')
            return redirect('accounts')
    else:
        print('hjjj')
        return render(request,'register.html')


def logout(request):
    auth.logout(request)
    return render(request,'logout.html')



def register(request):
    if request.method == "POST":
        print('ardra')
        # firstname = request.POST['firstname']
        # lastname = request.POST['lastname']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        email = request.POST['email']

        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username taken")
                return redirect('accounts')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email taken")
                return redirect('accounts')
            else:
                user = User.objects.create_user(username=username,password=password, email=email)
                user.save()
                print("User created")
                return redirect('login')
        else:
            print("Password incorrect")
            messages.info(request, "Password incorrect")
            return redirect('accounts')
    else:
        return render(request, "register.html")

