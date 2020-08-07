from models import Lecture
from io import BytesIO
from django.core.files.storage import default_storage
import pandas as pd
import json
from models import Global
import re
from mongoengine.queryset.visitor import Q

from upload.models import Subject

from django.db.utils import OperationalError
from django.contrib.auth.models import User
from django.db.models import F

def get_subjects_mapper():
    subs = Subject.objects.values_list("code","name")
    subjects = {i:j for i,j in subs}
    return subjects

def get_lecturers_mapper():
    lects = User.objects.exclude(profile__code="ADMIN").select_related("profile").annotate(code=F("profile__code"),name=F("profile__fullname")).values_list("code","name")
    lecturers = {i:j for i,j in lects}
    return lecturers

def get_lectures_data(date,std):
    syjc = std == "SYJC"
    query = Lecture.objects(date=date,syjc=syjc).only("division","subject","lecturer","date","start_time","end_time","num_students")
    data = []
    for lec in query:
        obj = {}
        obj["division"] = lec.division
        obj["subject"] = lec.subject
        obj["lecturer"] = lec.lecturer
        obj["date"] = lec.date
        obj["start_time"] = lec.start_time
        obj["end_time"] = lec.end_time
        obj["num_students"] = lec.num_students
        data.append(obj)

    df = pd.DataFrame(data)

    if len(df) == 0:
        return None

    df["date"] = df["date"].map(lambda x: x.strftime("%d/%m/%y"))
    df["start_time"] = df["start_time"].map(lambda x: str(x)[:2] + ":" + str(x)[2:])
    df["end_time"] = df["end_time"].map(lambda x: str(x)[:2] + ":" + str(x)[2:])
    df = df.rename(columns={"division":"Division","subject":"Subject","lecturer":"Lecturer","date":"Date","start_time":"From","end_time":"To","num_students":"Students"})
    df = df[["Division","Subject","Lecturer","Date","From","To","Students"]]

    df["Subject"] = df["Subject"].map(get_subjects_mapper())
    df["Lecturer"] = df["Lecturer"].map(get_lecturers_mapper())

    df = df.to_html(classes=["mystyle table table-bordered table-striped"],index=False,table_id="mytable")
    df = re.sub('<tbody>', '<tbody id="log">',df)

    replace = """
        <thead>
            <tr class="filters" style="text-align: right;">
                <th><input type="text" class="form-control" placeholder="Division" disabled></th>
                <th><input type="text" class="form-control" placeholder="Subject" disabled></th>
                <th><input type="text" class="form-control" placeholder="Lecturer" disabled></th>
                <th><input type="text" class="form-control" placeholder="Date" disabled></th>
                <th><input type="text" class="form-control" placeholder="From" disabled></th>
                <th><input type="text" class="form-control" placeholder="To" disabled></th>
                <th><input type="text" class="form-control" placeholder="Students" disabled></th>
            </tr>
        </thead>
    """

    df = re.sub(r"<thead>.+<\/thead>",replace,df,flags=re.S)
    df = df.replace("\\n","<br>")
    return df

def index_mapper(r,subjects_mapper,lecturers_mapper):
    return (r[0],subjects_mapper.get(r[1]),lecturers_mapper.get(r[2]))

def get_teachers_report_file_path(from_date,to_date,std):

    syjc = std == "SYJC"
    query = Lecture.objects(date__gte=from_date,date__lte=to_date,syjc=syjc).only("division","lecturer","subject")
    df = pd.DataFrame(json.loads(query.to_json()))

    if len(df) == 0:
        return "NA"

    df.drop("_id",axis=1,inplace=True)

    df = df.rename({"subject":"Subject","lecturer":"Lecturer","division":"Division"},axis=1)
    # Use mongoDB framework aggregation for this
    a = df.groupby(["Division","Subject","Lecturer"]).size()
    b = pd.DataFrame(a,columns=["Count"])

    subjects_mapper = get_subjects_mapper()
    lecturers_mapper = get_lecturers_mapper()
    b.index = b.index.map(index_mapper,subjects_mapper,lecturers_mapper)

    fd = from_date.strftime("%d_%m_%y")
    td = to_date.strftime("%d_%m_%y")

    in_memory_fp = BytesIO()
    b.to_excel(in_memory_fp)
    in_memory_fp.seek(0,0)
    file = in_memory_fp
    file_path = f"teachers_reports/{std}__{fd}__{td}.xlsx"
    default_storage.delete(file_path)
    file_name = default_storage.save(file_path, file)

    return "media/" + file_path

def get_students_report_file_path(from_date,to_date,division,std):
    syjc = std == "SYJC"
    filtered = Lecture.objects(Q(date__lte=to_date) & Q(date__gte=from_date) & Q(division=division.name) & Q(syjc=syjc)).only("present")
    pipeline = [
        {
                "$project":{
                        "record": {
                                    "$objectToArray":"$present"
                                }
                        }
        },
        {
                "$unwind" : "$record"
        },
        {
                "$group" :{
                            "_id":"$record.k",
                            "count":{"$sum":1},
                            "present":{
                                        "$sum": {"$cond" : [ "$record.v", 1, 0 ] }
                                    }
                        }
        }
        ]

    ans = filtered.aggregate(pipeline)
    data = [i for i in ans]
    df = pd.DataFrame(data)

    if len(df) == 0:
        return "NA"

    df = df.rename(columns={"_id":"Roll","count":"Total","present":"Present"})
    df = df.sort_values("Roll")

    fd = from_date.strftime("%d_%m_%y")
    td = to_date.strftime("%d_%m_%y")

    in_memory_fp = BytesIO()
    df.to_excel(in_memory_fp,index=False)
    in_memory_fp.seek(0,0)
    file = in_memory_fp
    file_path = f"students_reports/{division}/{fd}__{td}.xlsx"
    default_storage.delete(file_path)
    file_name = default_storage.save(file_path, file)

    return "media/" + file_path
