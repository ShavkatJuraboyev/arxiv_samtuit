from django.urls import path
from arxiv.views.views import (
    student_documents_table, add_student, 
    add_location, user_login, logOut, view_student,
    edit_student, delete_student, update_document_availability
    )
from arxiv.views.employes import (
    employee_documents_table, add_employee, view_employee,
    edit_employee, delete_employee,
    update_document_employee_availability
    )
from arxiv.views.abuturiyent import (
    abuturiyent_documents_table, add_abuturiyent, view_abuturiyent,
    edit_abuturiyent, delete_abuturiyent,
    update_document_abuturiyent_availability
    )

urlpatterns = [ 
    path('', student_documents_table, name="student_documents_table"),
    path('student/<int:student_id>/', view_student, name='view_student'),
    path('add/student/', add_student, name='add_student'),
    path('add/location/', add_location, name='add_location'),
    path("student/<int:student_id>/edit/", edit_student, name="edit_student"),
    path('student/<int:student_id>/delete/', delete_student, name='delete_student'),
    path('update/document/availability/', update_document_availability, name='update_document_availability'),

    path('user_login/', user_login, name='user_login'),
    path('logout/', logOut, name="logout"),

    path('employee/documents/table/', employee_documents_table, name="employee_documents_table"),
    path('employee/<int:employee_id>/', view_employee, name='view_employee'),
    path('add/employee/', add_employee, name='add_employee'),
    path("employee/<int:employee_id>/edit/", edit_employee, name="edit_employee"),
    path('employee/<int:employee_id>/delete/', delete_employee, name='delete_employee'),
    path('update/document/employee/availability', update_document_employee_availability, name='update_document_employee_availability'),

    path('abuturiyent/documents/table/', abuturiyent_documents_table, name="abuturiyent_documents_table"),
    path('abuturiyent/<int:abuturiyent_id>/', view_abuturiyent, name='view_abuturiyent'),
    path('add/abuturiyent/', add_abuturiyent, name='add_abuturiyent'),
    path("abuturiyent/<int:abuturiyent_id>/edit/", edit_abuturiyent, name="edit_abuturiyent"),
    path('abuturiyent/<int:abuturiyent_id>/delete/', delete_abuturiyent, name='delete_abuturiyent'),
    path('update/document/abuturiyent/availability', update_document_abuturiyent_availability, name='update_document_abuturiyent_availability'),
]
