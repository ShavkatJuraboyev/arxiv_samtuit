from django.shortcuts import render, get_object_or_404, redirect
from arxiv.models import Abuturiyent, DocumentAbuturiyent, Location
from arxiv.views.views import login_decorator
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


@login_decorator 
def abuturiyent_documents_table(request):
    abuturiyents = Abuturiyent.objects.all()[::-1] # barcha talabalar malumotni olish
    document_types = dict(DocumentAbuturiyent.DOCUMENT_TYPES) # Hujjat turli 
    query = request.GET.get('q', '')
    if query:
        abuturiyents = Abuturiyent.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(surname__icontains=query) |
            Q(abuturiyent_id__icontains=query) |
            Q(graduation_year__icontains=str(query))  # graduation_year raqam bo'lsa, str() bilan qidirish kerak
        )

    # Talabalar va hujjatlarni qayta ishlash
    data = []
    for abuturiyent in abuturiyents:
        documents = {doc.doc_type: doc for doc in abuturiyent.documents.all()}
        abuturiyent_data = {
            'abuturiyent': abuturiyent,
            'documents': [
                { 
                    'type': doc_type_name,
                    'is_available': documents.get(doc_type, None) is not None and documents[doc_type].is_available,
                }
                for doc_type, doc_type_name in document_types.items()
            ]
        } 
        data.append(abuturiyent_data)

    page_size = request.GET.get('page_size', 7)  # Agar qiymat bo'lmasa, default 7 bo'ladi
    paginator = Paginator(data, page_size)  # Paginatorni yaratish
    page_number = request.GET.get('page')  # Foydalanuvchi tanlagan sahifa raqamini olish
    page_obj = paginator.get_page(page_number)
    ctx = {'page_obj':page_obj, 'document_types':document_types, 'abuturiyents': abuturiyents, 'segment':'abuturiyent'}
    return render(request, 'abuturiyent/table.html', ctx)

@login_decorator
def view_abuturiyent(request, abuturiyent_id):
    try:
        abuturiyent = Abuturiyent.objects.get(id=abuturiyent_id)
        documents = DocumentAbuturiyent.objects.filter(abuturiyent=abuturiyent)
    except Abuturiyent.DoesNotExist:
        return HttpResponseNotFound("Talaba topilmadi.")

    return render(request, "abuturiyent/view_abuturiyent.html", {"abuturiyent": abuturiyent, "documents": documents, 'segment':'abuturiyent'})

@login_decorator
def add_abuturiyent(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        surname = request.POST.get("surname")
        birthday = request.POST.get("birthday")
        abuturiyent_id = request.POST.get("abuturiyent_id")
        graduation_year = request.POST.get("graduation_year")
        # Birinchi `location` ni tanlash
        location_ids = request.POST.getlist("location")
        location_id = location_ids[0] if location_ids else None
        abuturiyent = Abuturiyent.objects.create(
            first_name=first_name,
            last_name=last_name,
            surname=surname,
            birthday=birthday,
            abuturiyent_id=abuturiyent_id,
            graduation_year=graduation_year,
            location=Location.objects.get(id=location_id) if location_id else None,
        )

        # Hujjatlarni saqlash
        doc_types = request.POST.getlist("doc_type[]")
        is_available_list = request.POST.getlist("is_available[]")
        

        for doc_type, is_available in zip(doc_types, is_available_list):
            DocumentAbuturiyent.objects.create(
                abuturiyent=abuturiyent,
                doc_type=doc_type,
                is_available=bool(is_available),
            )

        return redirect("abuturiyent_documents_table")  # Talabalar ro'yxatiga yo'naltirish
    locations = Location.objects.all()
    return render(request, "abuturiyent/add_abuturiyent.html",  {"locations": locations, 'segment':'abuturiyent'})

@login_decorator
def edit_abuturiyent(request, abuturiyent_id):
    abuturiyent = get_object_or_404(Abuturiyent, id=abuturiyent_id)
    locations = Location.objects.all()

    if request.method == "POST":
        # Talabaning asosiy ma’lumotlarini yangilash
        abuturiyent.first_name = request.POST.get("first_name")
        abuturiyent.last_name = request.POST.get("last_name")
        abuturiyent.surname = request.POST.get("surname")
        abuturiyent.birthday = request.POST.get("birthday")
        abuturiyent.abuturiyent_id = request.POST.get("abuturiyent_id")
        abuturiyent.graduation_year = request.POST.get("graduation_year")
         # Birinchi `location` ni tanlash
        location_ids = request.POST.getlist("location")
        location_id = location_ids[0] if location_ids else None

        if location_id:  # Agar location tanlangan bo'lsa
            abuturiyent.location = Location.objects.get(id=location_id)
        else:
            abuturiyent.location = None  # Lokatsiya tanlanmagan bo'lsa

        abuturiyent.save()

        # Mavjud hujjatlarni yangilash
        doc_ids = request.POST.getlist("doc_ids[]")
        doc_types = request.POST.getlist("doc_type[]")
        is_available_list = request.POST.getlist("is_available[]")
        

        for doc_id, doc_type, is_available in zip(doc_ids, doc_types, is_available_list):
            document = DocumentAbuturiyent.objects.get(id=doc_id)
            document.doc_type = doc_type
            document.is_available = is_available == "1"
            document.save()

        # Yangi hujjatlarni qo'shish
        new_doc_types = request.POST.getlist("new_doc_type[]")
        new_is_available_list = request.POST.getlist("new_is_available[]")

        for doc_type, is_available in zip(new_doc_types, new_is_available_list):
            if doc_type:  # Hujjat turi tanlangan bo'lsa
                DocumentAbuturiyent.objects.create(
                    abuturiyent=abuturiyent,
                    doc_type=doc_type,
                    is_available=is_available == "1",
                )

        return redirect("abuturiyent_documents_table")  # Talabalar ro'yxatiga yo'naltirish

    return render(request, "abuturiyent/edit_abuturiyent.html", {"abuturiyent": abuturiyent, "locations": locations, 'segment':'abuturiyent'})


@login_decorator
def delete_abuturiyent(request, abuturiyent_id):
    abuturiyent = Abuturiyent.objects.get(id=abuturiyent_id)
    abuturiyent.delete()
    return redirect("abuturiyent_documents_table")

@login_decorator
@csrf_exempt
def update_document_abuturiyent_availability(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            document_id = data['document_id']
            is_available = data['is_available']

            document = DocumentAbuturiyent.objects.get(id=document_id)
            document.is_available = is_available
            document.save()

            return JsonResponse({'success': True})

        except DocumentAbuturiyent.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'DocumentAbuturiyent not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
