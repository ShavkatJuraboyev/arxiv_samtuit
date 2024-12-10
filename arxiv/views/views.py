from django.shortcuts import render, get_object_or_404, redirect
from arxiv.forms import LocationForm, LoginForm
from arxiv.models import Student, Document, Location
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.db.models import Q

def login_decorator(func):
    return login_required(func, login_url='user_login')

def user_login(request):
    if request.POST:
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, password=password, username=username)
            if user is not None:
                login(request, user)
                messages.success(request, f'{request.user.username} tizimga kirdiz!')
                return redirect('student_documents_table')
            else:
                messages.warning(request, 'Bunday foydalanuvchi mavjud emas!')
                return redirect('user_login')
        else:
            messages.warning(request, 'Username yoki parol xato!')
            return redirect('user_login')
    else:
        forms = LoginForm()
    return render(request, 'tables/login.html')


@login_decorator
def logOut(request):
    logout(request)
    return redirect("user_login")

@login_decorator
def student_documents_table(request):
    students = Student.objects.all()[::-1] # barcha talabalar malumotni olish
    document_types = dict(Document.DOCUMENT_TYPES) # Hujjat turli 
    query = request.GET.get('q', '')
    if query:
        students = Student.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(surname__icontains=query) |
            Q(student_id__icontains=query) |
            Q(graduation_year__icontains=str(query))  # graduation_year raqam bo'lsa, str() bilan qidirish kerak
        )

    # Talabalar va hujjatlarni qayta ishlash
    data = []
    for student in students:
        documents = {doc.doc_type: doc for doc in student.documents.all()}
        student_data = {
            'student': student,
            'documents': [
                {
                    'type': doc_type_name,
                    'is_available': documents.get(doc_type, None) is not None and documents[doc_type].is_available,
                }
                for doc_type, doc_type_name in document_types.items()
            ]
        }
        data.append(student_data)

    page_size = request.GET.get('page_size', 7)  # Agar qiymat bo'lmasa, default 7 bo'ladi
    paginator = Paginator(data, page_size)  # Paginatorni yaratish
    page_number = request.GET.get('page')  # Foydalanuvchi tanlagan sahifa raqamini olish
    page_obj = paginator.get_page(page_number)
    ctx = {'page_obj':page_obj, 'document_types':document_types, 'students': students, 'segment':'student'}
    return render(request, 'tables/table.html', ctx)

@login_decorator
def view_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        documents = Document.objects.filter(student=student)
    except Student.DoesNotExist:
        return HttpResponseNotFound("Talaba topilmadi.")

    return render(request, "tables/view_student.html", {"student": student, "documents": documents, 'segment':'student'})

@login_decorator
def add_student(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        surname = request.POST.get("surname")
        student_id = request.POST.get("student_id")
        graduation_year = request.POST.get("graduation_year")
        # Birinchi `location` ni tanlash
        location_ids = request.POST.getlist("location")
        location_id = location_ids[0] if location_ids else None
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            surname=surname,
            student_id=student_id,
            graduation_year=graduation_year,
            location=Location.objects.get(id=location_id) if location_id else None,
        )

        # Hujjatlarni saqlash
        doc_types = request.POST.getlist("doc_type[]")
        is_available_list = request.POST.getlist("is_available[]")
        

        for doc_type, is_available in zip(doc_types, is_available_list):
            Document.objects.create(
                student=student,
                doc_type=doc_type,
                is_available=bool(is_available),
            )

        return redirect("student_documents_table")  # Talabalar ro'yxatiga yo'naltirish
    locations = Location.objects.all()
    return render(request, "tables/add_student.html",  {"locations": locations, 'segment':'student'})

@login_decorator
@csrf_exempt
def add_location(request):
    if request.method == "POST":
        room = request.POST.get("room")
        shelf = request.POST.get("shelf")
        row = request.POST.get("row")

        # Yangi joyni yaratish
        location = Location.objects.create(room=room, shelf=shelf, row=row)

        # Javob qaytarish
        return JsonResponse({
            'success': True,
            'location': {
                'id': location.id,
                'room': location.room,
                'shelf': location.shelf,
                'row': location.row,
            }
        })
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_decorator
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    locations = Location.objects.all()

    if request.method == "POST":
        # Talabaning asosiy ma’lumotlarini yangilash
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.surname = request.POST.get("surname")
        student.student_id = request.POST.get("student_id")
        student.graduation_year = request.POST.get("graduation_year")
         # Birinchi `location` ni tanlash
        location_ids = request.POST.getlist("location")
        location_id = location_ids[0] if location_ids else None

        if location_id:  # Agar location tanlangan bo'lsa
            student.location = Location.objects.get(id=location_id)
        else:
            student.location = None  # Lokatsiya tanlanmagan bo'lsa

        student.save()

        # Mavjud hujjatlarni yangilash
        doc_ids = request.POST.getlist("doc_ids[]")
        doc_types = request.POST.getlist("doc_type[]")
        is_available_list = request.POST.getlist("is_available[]")
        

        for doc_id, doc_type, is_available in zip(doc_ids, doc_types, is_available_list):
            document = Document.objects.get(id=doc_id)
            document.doc_type = doc_type
            document.is_available = is_available == "1"
            document.save()

        # Yangi hujjatlarni qo'shish
        new_doc_types = request.POST.getlist("new_doc_type[]")
        new_is_available_list = request.POST.getlist("new_is_available[]")

        for doc_type, is_available in zip(new_doc_types, new_is_available_list):
            if doc_type:  # Hujjat turi tanlangan bo'lsa
                Document.objects.create(
                    student=student,
                    doc_type=doc_type,
                    is_available=is_available == "1",
                )

        return redirect("student_documents_table")  # Talabalar ro'yxatiga yo'naltirish

    return render(request, "tables/edit_student.html", {"student": student, "locations": locations, 'segment':'student'})


@login_decorator
def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    student.delete()
    return redirect("student_documents_table")

@login_decorator
@csrf_exempt
def update_document_availability(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            document_id = data['document_id']
            is_available = data['is_available']

            document = Document.objects.get(id=document_id)
            document.is_available = is_available
            document.save()

            return JsonResponse({'success': True})

        except Document.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Document not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
