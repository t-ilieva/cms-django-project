from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6)
    address = models.TextField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
#    class Meta:
#        ordering = ['first_name']


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return f'{self.category_name}'


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_description = models.TextField()
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    students = models.ManyToManyField(Student, through='Enrollment')

    def __str__(self):
        return self.course_name


class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student_id.user.first_name} {self.student_id.user.last_name} has enrolled in course {self.course_id.course_name}.'

    class Meta:
        unique_together = ('course_id', 'student_id')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(user=instance)
        if instance.user_type==2:
            Teacher.objects.create(user=instance, address="")
        if instance.user_type==3:
            Student.objects.create(user=instance, address="")

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.teacher.save()
    if instance.user_type==3:
        instance.student.save()