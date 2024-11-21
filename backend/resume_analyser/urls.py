from django.urls import path
from .views import upload_resume

urlpatterns = [
    path('upload/', upload_resume.as_view(), name='upload_resume'),
]
