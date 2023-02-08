from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# from course.forms import AddStudentForm, EditStudentForm
from course.models import User, Teacher, Course, Category, Student
from course.forms import AddStudentForm, EditStudentForm


def admin_home(request):
    return render(request, "hod_templates/home_content.html")

# ----- TEACHERS CRUD -----


def add_teacher(request):
    return render(request, "hod_templates/add_teacher_template.html")


def add_teacher_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = User.objects.create_user(username=username, password=password,email=email, last_name=last_name, first_name=first_name, user_type=2)
            user.teacher.address = address
            user.save()
            messages.success(request, "Successfully Added Teacher")
            return HttpResponseRedirect("/add_teacher")
        except:
            messages.error(request, "Failed to Add Teacher")
            return HttpResponseRedirect("/add_teacher")


def manage_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, "hod_templates/manage_teachers_template.html", {"teachers": teachers})


def edit_teacher(request, teacher_id):
    teacher = Teacher.objects.get(user=teacher_id)
    return render(request, "hod_templates/edit_teacher_template.html", {"teacher": teacher, "id": teacher_id})


def edit_teacher_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        teacher_id = request.POST.get("teacher_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")

        try:
            user = User.objects.get(id=teacher_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            teacher_model = Teacher.objects.get(user=teacher_id)
            teacher_model.address = address
            teacher_model.save()
            messages.success(request, "Successfully Edited Teacher")
            return HttpResponseRedirect(reverse("edit_teacher", kwargs={"teacher_id": teacher_id}))
        except:
            messages.error(request, "Failed to Edit Teacher")
            return HttpResponseRedirect(reverse("edit_teacher", kwargs={"teacher_id": teacher_id}))


def delete_teacher(request, teacher_id):

    teacher = User.objects.get(id=teacher_id)
    if request.method == "POST":
        teacher.delete()
        return HttpResponseRedirect(reverse("manage_teachers"))

    context = {'item': teacher}
    return render(request, "hod_templates/delete_teacher_template.html", context)

# ----- TEACHERS CRUD end -----


# ----- STUDENTS CRUD -----


def add_student(request):
    form = AddStudentForm()
    context = {"form": form}
    return render(request, "hod_templates/add_student_template.html", context)


def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Aloowed")
    else:
        form = AddStudentForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            gender = form.cleaned_data['gender']

            try:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
                user.student.address = address
                user.student.gender = gender
                user.save()
                messages.success(request, "Student Added Successfully!")
                return HttpResponseRedirect("/add_student")
            except:
                messages.error(request, "Failed to Add Student!")
            return HttpResponseRedirect("/add_student")
        
        else:
            context = {"form": form}
            form=AddStudentForm(request.POST)
            return render(request, "hod_templates/add_student_template.html", context)
        
def manage_students(request):
    students = Student.objects.all()
    return render(request, "hod_templates/manage_students_template.html", {"students": students})

def edit_student(request, teacher_id):
    teacher = Teacher.objects.get(user=teacher_id)
    return render(request, "hod_templates/edit_teacher_template.html", {"teacher": teacher, "id": teacher_id})

def delete_student(request, student_id):

    student = User.objects.get(id=student_id)
    if request.method == "POST":
        student.delete()
        return HttpResponseRedirect(reverse("manage_students"))

    context = {'item': student}
    return render(request, "hod_templates/delete_student_template.html", context)

# ----- STUDENTS CRUD end -----


# ----- CATEGORIES CRUD -----


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
            messages.error(request,"Category Already Exist")
            return HttpResponseRedirect("add_category")
        
def manage_categories(request):
    category=Category.objects.all()
    return render(request,"hod_templates/manage_categories_template.html",{"category":category})

def edit_category(request, category_id):
    category=Category.objects.get(id=category_id)
    return render(request,"hod_templates/edit_category_template.html",{"category":category, "id":category_id})

def edit_category_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        category_id=request.POST.get("category_id")
        category_name=request.POST.get("category")

        try:
            category=Category.objects.get(id=category_id)
            category.category_name=category_name
            category.save()
            messages.success(request, "Successfully Edited Category")
            return HttpResponseRedirect(reverse("edit_category", kwargs={"category_id":category_id}))
        except:
            messages.error(request, "Failed to Edit Category")
            return HttpResponseRedirect(reverse("edit_category", kwargs={"category_id":category_id}))
        

def delete_category(request, category_id):
    
    category=Category.objects.get(id=category_id)
    if request.method == "POST":
        category.delete()
        return HttpResponseRedirect(reverse("manage_categories"))

    context = {'item':category}
    return render(request,"hod_templates/delete_category_template.html", context)


# ----- CATEGORIES CRUD end -----
