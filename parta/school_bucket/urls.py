from django.urls import path
from school_bucket.views import Subjects, bucket


urlpatterns = [
    path("subjects/<str:grade>/", Subjects.as_view(), name="subject"),
    path("bucket/", bucket, name="bucket"),
]
