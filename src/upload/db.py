from django.core.files.storage import default_storage
from models import *
import pandas as pd
import json

id_col_name = "ID"
duration_col_name = "Duration"

def get_roll_num(x):
    try:
        a = x.split(" - ")
        r = a[1].strip()
        roll_int = int(r)
        return roll_int
    except Exception:
        return None

def get_expected_students_rolls_range(syjc,subject,division,lecturer):
    expected_doc = ExpectedStudents.objects.get(syjc=syjc,subject=subject,division=division,lecturer=lecturer)
    return (
        expected_doc.start_roll_num,
        expected_doc.end_roll_num,
        expected_doc.skip_roll_nums
    )

def insertLecture(syjc,subject,division,lecturer,date,start_time,end_time,present_record):
    lec = Lecture(
        syjc = syjc,
        subject = subject,
        lecturer = lecturer,
        date = date,
        start_time = int(start_time),
        end_time = int(end_time),
        present = present_record
    )

    lec.save()

def get_present_record(start,end,skip,present):
    present_record = {}
    for i in range(start,end+1):
        if i not in skip:
            if i in present:
                    present_record[str(i)] = True
            else:
                    present_record[str(i)] = False

    return present_record

def log_attendance(data,file):
    std = data["std"]
    syjc = std == "SYJC"
    subject = data["subject"]
    division = data["division"]
    lecturer = data["lecturer"]
    date = data["date"]
    start_time = str(data["start_time"])
    start_time = start_time[:2] + start_time[3:5]
    end_time = str(data["end_time"])
    end_time = end_time[:2] + end_time[3:5]

    file_name = date.strftime("%d_%m_%y") + "_" + lecturer + "_" + start_time + ".xlsx"
    fp = "./attendance/{}/{}/{}/{}"  # attendance/syjc/E/M2/file_name
    fp = fp.format(std,division,subject,file_name)
    default_storage.delete(fp)
    default_storage.save(fp, file)

    df = pd.read_excel(file)
    df["Roll"] = df[id_col_name].map(get_roll_num)
    df = df[["Duration","Roll"]]
    df = df.groupby("Roll")["Duration"].sum()
    df = pd.DataFrame(df)
    df = df[df["Duration"] >= 30]
    df.drop("Duration",axis=1,inplace=True)

    present = list(df.index)
    start,end,skip = get_expected_students_rolls_range(syjc,subject,division,lecturer)
    present_record = get_present_record(start,end,skip,present)

    insertLecture(syjc,subject,division,lecturer,date,start_time,end_time,present_record)

def insert_expected_students(data):
     syjc = data["std"] == "SYJC"
     if data["skip_roll_nums"] == None:
         skip_roll_nums = []
     else:
         skip_roll_nums = [int(i.strip()) for i in data["skip_roll_nums"].split(" ")]
     expected_students = ExpectedStudents(
        syjc = syjc,
        subject = data["subject"],
        division = data["division"],
        lecturer = data["lecturer"],
        start_roll_num = data["start_roll_num"],
        end_roll_num = data["end_roll_num"],
        skip_roll_nums = skip_roll_nums
     )

     expected_students.save()

def get_expected_students():
   a = json.loads(ExpectedStudents.objects.to_json())
   df = pd.DataFrame(a)
   df.drop("_id",axis=1,inplace=True)

   subjects = {i:j for i,j in Global.subject_choices}
   lecturers = {i:j for i,j in Global.lecturer_choices}

   df["subject"] = df["subject"].map(subjects)
   df["lecturer"] = df["lecturer"].map(lecturers)
   df["syjc"] = df["syjc"].map({True:"SYJC",False:"FYJC"})
   df = df.rename(columns={"syjc":"Class"})

   return df
