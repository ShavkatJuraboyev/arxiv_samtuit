from django.contrib import admin
from .models import Student, Document, Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('room', 'shelf', 'row')
    search_fields = ('room', 'shelf', 'row')

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1
    fields = ('doc_type', 'is_available', 'location')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'student_id', 'graduation_year')
    search_fields = ('first_name', 'last_name', 'student_id')
    inlines = [DocumentInline]
