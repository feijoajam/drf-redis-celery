from django.contrib import admin

from services.models import Service, Subscription, TariffPlan

# Register your models here.
admin.site.register(Service)
admin.site.register(TariffPlan)
admin.site.register(Subscription)
