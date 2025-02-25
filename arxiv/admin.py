from django.contrib import admin
from .models import Student, Document, Location, Employee, DocumentEmployee, Abuturiyent, DocumentAbuturiyent, SrtqiStudent, DocumentSrtqiStudent, Magister, DocumentMagister

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('room', 'shelf')
    search_fields = ('room', 'shelf')

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1
    fields = ('doc_type', 'is_available')
    verbose_name = 'Hujjat turi'
    verbose_name_plural = 'Hujjatlar mavjudligi'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'surname', 'student_id', 'graduation_year', 'get_documents')

    def get_documents(self, obj):
        doc_labels = dict(Document.DOCUMENT_TYPES)  # Key -> Value mapping yaratamiz
        return ", ".join([doc_labels.get(doc.doc_type, doc.doc_type) for doc in obj.documents.all()])
    
    get_documents.short_description = 'Hujjatlar'

    search_fields = ('first_name', 'last_name', 'surname', 'student_id')
    list_filter = ('documents__doc_type',)  # Added filter for documents
    inlines = [DocumentInline]

class DocumentEmployeeInline(admin.TabularInline):
    model = DocumentEmployee
    extra = 1
    fields = ('doc_type', 'is_available')
    verbose_name = 'Hujjat turi'
    verbose_name_plural = 'Hujjatlar mavjudligi'
 
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'surname', 'employee_id', 'gone_year', 'get_documents')

    def get_documents(self, obj):
        doc_labels = dict(DocumentEmployee.DOCUMENT_TYPES)  # Key -> Value mapping yaratamiz
        return ", ".join([doc_labels.get(doc.doc_type, doc.doc_type) for doc in obj.documents.all()])
    
    get_documents.short_description = 'Hujjatlar'

    search_fields = ('first_name', 'last_name', 'surname', 'employee_id')
    list_filter = ('documents__doc_type',)  # Added filter for documents
    inlines = [DocumentEmployeeInline]

class DocumentAbuturiyentInline(admin.TabularInline):
    model = DocumentAbuturiyent
    extra = 1
    fields = ('doc_type', 'is_available')
    verbose_name = 'Hujjat turi'
    verbose_name_plural = 'Hujjatlar mavjudligi'

@admin.register(Abuturiyent)
class AbuturiyentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'surname', 'abuturiyent_id', 'graduation_year', 'get_documents')

    def get_documents(self, obj):
        doc_labels = dict(DocumentAbuturiyent.DOCUMENT_TYPES)  # Key -> Value mapping yaratamiz
        return ", ".join([doc_labels.get(doc.doc_type, doc.doc_type) for doc in obj.documents.all()])
    
    get_documents.short_description = 'Hujjatlar'

    search_fields = ('first_name', 'last_name', 'surname', 'abuturiyent_id')
    list_filter = ('documents__doc_type',)  # Added filter for documents
    inlines = [DocumentAbuturiyentInline]

class DocumentMagisterInline(admin.TabularInline):
    model = DocumentMagister
    extra = 1
    fields = ('doc_type', 'is_available')
    verbose_name = 'Hujjat turi'
    verbose_name_plural = 'Hujjatlar mavjudligi'

@admin.register(Magister)
class MagisterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'surname', 'srtqi_id', 'graduation_year', 'get_documents')

    def get_documents(self, obj):
        doc_labels = dict(DocumentMagister.DOCUMENT_TYPES)  # Key -> Value mapping yaratamiz
        return ", ".join([doc_labels.get(doc.doc_type, doc.doc_type) for doc in obj.documents.all()])
    
    get_documents.short_description = 'Hujjatlar'

    search_fields = ('first_name', 'last_name', 'surname', 'srtqi_id')
    list_filter = ('documents__doc_type',)  # Added filter for documents
    inlines = [DocumentMagisterInline]

class DocumentSrtqiStudentInline(admin.TabularInline):
    model = DocumentSrtqiStudent
    extra = 1
    fields = ('doc_type', 'is_available')
    verbose_name = 'Hujjat turi'
    verbose_name_plural = 'Hujjatlar mavjudligi'

@admin.register(SrtqiStudent)
class DocumentSrtqiStudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'surname', 'srtqi_id', 'graduation_year', 'get_documents')

    def get_documents(self, obj):
        doc_labels = dict(DocumentSrtqiStudent.DOCUMENT_TYPES)  # Key -> Value mapping yaratamiz
        return ", ".join([doc_labels.get(doc.doc_type, doc.doc_type) for doc in obj.documents.all()])
    
    get_documents.short_description = 'Hujjatlar'

    search_fields = ('first_name', 'last_name', 'surname', 'srtqi_id')
    list_filter = ('documents__doc_type',)  # Added filter for documents
    inlines = [DocumentSrtqiStudentInline]
