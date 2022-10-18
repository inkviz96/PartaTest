from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from school_bucket.serializers import SubjectSerializer
from school_bucket.models import Subject, Plan


class Subjects(APIView):
    def get(self, _, *args, **kwargs):
        grade = kwargs.get("grade", None)
        subjects = SubjectSerializer(Subject.objects.filter(grade=grade), many=True)
        return Response(subjects.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def bucket(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    plans = [plan for plan in body.values()]
    response = {}
    for subject_pk, plan_pk in body.items():
        subject = Subject.objects.get(pk=subject_pk)
        plan_with_count = Plan.objects.get(pk=plan_pk).prices.values('price_for_one').get(count=plans.count(plan_pk))
        plan_without_count = Plan.objects.get(pk=plan_pk).prices.values('price_for_one').get(count=1)
        response[subject.name] = {
            "prise_with_discount": subject.price if subject.price else plan_with_count["price_for_one"],
            "prise_without_discount": subject.price if subject.price else plan_without_count["price_for_one"]
        }
    return Response(response, status=status.HTTP_200_OK)
