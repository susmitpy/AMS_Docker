from django.shortcuts import render
from django.views import View
from .forms import DateRangeSelector, DateSelector, StudentsReportSelector
from .db import get_teachers_report_file_path, get_lectures_data, get_students_report_file_path

def home(req):
    return render(req,"dashboard/home.html")

class StudentsReport(View):
    def get(self,req):
        context = self.get_get_context()
        return render(req,"dashboard/students_report_selector.html",context)

    def post(self,req):
        form = StudentsReportSelector(req.POST)
        if form.is_valid():
            from_date = form.cleaned_data["from_date"]
            to_date = form.cleaned_data["to_date"]
            division = form.cleaned_data["division"]
            context = self.get_post_context(from_date,to_date,division)
        else:
            context = {}
        return render(req,"dashboard/students_report_selector.html",context)

    def get_get_context(self):
        form = StudentsReportSelector()
        return {"form":form}

    def get_post_context(self,fd,td,d):
        form = StudentsReportSelector()
        fp = get_students_report_file_path(fd,td,d)
        return {"form":form,"fp":fp}

class TeachersReport(View):
    def get(self,req):
        context = self.get_get_context()
        return render(req,"dashboard/teachers_report_selector.html",context)

    def post(self,req):
        form = DateRangeSelector(req.POST)
        if form.is_valid():
            from_date = form.cleaned_data["from_date"]
            to_date = form.cleaned_data["to_date"]
            context = self.get_post_context(from_date,to_date)
            print(context["fp"])
        else:
            context = {}
        return render(req,"dashboard/teachers_report_selector.html",context)

    def get_get_context(self):
        form = DateRangeSelector()
        date_selector = DateSelector()
        return {"form":form,"date_selector":date_selector}

    def get_post_context(self,fd,td):
        # use mongoDB aggregation
        fp = get_teachers_report_file_path(fd,td)
        form = DateRangeSelector()
        date_selector = DateSelector()
        return {"fp":fp,"form":form,"date_selector":date_selector}

class ExporeLecturers(View):
    def post(self,req):
        form = DateSelector(req.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            context = self.get_post_context(date)
        else:
            context = {}
        return render(req,"dashboard/teachers_lectures_explore.html",context)

    def get_post_context(self,date):
        data = get_lectures_data(date)
        form = DateRangeSelector()
        date_selector = DateSelector()
        return {"data":data,"form":form,"date_selector":date_selector,"date":str(date)}
