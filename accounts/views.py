from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import View
from .forms import RegisterForm ,LoginForm
from django.contrib.auth import login,authenticate,logout

# Create your views here.
class Register(View):
    def get(self,request):
        form = RegisterForm()
        context  ={
            'form':form
        }
        return render(request,'register.html',context)
    def post(self,request):
        form  = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,f"Registered now login {user.username}")
            return redirect('login')
        else:
            context  ={
                'form':form
            }
            messages.error(request,"Form is not valid")
            return render(request,'register.html',context)
        
class Login(View):
    def get(self, request):
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "login successful")
                if user.is_staff or user.is_superuser:
                    return redirect('AdminDashboard')  # Use your admin dashboard URL name
                else:
                    return redirect('home')
            else:
                context = {'form': form}
                messages.error(request, "invalid Credentials")
                return render(request, 'login.html', context)
        else:
            context = {'form': form}
            messages.error(request, "Form is not valid")
            return render(request, 'login.html', context)
        
        
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('/')
    def post(self,request):
        logout(request)
        return redirect('/')



            