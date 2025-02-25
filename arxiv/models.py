from django.db import models

class Location(models.Model):
    room = models.CharField(max_length=50)  # Honaning nomi yoki raqami
    shelf = models.CharField(max_length=50)  # Shkaf raqami yoki nomi
 
    def __str__(self):
        return f"Hona: {self.room}, Shkaf: {self.shelf}"

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, null=True)
    student_id = models.CharField(max_length=20)  # Unique talaba ID
    birthday = models.DateField(null=True)
    graduation_year = models.CharField(max_length=1000, null=True)  # Bitirgan yili
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('diplom1', 'Diplom Universitet'),
        ('diplom2', 'Diplom Kollej'),
        ('atestat', 'Atestat'),
        ('buyruq1', 'Buyruqdan ko\'chirma 1-kurs'),
        ('buyruq2', 'Buyruqdan ko\'chirma 2-kurs'),
        ('buyruq3', 'Buyruqdan ko\'chirma 3-kurs'),
        ('buyruq4', 'Buyruqdan ko\'chirma 4-kurs'),
        ('buyruq5', 'Bitirgan'),
        ('achsleniya', 'Achisleniya'),
        ('reyting', 'Reyting'),
        ('bmi', 'BMI'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    is_available = models.BooleanField(default=False)  # Hujjat mavjudmi?

    def __str__(self):
        return f"{self.doc_type} ({'Mavjud' if self.is_available else 'Mavjud emas'}) - {self.student}"
 

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, null=True)
    employee_id = models.CharField(max_length=20)  # Unique talaba ID
    birthday = models.DateField(null=True)
    arrived_year = models.CharField(max_length=1000, null=True)  # kelgan yili
    gone_year = models.CharField(max_length=1000, null=True)  # ketgan yili
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
 
class DocumentEmployee(models.Model):
    DOCUMENT_TYPES = [
        ('turdavoy', 'Mexnat daftarcha'),
        ('t-2', 'T-2'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    is_available = models.BooleanField(default=False)  # Hujjat mavjudmi?

    def __str__(self):
        return f"{self.doc_type} ({'Mavjud' if self.is_available else 'Mavjud emas'}) - {self.employee}"

class Abuturiyent(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, null=True)
    birthday = models.DateField(null=True)
    abuturiyent_id = models.CharField(max_length=20)  # Unique talaba ID
    graduation_year = models.CharField(max_length=1000, null=True)  # hujjat topshirgan yil yili
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class DocumentAbuturiyent(models.Model):
    DOCUMENT_TYPES = [
        ('diplom', 'Diplom'),
        ('atestatsiya', 'Atestatsiya'),
    ]
    abuturiyent = models.ForeignKey(Abuturiyent, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    is_available = models.BooleanField(default=False)  # Hujjat mavjudmi?

    def __str__(self):
        return f"{self.doc_type} ({'Mavjud' if self.is_available else 'Mavjud emas'}) - {self.abuturiyent}"
    
class SrtqiStudent(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, null=True)
    birthday = models.DateField(null=True)
    srtqi_id = models.CharField(max_length=20)  # Unique talaba ID
    graduation_year = models.CharField(max_length=1000, null=True)  # hujjat topshirgan yil yili
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class DocumentSrtqiStudent(models.Model):
    DOCUMENT_TYPES = [
        ('diplom1', 'Diplom Universitet'),
        ('diplom2', 'Diplom Kollej'),
        ('atestat', 'Atestat'),
        ('buyruq1', 'Buyruqdan ko\'chirma 1-kurs'),
        ('buyruq2', 'Buyruqdan ko\'chirma 2-kurs'),
        ('buyruq3', 'Buyruqdan ko\'chirma 3-kurs'),
        ('buyruq4', 'Buyruqdan ko\'chirma 4-kurs'),
        ('buyruq5', 'Buyruqdan ko\'chirma 5-kurs'),
        ('bitirgan', 'Bitirgan'),
        ('achsleniya', 'Achisleniya'),
        ('reyting', 'Reyting'),
        ('bmi', 'BMI'),
    ]
    srtqistudent = models.ForeignKey(SrtqiStudent, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    is_available = models.BooleanField(default=False)  # Hujjat mavjudmi?

    def __str__(self):
        return f"{self.doc_type} ({'Mavjud' if self.is_available else 'Mavjud emas'}) - {self.srtqistudent}"
    
class Magister(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, null=True)
    birthday = models.DateField(null=True)
    srtqi_id = models.CharField(max_length=20)  # Unique talaba ID
    graduation_year = models.CharField(max_length=1000, null=True)  # hujjat topshirgan yil yili
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class DocumentMagister(models.Model):
    DOCUMENT_TYPES = [
        ('diplom1', 'Diplom Universitet'),
        ('diplom2', 'Diplom Kollej'),
        ('atestat', 'Atestat'),
        ('buyruq1', 'Buyruqdan ko\'chirma 1-kurs'),
        ('buyruq2', 'Buyruqdan ko\'chirma 2-kurs'),
        ('buyruq5', 'Bitirgan'),
        ('achsleniya', 'Achisleniya'),
        ('reyting', 'Reyting'),
        ('md', 'MD'),
    ]
    magister = models.ForeignKey(Magister, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    is_available = models.BooleanField(default=False)  # Hujjat mavjudmi?

    def __str__(self):
        return f"{self.doc_type} ({'Mavjud' if self.is_available else 'Mavjud emas'}) - {self.magister}"
