from django.db.models import Prefetch, Sum
from django.core.cache import cache
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client',
                 queryset=Client.objects.all().select_related('user').only('company_name', 'user__email')
                 )
    )

    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        response_data = {'result': response.data}

        price_cache = cache.get('price_cache')
        if price_cache:
            response_data['total_amount'] = price_cache
        else:
            response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
            cache.set('price_cache', response_data['total_amount'], 3600)

        response.data = response_data
        return response
