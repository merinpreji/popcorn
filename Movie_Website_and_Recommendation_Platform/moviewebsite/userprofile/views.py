from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
@login_required
def viewprofile(request):
    user = request.user
    return render(request, 'profile.html', {"user": user})


@login_required
def editprofile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username taken")
            return redirect("userprofile:editprofile")
        else:
            user.username = request.POST.get('username')
            user.save()
        return redirect("userprofile:viewprofile")
    return render(request, "editprofile.html")
