from django.urls import path

from . import views

from AMS import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.UploadAttendanceRecord.as_view(), name='UploadAttendanceRecord'),
    path("expected_students",views.ExpectedStudents.as_view(),name="expected_students"),
    ]


urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
