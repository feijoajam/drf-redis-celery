from celery import shared_task


@shared_task
def set_price(subscription_id):
    from services.models import Subscription

    subscription = Subscription.objects.get(id=subscription_id)
    new_price = subscription.service.service_price - (subscription.service.service_price * (subscription.plan.discount_percent / 100.00))
    subscription.price = new_price
    subscription.save()
