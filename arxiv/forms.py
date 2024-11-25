from django import forms
from .models import Student, Location, Document

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'graduation_year', 'location']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['room', 'shelf', 'row']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['student', 'doc_type', 'is_available']

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}))