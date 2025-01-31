from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView, UpdateView, DeleteView
from .models import Resident, DocumentType, DocumentRequest, DocumentFile, Payment
from .forms import DocumentRequestForm, DocumentFileForm, PaymentForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponse
from .forms import AdminLoginForm

class HomePageView(TemplateView):
    template_name = 'app/home.html'

class ResidentRegisterView(CreateView):
    model = Resident
    fields = ['first_name', 'last_name', 'address', 'contact_number', 'email']
    template_name = 'app/register.html'

class AdminLoginView(FormView):
    template_name = 'app/login.html'
    form_class = AdminLoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None and user.is_staff:
            login(self.request, user)
            return redirect('admin_dashboard') 
        else:
            return render(self.request, self.template_name, {'form': form, 'error': 'Invalid credentials or not an admin.'})


@method_decorator(login_required, name='dispatch')
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'app/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['residents'] = Resident.objects.all()
        context['document_types'] = DocumentType.objects.all()
        context['document_files'] = DocumentFile.objects.all()
        context['payments'] = Payment.objects.all()
        return context
    
class ResidentUpdateView(UpdateView):
    model = Resident
    fields = ['first_name', 'last_name', 'address', 'contact_number', 'email']
    template_name = 'app/resident_update.html'
    success_url = reverse_lazy('admin_dashboard')

class ResidentDeleteView(DeleteView):
    model = Resident
    template_name = 'app/resident_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')

class DocumentRequestFormView(FormView):
    template_name = 'app/document_request_form.html'
    form_class = DocumentRequestForm

    def form_valid(self, form):
        resident = Resident.objects.get(id=self.request.user.id)
        document_type = form.cleaned_data['document_type']
        document_request = DocumentRequest.objects.create(resident=resident, document_type=document_type)
        return redirect(reverse_lazy('document_file_upload', kwargs={'request_id': document_request.id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document_types'] = DocumentType.objects.all()
        return context

class DocumentFileUploadView(FormView):
    template_name = 'app/document_file_upload.html'
    form_class = DocumentFileForm

    def form_valid(self, form):
        document_request = DocumentRequest.objects.get(id=self.kwargs['request_id'])
        document_file = DocumentFile(file=form.cleaned_data['file'], request=document_request)
        document_file.save()
        return redirect(reverse_lazy('payment_form', kwargs={'request_id': document_request.id}))

class PaymentFormView(FormView):
    template_name = 'app/payment_form.html'
    form_class = PaymentForm

    def form_valid(self, form):
        document_request = DocumentRequest.objects.get(id=self.kwargs['request_id'])
        payment = form.save(commit=False)
        payment.request = document_request
        payment.save()
        if payment.payment_status == 'Paid':
            document_request.status = 'In Process'
        return redirect('document_request_success')

class DocumentRequestSuccessView(TemplateView):
    template_name = 'app/document_request_success.html'