from django.test import TestCase
from school_bucket.models import Price, Plan, Subject
from django.urls import reverse


class SubjectTestCase(TestCase):
    def setUp(self):
        price_1 = Price.objects.create(count=1, price_for_one=2000)
        price_2 = Price.objects.create(count=2, price_for_one=1500)
        price_3 = Price.objects.create(count=1, price_for_one=1800)
        price_4 = Price.objects.create(count=2, price_for_one=1200)
        plan = Plan.objects.create(name="General", grade="9")
        plan.prices.add(price_1, price_2)
        plan = Plan.objects.create(name="PRO", grade="9")
        plan.prices.add(price_3, price_4)
        subjects = []
        subjects.append(Subject(name="PI", grade="9"))
        subjects.append(Subject(name="Math", grade="9"))
        subjects.append(Subject(name="Biology", grade="9", price=3200))
        Subject.objects.bulk_create(subjects)

    def test_subject_price_list(self):
        response = self.client.get(reverse("subject", args=[9]))
        subject = Subject.objects.first()
        price_1 = Price.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["pk"], subject.pk)
        self.assertEqual(response.data[0]["name"], subject.name)
        self.assertEqual(response.data[0]["grade"], subject.grade)
        self.assertEqual(response.data[0]["price"][3]["price_for_one"], price_1.price_for_one)



    def test_bucket(self):
        import json
        data = {
            "1": 1,
            "2": 2,
            "3": 1,
        }
        response = self.client.post(reverse("bucket"), json.dumps(data),
                                content_type="application/json")
        self.assertEqual(response.data["PI"]["prise_with_discount"], 1500)
        self.assertEqual(response.data["PI"]["prise_without_discount"], 2000)
        self.assertEqual(response.data["Biology"]["prise_with_discount"], 3200)
        self.assertEqual(response.data["Biology"]["prise_with_discount"], 3200)