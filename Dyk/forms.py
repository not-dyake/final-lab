from django import forms
from .models import DocumentRequest, DocumentFile, Payment,DocumentType
from django.forms import ModelForm

class DocumentRequestForm(ModelForm):
    class Meta:
        model = DocumentRequest
        fields = ['document_type']

class DocumentFileForm(ModelForm):
    class Meta:
        model = DocumentFile
        fields = ['file']

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method']

class AdminLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)