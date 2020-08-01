from django.urls import path

from . import views

from AMS import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path("students_report",views.StudentsReport.as_view(),name="students_report"),
    path("teachers_report",views.TeachersReport.as_view(),name="teachers_report"),
    path("explore_lecturers",views.ExporeLecturers.as_view(),name="explore_lecturers")
    ]


urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
