from django.shortcuts import render, get_object_or_404, redirect
from arxiv.models import Magister, DocumentMagister, Location
from arxiv.views.views import login_decorator
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


@login_decorator
def magister_documents_table(request):
    magisters = Magister.objects.all()[::-1] # barcha talabalar malumotni olish
    document_types = dict(DocumentMagister.DOCUMENT_TYPES) # Hujjat turli 
    query = request.GET.get('q', '')
    if query:
        magisters = Magister.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(surname__icontains=query) |
            Q(srtqi_id__icontains=query) |
            Q(graduation_year__icontains=str(query))  # graduation_year raqam bo'lsa, str() bilan qidirish kerak
        )

    # Talabalar va hujjatlarni qayta ishlash
    data = []
    for magister in magisters:
        documents = {doc.doc_type: doc for doc in magister.documents.all()}
        magister_data = {
            'magister': magister,
            'documents': [
                { 
                    'type': doc_type_name,
                    'is_available': documents.get(doc_type, None) is not None and documents[doc_type].is_available,
                }
                for doc_type, doc_type_name in document_types.items()
            ]
        } 
        data.append(magister_data)

    page_size = request.GET.get('page_size', 7)  # Agar qiymat bo'lmasa, default 7 bo'ladi
    paginator = Paginator(data, page_size)  # Paginatorni yaratish
    page_number = request.GET.get('page')  # Foydalanuvchi tanlagan sahifa raqamini olish
    page_obj = paginator.get_page(page_number)
    ctx = {'page_obj':page_obj, 'document_types':document_types, 'magisters': magisters, 'segment':'magister'}
    return render(request, 'magister/table.html', ctx)
 
@login_decorator
def view_magister(request, magistr_id):
    try:
        magister = Magister.objects.get(id=magistr_id)
        documents = DocumentMagister.objects.filter(magister=magister)
    except Magister.DoesNotExist:
        return HttpResponseNotFound("Magistr topilmadi.")

    return render(request, "magister/view_magister.html", {"magister": magister, "documents": documents, 'segment':'magister'})

@login_decorator
def add_magister(request):
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
        magister = Magister.objects.create(
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
            DocumentMagister.objects.create(
                magister=magister,
                doc_type=doc_type,
                is_available=bool(is_available),
            )

        return redirect("magister_documents_table")  # Talabalar ro'yxatiga yo'naltirish
    locations = Location.objects.all()
    return render(request, "magister/add_magister.html",  {"locations": locations, 'segment':'magister'})


@login_decorator
def edit_magister(request, magistr_id):
    magister = get_object_or_404(Magister, id=magistr_id)
    locations = Location.objects.all()

    if request.method == "POST":
        # Talabaning asosiy ma’lumotlarini yangilash
        magister.first_name = request.POST.get("first_name")
        magister.last_name = request.POST.get("last_name")
        magister.surname = request.POST.get("surname")
        magister.birthday = request.POST.get("birthday")
        magister.srtqi_id = request.POST.get("srtqi_id")
        magister.graduation_year = request.POST.get("graduation_year")
         # Birinchi `location` ni tanlash
        location_ids = request.POST.getlist("location")
        location_id = location_ids[0] if location_ids else None

        if location_id:  # Agar location tanlangan bo'lsa
            magister.location = Location.objects.get(id=location_id)
        else:
            magister.location = None  # Lokatsiya tanlanmagan bo'lsa

        magister.save()

        # Mavjud hujjatlarni yangilash
        doc_ids = request.POST.getlist("doc_ids[]")
        doc_types = request.POST.getlist("doc_type[]")
        is_available_list = request.POST.getlist("is_available[]")
        

        for doc_id, doc_type, is_available in zip(doc_ids, doc_types, is_available_list):
            document = DocumentMagister.objects.get(id=doc_id)
            document.doc_type = doc_type
            document.is_available = is_available == "1"
            document.save()

        # Yangi hujjatlarni qo'shish
        new_doc_types = request.POST.getlist("new_doc_type[]")
        new_is_available_list = request.POST.getlist("new_is_available[]")

        for doc_type, is_available in zip(new_doc_types, new_is_available_list):
            if doc_type:  # Hujjat turi tanlangan bo'lsa
                DocumentMagister.objects.create(
                    magister=magister,
                    doc_type=doc_type,
                    is_available=is_available == "1",
                )

        return redirect("magister_documents_table")  # Talabalar ro'yxatiga yo'naltirish

    return render(request, "magister/edit_magister.html", {"magister": magister, "locations": locations, 'segment':'magister'})

@login_decorator
def delete_magister(request, magistr_id):
    magister = Magister.objects.get(id=magistr_id)
    magister.delete()
    return redirect("magister_documents_table")

@login_decorator
@csrf_exempt
def update_document_magister_availability(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            document_id = data['document_id']
            is_available = data['is_available']

            document = DocumentMagister.objects.get(id=document_id)
            document.is_available = is_available
            document.save()

            return JsonResponse({'success': True})

        except DocumentMagister.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'DocumentMagister not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
