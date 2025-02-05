from django.urls import path
from .views import login_view, upload_resume

urlpatterns = [
    path('upload/', upload_resume.as_view(), name='upload_resume'),
    path('login/', login_view.as_view(), name='login'),
]
