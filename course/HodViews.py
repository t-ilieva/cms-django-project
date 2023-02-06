from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

#from course.forms import AddStudentForm, EditStudentForm
from course.models import User, Teacher, Course, Category, Student


def admin_home(request):
    return render(request, "hod_templates/home_content.html")

def add_teacher(request):
    return render(request, "hod_templates/add_teacher_template.html")

def add_teacher_save(request):
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
            return HttpResponseRedirect("/add_teacher")
        except:
            messages.error(request,"Failed to Add Teacher")
            return HttpResponseRedirect("/add_teacher")
        
def manage_teachers(request):
    teachers=Teacher.objects.all()
    return render(request,"hod_templates/manage_teachers_template.html",{"teachers":teachers})

def edit_teacher(request, teacher_id):
    teacher=Teacher.objects.get(user=teacher_id)
    return render(request,"hod_templates/edit_teacher_template.html",{"teacher":teacher ,"id":teacher_id})

def edit_teacher_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        teacher_id=request.POST.get("teacher_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=User.objects.get(id=teacher_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            teacher_model=Teacher.objects.get(user=teacher_id)
            teacher_model.address=address
            teacher_model.save()
            messages.success(request,"Successfully Edited Teacher")
            return HttpResponseRedirect(reverse("edit_teacher", kwargs={"teacher_id":teacher_id}))
        except:
            messages.error(request,"Failed to Edit Teacher")
            return HttpResponseRedirect(reverse("edit_teacher", kwargs={"teacher_id":teacher_id}))
        
def add_category(request):
    return render(request,"hod_templates/add_category_template.html")

def add_category_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        category=request.POST.get("category")
        try:
            category_model=Category(category_name=category)
            category_model.save()
            messages.success(request,"Successfully Added Category")
            return HttpResponseRedirect("add_category")
        except:
            messages.error(request,"Failed To Add Category")
            return HttpResponseRedirect("add_category")