from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)  # Unique talaba ID
    graduation_year = models.IntegerField()  # Bitirgan yili

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Location(models.Model):
    room = models.CharField(max_length=50)  # Honaning nomi yoki raqami
    shelf = models.CharField(max_length=50)  # Shkaf raqami yoki nomi
    row = models.CharField(max_length=50)  # Polkada qayerda

    def __str__(self):
        return f"Hona: {self.room}, Shkaf: {self.shelf}, Polka: {self.row}"

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('diplom', 'Diplom'),
        ('atestat', 'Atestat'),
        ('pasport', 'Pasport kopiya'),
        ('ariza', 'Ariza'),
        ('buyruq', 'Buyruqdan ko‘chirma'),
        ('reyting', 'Reyting'),
        ('bmi', 'BMI'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    is_available = models.BooleanField(default=False)  # Hujjat mavjudmi?
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.doc_type} ({'Mavjud' if self.is_available else 'Mavjud emas'}) - {self.student}"
