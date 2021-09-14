from django.contrib import admin

# Register your models here.
from fees.orm.models import FeeSetup, FeeConfig, FeeCollection, StudentPaidFeeSetup

admin.site.register(FeeSetup)
admin.site.register(FeeConfig)
admin.site.register(FeeCollection)
admin.site.register(StudentPaidFeeSetup)
