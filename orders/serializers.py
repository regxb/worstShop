from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('initiator', 'status', 'phone_number')

    def get_status(self, obj):
        return obj.get_status_display()
