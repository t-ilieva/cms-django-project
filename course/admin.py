from django.contrib import admin
from .models import Student, Category, Course, Enrollment

# Register your models here.

admin.site.register(Student)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Enrollment)



