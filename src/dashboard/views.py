from django.shortcuts import render,redirect
from django.views import View
from .forms import TeachersReportSelector, ExploreLecturesForm, StudentsReportSelector,UserLoginForm
from .db import get_teachers_report_file_path, get_lectures_data, get_students_report_file_path
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth import update_session_auth_hash
from models import Global


@method_decorator(login_required, name='dispatch')
class FileBrowser(View):
    fs = FileSystemStorage(location="media/")
    def get(self,req):
        context = self.get_get_context()
        return render(req,"dashboard/file_browser.html",context)

    def post(self,req):
        context = self.get_post_context(req.POST)
        return render(req,"dashboard/file_browser.html",context)

    def get_get_context(self):
        folders = self.fs.listdir("")[0]
        current_path = ""
        return {"folders":folders,"current_path":current_path}

    def get_post_context(self,data):
        op_type = data.get("type")
        if op_type == "back":
            return self.back_op(data)
        else:
            folder_selected = data.get("folder")
            cp = data.get("current_path")
            cp = cp+folder_selected+"/"
            contents = self.fs.listdir(cp)
            if len(contents[0]) == 0:
                # Only Files are there
                files = contents[1]
                files_data = {}
                for file in files:
                    files_data[file] = Global.host_path + "media/" + cp + file
                return {"files":files_data,"current_path":cp}
            else:
                folders = contents[0]
                return {"folders":folders,"current_path":cp}
    def back_op(self,data):
        cp = data["current_path"]

        if cp in ["","attendance/","students_reports/","teachers_reports/"]:
            return self.get_get_context()
        splitted = cp.split("/")

        cp = "/".join(splitted[:-3])
        if cp != "":
            cp += "/"
        folder = splitted[-3]
        return self.get_post_context({"current_path":cp,"folder":folder,"type":"browse"})

@method_decorator(login_required, name='dispatch')
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
            std = form.cleaned_data["std"]
            context = self.get_post_context(from_date,to_date,division,std)
        else:
            context = {}
        return render(req,"dashboard/students_report_selector.html",context)

    def get_get_context(self):
        form = StudentsReportSelector()
        return {"form":form}

    def get_post_context(self,fd,td,d,std):
        form = StudentsReportSelector()
        fp = get_students_report_file_path(fd,td,d,std)
        fp = Global.host_path + fp
        return {"form":form,"fp":fp}

@method_decorator(login_required, name='dispatch')
class TeachersReport(View):
    def get(self,req):
        context = self.get_get_context()
        return render(req,"dashboard/teachers_report_selector.html",context)

    def post(self,req):
        form = TeachersReportSelector(req.POST)
        if form.is_valid():
            from_date = form.cleaned_data["from_date"]
            to_date = form.cleaned_data["to_date"]
            std = form.cleaned_data["std"]
            context = self.get_post_context(from_date,to_date,std)

        else:
            context = {}
        return render(req,"dashboard/teachers_report_selector.html",context)

    def get_get_context(self):
        form = TeachersReportSelector()
        explore_form = ExploreLecturesForm()
        return {"form":form,"explore_form":explore_form}

    def get_post_context(self,fd,td,std):
        fp = get_teachers_report_file_path(fd,td,std)
        fp = Global.host_path + fp
        form = TeachersReportSelector()
        explore_form = ExploreLecturesForm()
        return {"fp":fp,"form":form,"explore_form":explore_form}

@method_decorator(login_required, name='dispatch')
class ExploreLecturers(View):
    def post(self,req):
        form = ExploreLecturesForm(req.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            std = form.cleaned_data["std"]
            context = self.get_post_context(date,std)
        else:
            context = {}
        return render(req,"dashboard/teachers_lectures_explore.html",context)

    def get_post_context(self,date,std):
        data = get_lectures_data(date,std)
        form = TeachersReportSelector()
        explore_form = ExploreLecturesForm()
        return {"data":data,"form":form,"explore_form":explore_form,"date":str(date)}

def set_password(req):
    if req.method == "POST":
        form = PasswordChangeForm(req.user,req.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(req, user)
            return redirect("UploadAttendanceRecord")



class Login(View):
    def get(self,req):
        context = self.get_get_context()
        return render(req,"registration/login.html",context=context)

    def get_get_context(self):
        form = UserLoginForm()
        return {"form":form}

    def post(self,req):
        form = UserLoginForm(data=req.POST)
        if form.is_valid():
            user = form.get_user()
            login(req, user)

            if user.profile.force_password_change:
                user.profile.force_password_change = False
                user.save()
                form = PasswordChangeForm(user)

                return render(req,"registration/password_change_form.html",{"form":form})

            return redirect('UploadAttendanceRecord')
        return render(req,"registration/login.html",context={"form":form})
