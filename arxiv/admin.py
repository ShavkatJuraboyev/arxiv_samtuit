from django.contrib import admin
from .models import Student, Document, Location, Employee, DocumentEmployee, Abuturiyent, DocumentAbuturiyent

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('room', 'shelf', 'row')
    search_fields = ('room', 'shelf', 'row')

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1
    fields = ('doc_type', 'is_available')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'student_id', 'graduation_year')
    search_fields = ('first_name', 'last_name', 'student_id')
    inlines = [DocumentInline]

class DocumentEmployeeInline(admin.TabularInline):
    model = DocumentEmployee
    extra = 1
    fields = ('doc_type', 'is_available')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'employee_id', 'graduation_year')
    search_fields = ('first_name', 'last_name', 'employee_id')
    inlines = [DocumentEmployeeInline]

class DocumentAbuturiyentInline(admin.TabularInline):
    model = DocumentAbuturiyent
    extra = 1
    fields = ('doc_type', 'is_available')

@admin.register(Abuturiyent)
class AbuturiyentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'abuturiyent_id', 'graduation_year')
    search_fields = ('first_name', 'last_name', 'abuturiyent_id')
    inlines = [DocumentAbuturiyentInline]

