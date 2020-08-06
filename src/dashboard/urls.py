from django.urls import path

from . import views

from AMS import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.TeachersReport.as_view(), name='dashboard'),
    path("students_report",views.StudentsReport.as_view(),name="students_report"),
    path("teachers_report",views.TeachersReport.as_view(),name="teachers_report"),
    path("explore_lecturers",views.ExploreLecturers.as_view(),name="explore_lecturers"),
    path("file_browser",views.FileBrowser.as_view(),name="file_browser"),
    path("set_password",views.set_password,name="set_password")
    ]


urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
