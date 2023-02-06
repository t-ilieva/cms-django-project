from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

#from course.forms import AddStudentForm, EditStudentForm
from course.models import User, Teacher, Course, Category, Student


def admin_home(request):
    return render(request, "hod_templates/home_content.html")