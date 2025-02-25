from django.db import models

class Location(models.Model):
    room = models.CharField(max_length=50, verbose_name="Hona")  # Honaning nomi yoki raqami
    shelf = models.CharField(max_length=50, verbose_name="Shkaf")  # Shkaf raqami yoki nomi
 
    def __str__(self):
        return f"Hona: {self.room}, Shkaf: {self.shelf}"
    class Meta:
        verbose_name = "Joylashuv"
        verbose_name_plural = "Joylashuvlar"
 
class Student(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    surname = models.CharField(max_length=100, null=True, verbose_name="Sharif")
    student_id = models.CharField(max_length=20, verbose_name="Talaba ID")  # Unique talaba ID
    birthday = models.DateField(null=True, verbose_name="Tug'ilgan kun")
    graduation_year = models.CharField(max_length=1000, null=True, verbose_name="Bitirgan yil")  # Bitirgan yili
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Joylashuv")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta: 
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"

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
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents', verbose_name="Talaba")
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name="Hujjat turi")
    is_available = models.BooleanField(default=False, verbose_name="Tasdiqlash")  # Hujjat mavjudmi?

    def __str__(self):
        return f"{self.doc_type} ({'Mavjud' if self.is_available else 'Mavjud emas'}) - {self.student}"

    class Meta:
        verbose_name = "Hujjat"
        verbose_name_plural = "Hujjatlar"
 
class Employee(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    surname = models.CharField(max_length=100, null=True, verbose_name="Sharif")
    employee_id = models.CharField(max_length=20, verbose_name="Xodim ID")  # Unique talaba ID
    birthday = models.DateField(null=True, verbose_name="Tug'ilgan kun")
    arrived_year = models.CharField(max_length=1000, null=True, verbose_name="Kelgan yili")  # kelgan yili
    gone_year = models.CharField(max_length=1000, null=True, verbose_name="Ketgan yili")  # ketgan yili
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Joylashuv")
 
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Xodim"
        verbose_name_plural = "Xodimlar"
 
class DocumentEmployee(models.Model):
    DOCUMENT_TYPES = [
        ('turdavoy', 'Mexnat daftarcha'),
        ('t-2', 'T-2'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents', verbose_name="Xodim")
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name="Hujjat turi")
    is_available = models.BooleanField(default=False, verbose_name="Tasdiqlash")  # Hujjat mavjudmi?

    def __str__(self):
        return f"{self.doc_type} ({'Mavjud' if self.is_available else 'Mavjud emas'}) - {self.employee}"

    class Meta:
        verbose_name = "Hujjat"
        verbose_name_plural = "Hujjatlar"

class Abuturiyent(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    surname = models.CharField(max_length=100, null=True, verbose_name="Sharif")
    birthday = models.DateField(null=True, verbose_name="Tug'ilgan kun")
    abuturiyent_id = models.CharField(max_length=20, verbose_name="Abituriyent ID")  # Unique talaba ID
    graduation_year = models.CharField(max_length=1000, null=True, verbose_name="Hujjat topshirgan yili")  # hujjat topshirgan yil yili
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Joylashuv")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta: 
        verbose_name = "Abituriyent"
        verbose_name_plural = "Abituriyentlar"

class DocumentAbuturiyent(models.Model):
    DOCUMENT_TYPES = [
        ('diplom', 'Diplom'),
        ('atestatsiya', 'Atestatsiya'),
    ]
    abuturiyent = models.ForeignKey(Abuturiyent, on_delete=models.CASCADE, related_name='documents', verbose_name="Abituriyent")
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name="Hujjat turi")
    is_available = models.BooleanField(default=False, verbose_name="Tasdiqlash")  # Hujjat mavjudmi?

    def __str__(self):
        return f"{self.doc_type} ({'Mavjud' if self.is_available else 'Mavjud emas'}) - {self.abuturiyent}"

    class Meta:
        verbose_name = "Hujjat"
        verbose_name_plural = "Hujjatlar"
    
class SrtqiStudent(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    surname = models.CharField(max_length=100, null=True, verbose_name="Sharif")
    birthday = models.DateField(null=True, verbose_name="Tug'ilgan kun")
    srtqi_id = models.CharField(max_length=20, verbose_name="Sirqi talaba ID")  # Unique talaba ID
    graduation_year = models.CharField(max_length=1000, null=True, verbose_name="Bitirgan yil")  # hujjat topshirgan yil yili
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Joylashuv")

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
    srtqistudent = models.ForeignKey(SrtqiStudent, on_delete=models.CASCADE, related_name='documents', verbose_name="Sirqi talaba")
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name="Hujjat turi")
    is_available = models.BooleanField(default=False, verbose_name="Tasdiqlash")  # Hujjat mavjudmi?

    def __str__(self):
        return f"{self.doc_type} ({'Mavjud' if self.is_available else 'Mavjud emas'}) - {self.srtqistudent}"

    class Meta:
        verbose_name = "Hujjat"
        verbose_name_plural = "Hujjatlar"
    
class Magister(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    surname = models.CharField(max_length=100, null=True, verbose_name="Sharif")
    birthday = models.DateField(null=True, verbose_name="Tug'ilgan kun")
    srtqi_id = models.CharField(max_length=20, verbose_name="Magistr ID")  # Unique talaba ID
    graduation_year = models.CharField(max_length=1000, null=True, verbose_name="Tugatgan yil")  # hujjat topshirgan yil yili
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Joylashuv")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Magistr"
        verbose_name_plural = "Magistrantlar"

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
    magister = models.ForeignKey(Magister, on_delete=models.CASCADE, related_name='documents', verbose_name="Magistr")
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name="Hujjat turi")
    is_available = models.BooleanField(default=False, verbose_name="Tasdiqlash")  # Hujjat mavjudmi?

    def __str__(self):
        return f"{self.doc_type} ({'Mavjud' if self.is_available else 'Mavjud emas'}) - {self.magister}"

    class Meta: 
        verbose_name = "Hujjat"
        verbose_name_plural = "Hujjatlar"
