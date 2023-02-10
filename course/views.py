from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from course.EmailBackEnd import EmailBackEnd
from course.models import User


# Create your views here.
def showDemoPage(request):
    return render(request, "demo.html")


def showLoginPage(request):
    return render(request, "login_page.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            "email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("teacher_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email + " usertype : " + str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def signup_admin(request):
    return render(request, "signup_admin_template.html")


def do_admin_signup(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
        user = User.objects.create_user(username=username, password=password, email=email, user_type=1)
        user.save()
        messages.success(request, "Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request, "Failed to Create Admin")
        return HttpResponseRedirect(reverse("signup_admin"))


def signup_student(request):
    return render(request, "signup_student_template.html")


def do_student_signup(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    gender = request.POST.get("gender")

    try:
        user = User.objects.create_user(username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=3)
        user.student.address = address
        user.student.gender = gender
        user.save()
        messages.success(request, "Successfully Added Student")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request, "Failed to Add Student")
        return HttpResponseRedirect(reverse("signup_student"))


def signup_teacher(request):
    return render(request, "signup_teacher_template.html")


def do_teacher_signup(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")

    try:
        user = User.objects.create_user(username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=2)
        user.teacher.address = address
        user.save()
        messages.success(request, "Successfully Created Teacher")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request, "Failed to Create Teacher")
        return HttpResponseRedirect(reverse("signup_teacher"))
