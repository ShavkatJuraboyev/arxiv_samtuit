from django.shortcuts import render, get_object_or_404, redirect
from arxiv.models import Employee, DocumentEmployee, Location
from arxiv.views.views import login_decorator
from django.contrib import messages
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.db.models import Q


@login_decorator
def employee_documents_table(request):
    employees = Employee.objects.all()[::-1] # barcha talabalar malumotni olish
    document_types = dict(DocumentEmployee.DOCUMENT_TYPES) # Hujjat turli 
    query = request.GET.get('q', '')
    if query:
        employees = Employee.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(surname__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(graduation_year__icontains=str(query))  # graduation_year raqam bo'lsa, str() bilan qidirish kerak
        )

    # Talabalar va hujjatlarni qayta ishlash
    data = []
    for employee in employees:
        documents = {doc.doc_type: doc for doc in employee.documents.all()}
        employee_data = {
            'employee': employee,
            'documents': [
                { 
                    'type': doc_type_name,
                    'is_available': documents.get(doc_type, None) is not None and documents[doc_type].is_available,
                }
                for doc_type, doc_type_name in document_types.items()
            ]
        } 
        data.append(employee_data)

    page_size = request.GET.get('page_size', 7)  # Agar qiymat bo'lmasa, default 7 bo'ladi
    paginator = Paginator(data, page_size)  # Paginatorni yaratish
    page_number = request.GET.get('page')  # Foydalanuvchi tanlagan sahifa raqamini olish
    page_obj = paginator.get_page(page_number)
    ctx = {'page_obj':page_obj, 'document_types':document_types, 'employees': employees, 'segment':'employee'}
    return render(request, 'employee/table.html', ctx)

@login_decorator
def view_employee(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        documents = DocumentEmployee.objects.filter(employee=employee)
    except Employee.DoesNotExist:
        return HttpResponseNotFound("Talaba topilmadi.")

    return render(request, "employee/view_employee.html", {"employee": employee, "documents": documents, 'segment':'employee'})

@login_decorator
def add_employee(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        surname = request.POST.get("surname")
        employee_id = request.POST.get("employee_id")
        graduation_year = request.POST.get("graduation_year")
        # Birinchi `location` ni tanlash
        location_ids = request.POST.getlist("location")
        location_id = location_ids[0] if location_ids else None
        employee = Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            surname=surname,
            employee_id=employee_id,
            graduation_year=graduation_year,
            location=Location.objects.get(id=location_id) if location_id else None,
        )

        # Hujjatlarni saqlash
        doc_types = request.POST.getlist("doc_type[]")
        is_available_list = request.POST.getlist("is_available[]")
        

        for doc_type, is_available in zip(doc_types, is_available_list):
            DocumentEmployee.objects.create(
                employee=employee,
                doc_type=doc_type,
                is_available=bool(is_available),
            )

        return redirect("employee_documents_table")  # Talabalar ro'yxatiga yo'naltirish
    locations = Location.objects.all()
    return render(request, "employee/add_employee.html",  {"locations": locations, 'segment':'employee'})

@login_decorator
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    locations = Location.objects.all()

    if request.method == "POST":
        # Talabaning asosiy ma’lumotlarini yangilash
        employee.first_name = request.POST.get("first_name")
        employee.last_name = request.POST.get("last_name")
        employee.surname = request.POST.get("surname")
        employee.employee_id = request.POST.get("employee_id")
        employee.graduation_year = request.POST.get("graduation_year")
         # Birinchi `location` ni tanlash
        location_ids = request.POST.getlist("location")
        location_id = location_ids[0] if location_ids else None

        if location_id:  # Agar location tanlangan bo'lsa
            employee.location = Location.objects.get(id=location_id)
        else:
            employee.location = None  # Lokatsiya tanlanmagan bo'lsa

        employee.save()

        # Mavjud hujjatlarni yangilash
        doc_ids = request.POST.getlist("doc_ids[]")
        doc_types = request.POST.getlist("doc_type[]")
        is_available_list = request.POST.getlist("is_available[]")
        

        for doc_id, doc_type, is_available in zip(doc_ids, doc_types, is_available_list):
            document = DocumentEmployee.objects.get(id=doc_id)
            document.doc_type = doc_type
            document.is_available = is_available == "1"
            document.save()

        # Yangi hujjatlarni qo'shish
        new_doc_types = request.POST.getlist("new_doc_type[]")
        new_is_available_list = request.POST.getlist("new_is_available[]")

        for doc_type, is_available in zip(new_doc_types, new_is_available_list):
            if doc_type:  # Hujjat turi tanlangan bo'lsa
                DocumentEmployee.objects.create(
                    employee=employee,
                    doc_type=doc_type,
                    is_available=is_available == "1",
                )

        return redirect("employee_documents_table")  # Talabalar ro'yxatiga yo'naltirish

    return render(request, "employee/edit_employee.html", {"employee": employee, "locations": locations, 'segment':'employee'})

@login_decorator  
def delete_employee(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    return redirect("employee_documents_table")

@csrf_exempt
def update_document_employee_availability(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            document_id = data['document_id']
            is_available = data['is_available']

            document = DocumentEmployee.objects.get(id=document_id)
            document.is_available = is_available
            document.save()

            return JsonResponse({'success': True})

        except DocumentEmployee.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'DocumentEmployee not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
