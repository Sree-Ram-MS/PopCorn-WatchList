from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView,View
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import UserForm,UserLoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages



class signinpage(CreateView):
    template_name = "signin.html"
    form_class=UserForm
    model=User
    success_url=reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "You have successfully signed in! \n You Can Login Now")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)

        if 'username' in form.errors:
            messages.error(self.request, "Username already exists. Please choose a different username.")

        return response


class loginpage(FormView):
    template_name = "login.html"
    form_class = UserLoginForm
    def post(self,req,*args,**kwargs):
        form_data = UserLoginForm(data=req.POST)
        if form_data.is_valid():
            un=form_data.cleaned_data.get("username")
            pw=form_data.cleaned_data.get("password")
            auth=authenticate(req,username=un,password=pw)
            if auth:
                print(auth.username , "is logined")
                login(req,auth)
                messages.success(req,f"You logined as {auth.username}")
                return redirect("First")
            else:
                messages.error(req,"Something went wrong , Please try again")
                return redirect("login")
        else:
            return render(req,"login.html",{"form":form_data})
        

class LogOut(View):
    def get(self,req):
        logout(req)
        return redirect('login')





