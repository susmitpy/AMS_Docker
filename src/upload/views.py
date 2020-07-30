from django.shortcuts import render
from django.http import JsonResponse

from django.views import View

from .forms import LectureSelectorForm, ExpectedStudentsInsertForm
from .db import log_attendance, insert_expected_students,get_expected_students

class ExpectedStudents(View):
    def get(self,req):
        context = self.get_context()
        return render(req,"upload/expected_students.html",context)

    def post(self,req):
        form = ExpectedStudentsInsertForm(req.POST)
        if form.is_valid():
            insert_expected_students(form.cleaned_data)
        context = self.get_context()
        return render(req,"upload/expected_students.html",context)

    def get_context(self):
        df = get_expected_students()
        df = df.to_html(classes=["mystyle table table-bordered table-striped"],index=False)
        return {"form":ExpectedStudentsInsertForm(),"data":df}

class UploadAttendanceRecord(View):
    def get(self,req):
        context = self.get_context()
        return render(req,"upload/upload_attendance_record.html",context)

    def post(self,req):
        form = LectureSelectorForm(req.POST, req.FILES)
        if form.is_valid():
            log_attendance(form.cleaned_data,req.FILES['file'])
        return JsonResponse({"status":"Success"},status=200)

    def get_context(self):
        return {"form":LectureSelectorForm()}
