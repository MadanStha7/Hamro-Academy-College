from django.contrib import admin
from django.apps import apps

# class StudentInvoiceAdmin(admin.ModelAdmin):
#     list_display = ("student__id", "fee__amount")


models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
