"""web_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from course import HodViews, views, StudentViews, TeacherViews
from web_project import settings

urlpatterns = [
    path('', views.showLoginPage, name="show_login"),
    path('demo', views.showDemoPage),
    path('doLogin', views.doLogin, name="do_login"),
    path('admin/', admin.site.urls),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user, name="logout"),
    path('admin_home', HodViews.admin_home, name="admin_home"),

    path('add_teacher', HodViews.add_teacher, name="add_teacher"),
    path('add_teacher_save', HodViews.add_teacher_save, name="add_teacher_save"),
    path('manage_teachers', HodViews.manage_teachers, name="manage_teachers"),
    path('edit_teacher/<str:teacher_id>', HodViews.edit_teacher, name="edit_teacher"),
    path('edit_teacher_save', HodViews.edit_teacher_save, name="edit_teacher_save"),
    path('delete_teacher/<str:teacher_id>', HodViews.delete_teacher, name="delete_teacher"),

    path('add_category', HodViews.add_category, name="add_category"),
    path('add_category_save', HodViews.add_category_save, name="add_category_save"),
    path('manage_categories', HodViews.manage_categories, name="manage_categories"),
    path('edit_category/<str:category_id>', HodViews.edit_category, name="edit_category"),
    path('edit_category_save', HodViews.edit_category_save, name="edit_category_save"),
    path('delete_category/<str:category_id>', HodViews.delete_category, name="delete_category"),

    path('teacher_add_category', TeacherViews.add_category, name="teacher_add_category"),
    path('teacher_add_category_save', TeacherViews.add_category_save, name="teacher_add_category_save"),
    path('teacher_manage_categories', TeacherViews.manage_categories, name="teacher_manage_categories"),
    path('teacher_edit_category/<str:category_id>', TeacherViews.edit_category, name="teacher_edit_category"),
    path('teacher_edit_category_save', TeacherViews.edit_category_save, name="teacher_edit_category_save"),
    path('teacher_delete_category/<str:category_id>', TeacherViews.delete_category, name="teacher_delete_category"),

    path('add_course', HodViews.add_course, name="add_course"),
    path('add_course_save', HodViews.add_course_save, name="add_course_save"),
    path('manage_courses', HodViews.manage_courses, name="manage_courses"),
    path('edit_course/<str:course_id>', HodViews.edit_course,name="edit_course"),
    path('edit_course_save', HodViews.edit_course_save,name="edit_course_save"),
    path('delete_course/<str:course_id>', HodViews.delete_course, name="delete_course"),

    path('teacher_add_course', TeacherViews.add_course, name="teacher_add_course"),
    path('teacher_add_course_save', TeacherViews.add_course_save, name="teacher_add_course_save"),
    path('teacher_manage_courses', TeacherViews.manage_courses, name="teacher_manage_courses"),
    path('teacher_edit_course/<str:course_id>', TeacherViews.edit_course,name="teacher_edit_course"),
    path('teacher_edit_course_save', TeacherViews.edit_course_save,name="teacher_edit_course_save"),
    path('teacher_delete_course/<str:course_id>', TeacherViews.delete_course, name="teacher_delete_course"),

    path('add_student', HodViews.add_student,name="add_student"),
    path('add_student_save', HodViews.add_student_save, name="add_student_save"),
    path('manage_students', HodViews.manage_students, name="manage_students"),
    path('edit_student/<str:student_id>', HodViews.edit_student, name="edit_student"),
    path('edit_student_save', HodViews.edit_student_save, name="edit_student_save"),
    path('delete_student/<str:student_id>', HodViews.delete_student, name="delete_student"),

    path('manage_enrollments', HodViews.manage_enrollments,name="manage_enrollments"),
    path('delete_enrollment/<str:enrollment_id>', HodViews.delete_enrollment, name="delete_enrollment"),
    path('enrollment', StudentViews.enrollment, name="enrollment"),
    path('enroll/<str:course_id>', StudentViews.enroll, name="enroll"),
    path('my_enrollments', StudentViews.my_enrollments, name="my_enrollments"),
    path('unenroll/<str:enrollment_id>', StudentViews.unenroll, name="unenroll"),

    path('teacher_home', TeacherViews.teacher_home, name="teacher_home"),
    path('student_home', StudentViews.student_home, name="student_home"),
   
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
