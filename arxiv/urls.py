from django.urls import path
from .views import student_documents, student_documents_table, add_student, add_location, add_location_table

urlpatterns = [
    path('', student_documents_table, name="student_documents_table"),
    path('student/documents/', student_documents, name="student_documents"),
    path('add_student/', add_student, name='add_student'),
    path('add_location/', add_location, name='add_location'),
    path('add_location_table/', add_location_table, name='add_location_table'),
] 
