import time

from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.core.cache import cache


@shared_task(base=Singleton)
def set_price(subscription_id):
    from services.models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().get(id=subscription_id)
        new_price = subscription.service.service_price - (subscription.service.service_price * (subscription.plan.discount_percent / 100.00))
        subscription.price = new_price
        subscription.save()
    cache.delete('price_cache')
