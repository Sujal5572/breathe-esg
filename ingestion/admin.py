from django.contrib import admin
from .models import DataSource, ImportBatch, RawRecord

admin.site.register(DataSource)
admin.site.register(ImportBatch)
admin.site.register(RawRecord)