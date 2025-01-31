from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=11)
    email = models.EmailField(unique=True)  # Ensure unique email per resident
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('document_request')

class DocumentType(models.Model):
    DOCUMENT_CHOICES = [
        ('barangay_id', 'Barangay ID'),
        ('barangay_clearance', 'Barangay Clearance'),
        ('barangay_indigency', 'Barangay Indigency'),
        ('police_clearance', 'Police Clearance'),
    ]

    doc_type = models.CharField(max_length=50, choices=DOCUMENT_CHOICES, unique=True)
    details = models.TextField()

    def __str__(self):
        return dict(self.DOCUMENT_CHOICES).get(self.doc_type, self.doc_type)

class DocumentRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Process', 'In Process'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return f"{self.document_type.doc_type} - {self.status}"

class DocumentFile(models.Model):
    request = models.ForeignKey(DocumentRequest, on_delete=models.CASCADE)  # Ensure this line exists
    file = models.FileField(upload_to='document_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.request}"

class Payment(models.Model):
    request = models.ForeignKey(DocumentRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20,
        choices=[('GCash', 'GCash'), ('Bank Transfer', 'Bank Transfer'), ('Credit Card', 'Credit Card')]
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Paid', 'Paid')],
        default='Pending'
    )

    def __str__(self):
        return f"Payment for {self.request} - {self.amount} - {self.payment_status}"