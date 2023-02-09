from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from course.models import Teacher, Course, Category
from course.forms import AddCourseForm, EditCourseForm


def teacher_home(request):
    return render(request, "teacher_templates/teacher_home_template.html")

# ----- CATEGORIES CRUD -----


def add_category(request):
    return render(request,"teacher_templates/add_category_template.html")

def add_category_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        category=request.POST.get("category")
        try:
            category_model=Category(category_name=category)
            category_model.save()
            messages.success(request,"Successfully Added Category")
            return HttpResponseRedirect("teacher_add_category")
        except:
            messages.error(request,"Category Already Exist")
            return HttpResponseRedirect("teacher_add_category")
        
def manage_categories(request):
    category=Category.objects.all()
    return render(request,"teacher_templates/manage_categories_template.html",{"category":category})

def edit_category(request, category_id):
    category=Category.objects.get(id=category_id)
    return render(request,"teacher_templates/edit_category_template.html",{"category":category, "id":category_id})

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
            return HttpResponseRedirect(reverse("teacher_edit_category", kwargs={"category_id":category_id}))
        except:
            messages.error(request, "Failed to Edit Category")
            return HttpResponseRedirect(reverse("teacher_edit_category", kwargs={"category_id":category_id}))
        

def delete_category(request, category_id):
    
    category=Category.objects.get(id=category_id)
    if request.method == "POST":
        category.delete()
        return HttpResponseRedirect(reverse("teacher_manage_categories"))

    context = {'item':category}
    return render(request,"teacher_templates/delete_category_template.html", context)


# ----- CATEGORIES CRUD end -----

# ----- COURSES CRUD -----

def add_course(request):
    form = AddCourseForm()
    context = {"form": form}
    return render(request, "teacher_templates/add_course_template.html", context)


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
                return HttpResponseRedirect(reverse("teacher_add_course"))
            except:
                messages.error(request,"Failed to Add Course")
                return HttpResponseRedirect(reverse("teacher_add_course"))
        else:
            form=AddCourseForm(request.POST)
            return render(request, "teacher_templates/add_course_template.html", {"form": form})
        
def manage_courses(request):
    courses = Course.objects.all()
    return render(request, "teacher_templates/manage_courses_template.html", {"courses": courses})

def edit_course(request, course_id):
    request.session['course_id']=course_id
    course_obj=Course.objects.get(id=course_id)
    form=EditCourseForm()
    form.fields['course_name'].initial=course_obj.course_name
    form.fields['course_description'].initial=course_obj.course_description
    form.fields['category'].initial=course_obj.category_id
    form.fields['teacher'].initial=course_obj.teacher_id

    return render(request, "teacher_templates/edit_course_template.html",{"form":form, "id":course_id})

def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.session.get("course_id")
        if course_id == None:
            return HttpResponseRedirect(reverse("teacher_manage_courses"))

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
                return HttpResponseRedirect(reverse("teacher_edit_course", kwargs={"course_id":course_id}))
            except:
                messages.error(request,"Failed to Edit Course")
                return HttpResponseRedirect(reverse("teacher_edit_course", kwargs={"course_id":course_id}))
        else:
            form=EditCourseForm(request.POST)
            course=Course.objects.get(id=course_id)
            return render(request,"teacher_templates/edit_course_template.html",{"form":form,"id":course_id})

def delete_course(request, course_id):
    
    course=Course.objects.get(id=course_id)
    if request.method == "POST":
        course.delete()
        return HttpResponseRedirect(reverse("teacher_manage_courses"))

    context = {'item':course}
    return render(request,"teacher_templates/delete_course_template.html", context)

# ----- COURSES CRUD end -----
