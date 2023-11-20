from typing import Any
from django.shortcuts import render,redirect
from crm.forms import  EmployeModelForm,LoginForm,RegistrationForm
from django.views.generic import View
from crm.models import Employees
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator


def signin_required(fn):
    def wrapper(request,*args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args, **kwargs)
    return wrapper



# Create your views here.
@method_decorator(signin_required,name="dispatch")
class EmployecreateView(View):
    def get(self,request,*args,**kwargs):
         form=EmployeModelForm()
         return render(request,"emp_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
         form=EmployeModelForm(request.POST,files=request.FILES)
         if form.is_valid():
              form.save()
              messages.success(request,"employee has been created")
          #     Employees.objects.create(**form.cleaned_data)
              print("created")
              return render(request,"emp_add.html",{"form":form})
         else:
              messages.error(request,"failed to create employee")
              return render(request,"emp_add.html",{"form":form})
         
@method_decorator(signin_required,name="dispatch")        
class EmployeeslistView(View):
    def get(self,request,*args, **kwargs):
      if request.user.is_authenticated:
        qs=Employees.objects.all()
        department=Employees.objects.all().values_list("department",flat=True).distinct()
        print(department)

        if "department" in request.GET:
                  dept=request.GET.get("department")
                  qs=qs.filter(department__iexact=dept)

        return render(request,"list.html",{"data":qs,"department":department})
      else:
               messages.error(request,"invalid session")
               return redirect("signin")

        
    def post(self,request,*args, **kwargs):
        name=request.POST.get("box")
        qs=Employees.objects.filter(name__icontains=name)
        return render(request,"list.html",{"data":qs})
    
@method_decorator(signin_required,name="dispatch")
class EmployedetailView(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        return render(request,"detail.html",{"data":qs})
    
@method_decorator(signin_required,name="dispatch")
class EmployeedeleteView(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        Employees.objects.get(id=id).delete()
        messages.success(request,"Deleted")
        return redirect ("emp-list")
    
@method_decorator(signin_required,name="dispatch")
class EmployeeupdateView(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)
        form=EmployeModelForm(instance=obj)
        return render(request,"edit.html",{"form":form})
    def post(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)
        form=EmployeModelForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Employees Details has been Updated")
            return redirect("emp-list")
        else:
            messages.error(request,"Failed to Update")
            return render(request, "edit.html",{"form":form})
        

        
class SignupView(View):
    def get(self,request,*args, **kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args, **kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            print("saved")
            messages.success(request,"account has been created")
            return render(request,"register.html",{"form":form})
        else:
            print("failed")
            messages.error(request,"failed to create account")
            return render(request,"register.html",{"form":form})

class SigninView(View):
    def get(self,request,*args, **kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            print(request.user,"before")
            user_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(user_name,pwd)
            user_obj=authenticate(request,username=user_name,password=pwd)
            if user_obj:
                print("valid")
                login(request,user_obj)
            
                return redirect("emp-list")
            # else:
            messages.error(request,"invalid credential")
            return render(request,"login.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
