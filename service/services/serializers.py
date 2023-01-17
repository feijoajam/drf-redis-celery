from rest_framework import serializers

from services.models import Subscription, TariffPlan


class TariffPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffPlan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = TariffPlanSerializer()
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    price = serializers.SerializerMethodField()

    def get_price(self, instance):
        return instance.service.price - instance.service.price * (instance.plan.discount_percent / 100)

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')
