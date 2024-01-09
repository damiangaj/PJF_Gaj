from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    return render(request,"myapp/signin.html")

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['pass1']
        password2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        messages.success(request,"Your account has been successfully created.")
        return redirect('signin')

    return render(request, "myapp/signup.html")
def signin(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['pass']

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return render(request, "myapp/account.html")


        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')

    return render(request, "myapp/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged Out!")
    return redirect('home')