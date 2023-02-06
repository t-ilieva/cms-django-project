from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    USER_TYPE_SELECTION = (
        (1, "HOD"),
        (2, "Teacher"),
        (3, "Student")
    )

    user_type = models.CharField(max_length=1, choices=USER_TYPE_SELECTION, default=1)

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    address = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Student(models.Model):
    GENDER_SELECTION = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_SELECTION)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['first_name']


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.category_name}'


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    starting_date = models.DateTimeField()
    ending_date = models.DateTimeField()
    students = models.ManyToManyField(Student, through='Enrollment')

    def __str__(self):
        return self.course_name

    class Meta:
        ordering = ['course_name']


class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student_id.first_name} {self.student_id.last_name} has enrolled in course {self.course_id.course_name}.'

    class Meta:
        unique_together = ('course_id', 'student_id')

