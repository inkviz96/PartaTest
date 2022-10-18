from rest_framework import serializers
from school_bucket.models import Subject, Plan
from itertools import chain


class SubjectSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            "pk",
            "name",
            "grade",
            "price",
        ]

    def get_price(self, instance):
        if instance.price:
            return instance.price
        plans = Plan.objects.filter(grade=instance.grade)
        prices = [s.prices.values('price_for_one').get(count=1) for s in plans]
        price = {plans[x].pk:prices[x] for x in range(len(plans))}
        return price
