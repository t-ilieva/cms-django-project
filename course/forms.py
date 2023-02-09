from django import forms 
from django.forms import Form
from course.models import Student, Category, Teacher

class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    
class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    

class AddCourseForm(forms.Form):
    course_name = forms.CharField(label="Name", max_length=255, widget=forms.TextInput(attrs={"class":"form-control"}))
    course_description = forms.CharField(label="Description", widget=forms.TextInput(attrs={"class":"form-control"}))

    try:
        categories = Category.objects.all()
        category_list = []
        for category in categories:
            single_category = (category.id, category.category_name)
            category_list.append(single_category)
    except:
        category_list = []
    
    try:
        teachers = Teacher.objects.all()
        teacher_list = []
        for teacher in teachers:
            single_teacher = (teacher.id, f'{teacher.user.first_name} {teacher.user.last_name}')
            teacher_list.append(single_teacher)
    except:
        category_list = []
    
    category = forms.ChoiceField(label="Category", choices=category_list, widget=forms.Select(attrs={"class":"form-control"}))
    teacher= forms.ChoiceField(label="Teacher", choices=teacher_list, widget=forms.Select(attrs={"class":"form-control"}))

class EditCourseForm(forms.Form):
    course_name = forms.CharField(label="Name", max_length=255, widget=forms.TextInput(attrs={"class":"form-control"}))
    course_description = forms.CharField(label="Description", widget=forms.TextInput(attrs={"class":"form-control"}))

    try:
        categories = Category.objects.all()
        category_list = []
        for category in categories:
            single_category = (category.id, category.category_name)
            category_list.append(single_category)
    except:
        category_list = []
    
    try:
        teachers = Teacher.objects.all()
        teacher_list = []
        for teacher in teachers:
            single_teacher = (teacher.id, f'{teacher.user.first_name} {teacher.user.last_name}')
            teacher_list.append(single_teacher)
    except:
        category_list = []
    
    category = forms.ChoiceField(label="Category", choices=category_list, widget=forms.Select(attrs={"class":"form-control"}))
    teacher= forms.ChoiceField(label="Teacher", choices=teacher_list, widget=forms.Select(attrs={"class":"form-control"}))
