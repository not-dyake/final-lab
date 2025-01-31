from django.urls import path
from .views import AdminLoginView, HomePageView, ResidentDeleteView, ResidentRegisterView, DocumentRequestFormView, DocumentFileUploadView, PaymentFormView, DocumentRequestSuccessView, AdminDashboardView, ResidentUpdateView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('register/', ResidentRegisterView.as_view(), name='register'),
    path('document-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('resident-update/<int:pk>/', ResidentUpdateView.as_view(), name='resident_update'),
    path('resident-delete/<int:pk>/', ResidentDeleteView.as_view(), name='resident_delete'),
    path('document-request/', DocumentRequestFormView.as_view(), name='document_request'),
    path('document-file-upload/<int:request_id>/', DocumentFileUploadView.as_view(), name='document_file_upload'),
    path('payment-form/<int:request_id>/', PaymentFormView.as_view(), name='payment_form'),
    path('document-request-success/', DocumentRequestSuccessView.as_view(), name='document_request_success'),
]