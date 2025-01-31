from django.contrib import admin
from.models import Resident,DocumentType,DocumentRequest,DocumentFile,Payment

admin.site.register(Resident)
admin.site.register(DocumentType)
admin.site.register(DocumentRequest)
admin.site.register(DocumentFile)
admin.site.register(Payment)
