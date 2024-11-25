from django.urls import path
from .views.views import student_documents_table, add_student, add_location, user_login, logOut, view_student, edit_student, delete_student, update_document_availability

urlpatterns = [
    path('', student_documents_table, name="student_documents_table"),
    path('student/<int:student_id>/', view_student, name='view_student'),
    path('add_student/', add_student, name='add_student'),
    path('add_location/', add_location, name='add_location'),
    path("student/<int:student_id>/edit/", edit_student, name="edit_student"),
    path('student/<int:student_id>/delete/', delete_student, name='delete_student'),
    path('update_document_availability/', update_document_availability, name='update_document_availability'),

    path('user_login/', user_login, name='user_login'),
    path('logout/', logOut, name="logout"),
] 
