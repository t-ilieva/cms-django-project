from ast import Compare
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from course.models import User, Teacher, Course, Category, Student, Enrollment
from course.forms import AddStudentForm, EditStudentForm, AddCourseForm, EditCourseForm


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

def edit_student(request, student_id):
    request.session['student_id']=student_id
    student=Student.objects.get(user=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.user.email
    form.fields['first_name'].initial=student.user.first_name
    form.fields['last_name'].initial=student.user.last_name
    form.fields['username'].initial=student.user.username
    form.fields['address'].initial=student.address
    form.fields['gender'].initial=student.gender
    return render(request, "hod_templates/edit_student_template.html",{"form":form, "id":student_id, "username":student.user.username})

def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id == None:
            return HttpResponseRedirect(reverse("manage_students"))

        form = EditStudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            gender = form.cleaned_data["gender"]

            try:
                user=User.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Student.objects.get(user=student_id)
                student.address=address
                student.gender=gender
                student.save()

                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Student.objects.get(user=student_id)
            return render(request,"hod_templates/edit_student_template.html",{"form":form,"id":student_id,"username":student.user.username})


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



# ----- COURSES CRUD -----

def add_course(request):
    form = AddCourseForm()
    context = {"form": form}
    return render(request, "hod_templates/add_course_template.html", context)


def add_course_save(request):
        
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddCourseForm(request.POST)
        if form.is_valid():
            course_name=form.cleaned_data["course_name"]
            course_description=form.cleaned_data["course_description"]
            category_id=form.cleaned_data["category"]
            teacher_id=form.cleaned_data["teacher"]

            try:
                category=Category.objects.get(id=category_id)
                teacher=Teacher.objects.get(id=teacher_id)
                course=Course.objects.create(course_name=course_name, course_description=course_description, category_id=category, teacher_id=teacher)
                course.save()
                messages.success(request,"Successfully Added Course")
                return HttpResponseRedirect(reverse("add_course"))
            except:
                messages.error(request,"Failed to Add Course")
                return HttpResponseRedirect(reverse("add_course"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "hod_templates/add_course_template.html", {"form": form})
        
def manage_courses(request):
    courses = Course.objects.all()
    return render(request, "hod_templates/manage_courses_template.html", {"courses": courses})

def edit_course(request, course_id):
    request.session['course_id']=course_id
    course_obj=Course.objects.get(id=course_id)
    form=EditCourseForm()
    form.fields['course_name'].initial=course_obj.course_name
    form.fields['course_description'].initial=course_obj.course_description
    form.fields['category'].initial=course_obj.category_id
    form.fields['teacher'].initial=course_obj.teacher_id

    return render(request, "hod_templates/edit_course_template.html",{"form":form, "id":course_id})

def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.session.get("course_id")
        if course_id == None:
            return HttpResponseRedirect(reverse("manage_courses"))

        form = EditCourseForm(request.POST)
        if form.is_valid():
            course_name=form.cleaned_data["course_name"]
            course_description=form.cleaned_data["course_description"]
            category_id=form.cleaned_data["category"]
            teacher_id=form.cleaned_data["teacher"]

            try:
                category=Category.objects.get(id=category_id)
                teacher=Teacher.objects.get(id=teacher_id)
                course=Course.objects.get(id=course_id)
                course.course_name=course_name
                course.course_description=course_description
                course.category_id=category
                course.teacher_id=teacher
                course.save()

                del request.session['course_id']
                messages.success(request,"Successfully Edited Course")
                return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id":course_id}))
            except:
                messages.error(request,"Failed to Edit Course")
                return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id":course_id}))
        else:
            form=EditCourseForm(request.POST)
            course=Course.objects.get(id=course_id)
            return render(request,"hod_templates/edit_course_template.html",{"form":form,"id":course_id})

def delete_course(request, course_id):
    
    course=Course.objects.get(id=course_id)
    if request.method == "POST":
        course.delete()
        return HttpResponseRedirect(reverse("manage_courses"))

    context = {'item':course}
    return render(request,"hod_templates/delete_course_template.html", context)

# ----- COURSES CRUD end -----


# ----- ENROLLMENTS -----

def manage_enrollments(request):
    enrollments = Enrollment.objects.all()
    return render(request, "hod_templates/manage_enrollments_template.html", {"enrollments": enrollments})

def delete_enrollment(request, enrollment_id):
    
    enrollment=Enrollment.objects.get(id=enrollment_id)
    if request.method == "POST":
        enrollment.delete()
        return HttpResponseRedirect(reverse("manage_enrollments"))

    context = {'item':enrollment}
    return render(request,"hod_templates/delete_enrollment_template.html", context)

def enrollment(request):
    enrollments=Enrollment.objects.all()
    student_id = request.user.id
    student = Student.objects.get(id=student_id)
    list_course = []
    courses = Course.objects.all()
    for item in courses:
        list_course.append(item)

    for item in enrollments:
        if item.student_id == student:
            course = item.course_id
            list_course.remove(course)
            
    courses=list_course
    return render(request, "hod_templates/enrollment_template.html", {"courses": courses})

def enroll(request, course_id):
    request.session['course_id']=course_id
    if request.method == "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_obj=Course.objects.get(id=course_id)
        student_id = request.user.id
        student = Student.objects.get(id=student_id)

        try:
            Enrollment.objects.create(student_id=student, course_id=course_obj)
            messages.success(request, "Successfully Enrolled")
            return HttpResponseRedirect(reverse("enrollment"))
        except:
            messages.error(request, "You've already enrolled in this course!")
            return HttpResponseRedirect(reverse("enrollment"))
        
def my_enrollments(request):
    enrollments=Enrollment.objects.all()
    student_id = request.user.id
    student = Student.objects.get(id=student_id)
    list_enrollments = []
    for item in enrollments:
        if item.student_id == student:
            enrollment = item
            list_enrollments.append(enrollment)
    enrollments=list_enrollments
    return render(request, "hod_templates/my_enrollments_template.html", {"enrollments": enrollments})


def unenroll(request, enrollment_id):
    request.session['enrollment_id']=enrollment_id
    enrollment=Enrollment.objects.get(id=enrollment_id)
    if request.method == "POST":
        enrollment.delete()
        messages.success(request, "Successfully Unenrolled")
        return HttpResponseRedirect(reverse("my_enrollments"))
    context = {'item':enrollment}
    return render(request,"hod_templates/unenroll_template.html", context)

        