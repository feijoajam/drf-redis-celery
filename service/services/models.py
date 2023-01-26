from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client
from services.tasks import set_price
from model_utils import FieldTracker


class Service(models.Model):
    name = models.CharField(max_length=50)
    service_price = models.PositiveIntegerField()

    tracker = FieldTracker()

    def save(self, *args, **kwargs):
        if self.tracker.has_changed('service_price'):
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name + ": " + str(self.service_price)


class TariffPlan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=20)
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

    tracker = FieldTracker()

    def __str__(self):
        return self.plan_type + ": " + str(self.discount_percent)

    def save(self, *args, **kwargs):
        if self.tracker.has_changed('discount_percent'):
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
        return super().save(*args, **kwargs)


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(TariffPlan, related_name='subscriptions', on_delete=models.PROTECT)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.service) + ": " + str(self.plan)
