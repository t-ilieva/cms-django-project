
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from course.models import Course, Student, Enrollment, User



def student_home(request):
    return render(request,"student_templates/student_home_template.html")

def enrollment(request):
    enrollments=Enrollment.objects.all()
    student_id = request.user.id
    user_obj = User.objects.get(id=student_id)
    student = Student.objects.get(user=user_obj)
    list_course = []
    courses = Course.objects.all()
    for item in courses:
        list_course.append(item)

    for item in enrollments:
        if item.student_id == student:
            course = item.course_id
            list_course.remove(course)
            
    courses=list_course
    return render(request, "student_templates/enrollment_template.html", {"courses": courses})

def enroll(request, course_id):
    request.session['course_id']=course_id
    if request.method == "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_obj=Course.objects.get(id=course_id)
        student_id = request.user.id
        user_obj = User.objects.get(id=student_id)
        student = Student.objects.get(user=user_obj)

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
    user_obj = User.objects.get(id=student_id)
    student = Student.objects.get(user=user_obj)
    list_enrollments = []
    for item in enrollments:
        if item.student_id == student:
            enrollment = item
            list_enrollments.append(enrollment)
    enrollments=list_enrollments
    return render(request, "student_templates/my_enrollments_template.html", {"enrollments": enrollments})


def unenroll(request, enrollment_id):
    request.session['enrollment_id']=enrollment_id
    enrollment=Enrollment.objects.get(id=enrollment_id)
    if request.method == "POST":
        enrollment.delete()
        messages.success(request, "Successfully Unenrolled")
        return HttpResponseRedirect(reverse("my_enrollments"))
    context = {'item':enrollment}
    return render(request,"student_templates/unenroll_template.html", context)

        