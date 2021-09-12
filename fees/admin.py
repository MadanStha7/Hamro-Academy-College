from django.contrib import admin

# Register your models here.
from fees.orm.models import FeeSetup, FeeConfig

admin.site.register(FeeSetup)
admin.site.register(FeeConfig)
