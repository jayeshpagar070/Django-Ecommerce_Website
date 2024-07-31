from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if password != confirmpassword:
            messages.warning(request, "Password is Not Matching")
            return render(request, 'authentication/signup.html')

        if User.objects.filter(username=email).exists():
            messages.info(request, "Email is taken")
            return render(request, 'authentication/signup.html')

        User.objects.create_user(username=email, email=email, password=password)
        messages.success(request, "Signup successful. Please login.")
        return redirect('/vogue_auth/login/')
    
    return render(request, "authentication/signup.html")


def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get("email")
        userpassword = request.POST.get("password")
        myuser = authenticate(username=username, password=userpassword)

        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, "authentication/login.html")

    return render(request, "authentication/login.html")


def handlelogout(request):
    logout(request)
    messages.info(request, "Logout Success")
    return render(request, "authentication/login.html")
