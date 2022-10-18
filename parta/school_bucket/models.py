from django.db import models


class Grades(models.TextChoices):
    nine = "9"
    eleven = "11"


class Subject(models.Model):
    name = models.CharField(max_length=32)
    grade = models.CharField(max_length=8, choices=Grades.choices)
    price = models.PositiveSmallIntegerField(null=True, blank=True)


class Teacher(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    grade = models.CharField(max_length=8, choices=Grades.choices)
    subject = models.ManyToManyField(Subject)


class Price(models.Model):
    count = models.PositiveSmallIntegerField()
    price_for_one = models.PositiveIntegerField()


class Plan(models.Model):
    name = models.CharField(max_length=32)
    grade = models.CharField(max_length=8, choices=Grades.choices)
    prices = models.ManyToManyField(Price)
