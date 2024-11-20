from django.shortcuts import render, get_object_or_404, redirect
from .forms import StudentForm, DocumentForm, LocationForm
from .models import Student, Document, Location
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def add_student(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        student_id = request.POST.get("student_id")
        graduation_year = request.POST.get("graduation_year")

        if Student.objects.filter(student_id=student_id).exists():
            error_message = f"Talaba ID '{student_id}' allaqachon mavjud. Boshqa ID kiriting."
            return render(request, "tables/add_student.html", {"error": error_message})
        # Talabani saqlash
        if not graduation_year or not graduation_year.isdigit():
            error_yers = "Graduation year noto'g'ri yoki kiritilmagan"
            return render(request, "tables/add_student.html", {"error_yers": error_yers})

        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            graduation_year=graduation_year,
        )

        # Hujjatlarni saqlash
        doc_types = request.POST.getlist("doc_type[]")
        is_available_list = request.POST.getlist("is_available[]")
        locations = request.POST.getlist("location[]")

        for doc_type, is_available, location_id in zip(doc_types, is_available_list, locations):
            location = Location.objects.get(id=location_id) if location_id else None
            Document.objects.create(
                student=student,
                doc_type=doc_type,
                is_available=bool(is_available),
                location=location,
            )

        return redirect("student_documents_table")  # Talabalar ro'yxatiga yo'naltirish
    locations = Location.objects.all()
    return render(request, "tables/add_student.html",  {"locations": locations})

@csrf_exempt
def add_location(request):
    if request.method == "POST":
        room = request.POST.get("room")
        shelf = request.POST.get("shelf")
        row = request.POST.get("row")

        # Create and save the location
        location = Location.objects.create(room=room, row=row, shelf=shelf)
        return JsonResponse({"success": True, "location": {
            "id": location.id,
            "room": location.room,
            "row": location.row,
            "shelf": location.shelf,
        }})
    return JsonResponse({"success": False})


def add_location_table(request):
    if request.method == 'POST':
        location_form = LocationForm(request.POST)
        if location_form.is_valid():
            location_form.save()
            return redirect('add_student')  # Yoki boshqa manzilga
    else:
        location_form = LocationForm()

    return render(request, 'tables/add_location.html', {'form': location_form})

def student_documents_table(request):
    students = Student.objects.all() # barcha talabalar malumotni olish
    document_types = dict(Document.DOCUMENT_TYPES) # Hujjat turli 

    # talabalar va ularni hujjatlarni qayta ishlash 
    data = []
    for student in students:
        documents = {doc.doc_type: doc for doc in student.documents.all()}
        student_data = {
            'student':student,
            'documents': [
                {
                    'type':doc_type_name,
                    'is_available' : documents.get(doc_type, None) is not None and documents[doc_type].is_available,
                    'locations': documents[doc_type].location if documents.get(doc_type, None) else None,

                }
                for doc_type, doc_type_name in document_types.items()
            ]
        }
        data.append(student_data)

    paginator = Paginator(data, 3)  # Sahifaga 10 ta element
    page_number = request.GET.get('page')  # URL'dan sahifa raqamini olish
    page_obj = paginator.get_page(page_number)

    ctx = {'page_obj':page_obj, 'document_types':document_types}
    return render(request, 'tables/table.html', ctx)


def student_documents(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    document_types = dict(Document.DOCUMENT_TYPES)  # Hujjat turlari lug'atga aylantirildi
    documents = {doc.doc_type: doc for doc in student.documents.all()}  # Mavjud hujjatlar

    # Har bir hujjat turini bor/yo'q deb ko'rinishga o'tkazamiz
    document_status = [
        {
            'type': doc_type_name,
            'is_available': documents.get(doc_type, None) is not None and documents[doc_type].is_available,
        }
        for doc_type, doc_type_name in document_types.items()
    ]
    ctx ={'student': student, 'document_status': document_status}
    return render(request, 'tables/talaba.html', ctx)


