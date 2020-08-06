from django.shortcuts import render
from django.http import JsonResponse

from django.views import View

from .forms import LectureSelectorForm, ExpectedStudentsInsertForm, DivisionSelectorForm
from .db import log_attendance, insert_expected_students,get_expected_students

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class ExploreExpectedStudents(View):
    def post(self,req):
        form = DivisionSelectorForm(req.POST)
        if form.is_valid():
            div = form.cleaned_data["division"]
            context = self.get_post_context(div)
        else:
            context = {}
        return render(req,"upload/expected_students_explore.html",context)

    def get_post_context(self,div):
        df = get_expected_students(div)
        df = df.to_html(classes=["mystyle table table-bordered table-striped"],index=False)
        divi = DivisionSelectorForm()
        form = ExpectedStudentsInsertForm()
        return {"data":df,"form":form,"div":divi,"division":div}

@method_decorator(login_required, name='dispatch')
class ExpectedStudents(View):
    def get(self,req):
        context = self.get_context()
        return render(req,"upload/expected_students.html",context)

    def post(self,req):
        form = ExpectedStudentsInsertForm(req.POST)

        if form.is_valid():

            res = insert_expected_students(form.cleaned_data)
            if res:
                messages.info(req, 'Expected Students Successfully Inserted')

        context = self.get_context()
        return render(req,"upload/expected_students.html",context)

    def get_context(self):
        div= DivisionSelectorForm()
        return {"form":ExpectedStudentsInsertForm(),"div":div}

@method_decorator(login_required, name='dispatch')
class UploadAttendanceRecord(View):
    def get(self,req):
        context = self.get_context()
        return render(req,"upload/upload_attendance_record.html",context)

    def post(self,req):
        lecturer_code = req.user.profile.code
        form = LectureSelectorForm(req.POST, req.FILES)
        if form.is_valid():
            res = log_attendance(lecturer_code,form.cleaned_data,req.FILES['file'])
            if res:
                messages.info(req, 'Attendance Successfully Logged')
        context = self.get_context()
        return render(req,"upload/upload_attendance_record.html",context)

    def get_context(self):
        return {"form":LectureSelectorForm()}
