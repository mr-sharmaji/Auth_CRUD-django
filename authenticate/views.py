from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from .forms import SignUpForm,EditProfileForm
# Create your views here.

def home(request):
    return render(request,'authenticate/home.html',{})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request,("Logged In successfully"))
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.success(request,("Error Logging In - Please Try Again"))
            return redirect('login')
    else:
        return render(request,'authenticate/login.html',{})

@login_required(login_url='/')
def logout_user(request):
    logout(request)
    # Redirect to a success page.
    messages.success(request,("Logged Out Successfully!"))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request,user)
            messages.success(request,("You have registered successfully"))
            return redirect('home')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request,'authenticate/register.html',context)

@login_required(login_url='/')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,("You have edited successfully"))
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
    context = {'form': form}
    return render(request,'authenticate/edit_profile.html',context)
    
@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,("You have edited successfully"))
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request,'authenticate/change_password.html',context)
