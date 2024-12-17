from django.shortcuts import render, get_object_or_404, redirect
from arxiv.models import SrtqiStudent, DocumentSrtqiStudent, Location
from arxiv.views.views import login_decorator
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


@login_decorator
def srtqistudent_documents_table(request):
    srtqistudents = SrtqiStudent.objects.all()[::-1] # barcha talabalar malumotni olish
    document_types = dict(DocumentSrtqiStudent.DOCUMENT_TYPES) # Hujjat turli 
    query = request.GET.get('q', '')
    if query:
        srtqistudents = SrtqiStudent.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(surname__icontains=query) |
            Q(srtqi_id__icontains=query) |
            Q(graduation_year__icontains=str(query))  # graduation_year raqam bo'lsa, str() bilan qidirish kerak
        )

    # Talabalar va hujjatlarni qayta ishlash
    data = []
    for srtqistudent in srtqistudents:
        documents = {doc.doc_type: doc for doc in srtqistudent.documents.all()}
        srtqistudent_data = {
            'srtqistudent': srtqistudent,
            'documents': [
                { 
                    'type': doc_type_name,
                    'is_available': documents.get(doc_type, None) is not None and documents[doc_type].is_available,
                }
                for doc_type, doc_type_name in document_types.items()
            ]
        } 
        data.append(srtqistudent_data)

    page_size = request.GET.get('page_size', 7)  # Agar qiymat bo'lmasa, default 7 bo'ladi
    paginator = Paginator(data, page_size)  # Paginatorni yaratish
    page_number = request.GET.get('page')  # Foydalanuvchi tanlagan sahifa raqamini olish
    page_obj = paginator.get_page(page_number)
    ctx = {'page_obj':page_obj, 'document_types':document_types, 'srtqistudents': srtqistudents, 'segment':'srtqi'}
    return render(request, 'srtqi/table.html', ctx)
 
@login_decorator
def view_srtqistudent(request, srtqistudent_id):
    try:
        srtqistudent = SrtqiStudent.objects.get(id=srtqistudent_id)
        documents = DocumentSrtqiStudent.objects.filter(srtqistudent=srtqistudent)
    except SrtqiStudent.DoesNotExist:
        return HttpResponseNotFound("Srtqi student topilmadi.")

    return render(request, "srtqi/view_srtqistudent.html", {"srtqistudent": srtqistudent, "documents": documents, 'segment':'srtqi'})

@login_decorator
def add_srtqistudent(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        surname = request.POST.get("surname")
        birthday = request.POST.get("birthday")
        srtqi_id = request.POST.get("srtqi_id")
        graduation_year = request.POST.get("graduation_year")
        # Birinchi `location` ni tanlash
        location_ids = request.POST.getlist("location")
        location_id = location_ids[0] if location_ids else None
        srtqistudent = SrtqiStudent.objects.create(
            first_name=first_name,
            last_name=last_name,
            surname=surname,
            birthday=birthday,
            srtqi_id=srtqi_id,
            graduation_year=graduation_year,
            location=Location.objects.get(id=location_id) if location_id else None,
        )

        # Hujjatlarni saqlash
        doc_types = request.POST.getlist("doc_type[]")
        is_available_list = request.POST.getlist("is_available[]")
        

        for doc_type, is_available in zip(doc_types, is_available_list):
            DocumentSrtqiStudent.objects.create(
                srtqistudent=srtqistudent,
                doc_type=doc_type,
                is_available=bool(is_available),
            )

        return redirect("srtqistudent_documents_table")  # Talabalar ro'yxatiga yo'naltirish
    locations = Location.objects.all()
    return render(request, "srtqi/add_srtqistudent.html",  {"locations": locations, 'segment':'srtqi'})


@login_decorator
def edit_srtqistudent(request, srtqistudent_id):
    srtqistudent = get_object_or_404(SrtqiStudent, id=srtqistudent_id)
    locations = Location.objects.all()

    if request.method == "POST":
        # Talabaning asosiy ma’lumotlarini yangilash
        srtqistudent.first_name = request.POST.get("first_name")
        srtqistudent.last_name = request.POST.get("last_name")
        srtqistudent.surname = request.POST.get("surname")
        srtqistudent.birthday = request.POST.get("birthday")
        srtqistudent.srtqi_id = request.POST.get("srtqi_id")
        srtqistudent.graduation_year = request.POST.get("graduation_year")
         # Birinchi `location` ni tanlash
        location_ids = request.POST.getlist("location")
        location_id = location_ids[0] if location_ids else None

        if location_id:  # Agar location tanlangan bo'lsa
            srtqistudent.location = Location.objects.get(id=location_id)
        else:
            srtqistudent.location = None  # Lokatsiya tanlanmagan bo'lsa

        srtqistudent.save()

        # Mavjud hujjatlarni yangilash
        doc_ids = request.POST.getlist("doc_ids[]")
        doc_types = request.POST.getlist("doc_type[]")
        is_available_list = request.POST.getlist("is_available[]")
        

        for doc_id, doc_type, is_available in zip(doc_ids, doc_types, is_available_list):
            document = DocumentSrtqiStudent.objects.get(id=doc_id)
            document.doc_type = doc_type
            document.is_available = is_available == "1"
            document.save()

        # Yangi hujjatlarni qo'shish
        new_doc_types = request.POST.getlist("new_doc_type[]")
        new_is_available_list = request.POST.getlist("new_is_available[]")

        for doc_type, is_available in zip(new_doc_types, new_is_available_list):
            if doc_type:  # Hujjat turi tanlangan bo'lsa
                DocumentSrtqiStudent.objects.create(
                    srtqistudent=srtqistudent,
                    doc_type=doc_type,
                    is_available=is_available == "1",
                )

        return redirect("srtqistudent_documents_table")  # Talabalar ro'yxatiga yo'naltirish

    return render(request, "srtqi/edit_srtqistudent.html", {"srtqistudent": srtqistudent, "locations": locations, 'segment':'srtqi'})

@login_decorator
def delete_srtqistudent(request, srtqistudent_id):
    srtqistudent = SrtqiStudent.objects.get(id=srtqistudent_id)
    srtqistudent.delete()
    return redirect("srtqistudent_documents_table")

@login_decorator
@csrf_exempt
def update_document_srtqistudent_availability(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            document_id = data['document_id']
            is_available = data['is_available']

            document = DocumentSrtqiStudent.objects.get(id=document_id)
            document.is_available = is_available
            document.save()

            return JsonResponse({'success': True})

        except DocumentSrtqiStudent.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'DocumentSrtqiStudent not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
