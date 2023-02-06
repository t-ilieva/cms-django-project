from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

#from course.forms import AddStudentForm, EditStudentForm
from course.models import User, Teacher, Course, Category, Student


def admin_home(request):
    return render(request, "hod_templates/home_content.html")

def add_teachers(request):
    return render(request, "hod_templates/add_teachers_template.html")

def add_teachers_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=User.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.teacher.address=address
            user.save()
            messages.success(request,"Successfully Added Teacher")
            return HttpResponseRedirect("/add_teachers")
        except:
            messages.error(request,"Failed to Add Teacher")
            return HttpResponseRedirect("/add_teachers")