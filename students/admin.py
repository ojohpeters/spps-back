from django.contrib import admin
from .models import Student, Course, Result, AdditionalFactors

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'department', 'admission_year']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    list_filter = ['department', 'admission_year']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_title', 'credit_units', 'department']
    search_fields = ['course_code', 'course_title']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'semester', 'score', 'grade']
    list_filter = ['semester', 'grade']

@admin.register(AdditionalFactors)
class AdditionalFactorsAdmin(admin.ModelAdmin):
    list_display = ['student', 'attendance_percentage', 'assignment_average']
