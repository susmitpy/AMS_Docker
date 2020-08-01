from django.core.files.storage import default_storage
from models import *
import pandas as pd
import json
import datetime
from copy import deepcopy

def convert24(str1):

    # Checking if last two elements of time
    # is AM and first two elements are 12
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]

    # remove the AM
    elif str1[-2:] == "AM":
        return str1[:-2]

    # Checking if last two elements of time
    # is PM and first two elements are 12
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]

    else:

        # add 12 to hours and remove PM
        return str(int(str1[:2]) + 12) + str1[2:8]

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

def insertLecture(syjc,subject,division,lecturer,date,start_time,end_time,num_students,present_record):
    lec = Lecture(
        syjc = syjc,
        subject = subject,
        lecturer = lecturer,
        division=division,
        date = date,
        start_time = start_time,
        end_time = end_time,
        num_students = num_students,
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

    print(type(file))
    f = deepcopy(file)
    df = pd.read_csv(file)

    attnd = pd.read_csv(f,skiprows=3)

    date = df["Start Time"][0].split(" ")[0]
    date = datetime.datetime.strptime(date,"%m/%d/%Y").date()

    start_time_period = " ".join(df["Start Time"][0].split(" ")[1:])
    if len(start_time_period)==10:
        start_time_period = "0" + start_time_period
    start_time = convert24(start_time_period)
    start_time_str = start_time[:2]+start_time[3:5]
    start_time = int(start_time_str)

    end_time_period = " ".join(df["End Time"][0].split(" ")[1:])
    if len(end_time_period)==10:
        end_time_period = "0" + end_time_period
    end_time = convert24(end_time_period)
    end_time = int(end_time[:2]+end_time[3:5])

    num_students = int(df["Participants"][0])

    file_name = date.strftime("%d_%m_%y") + "_" + lecturer + "_" + start_time_str + ".csv"
    fp = "./attendance/{}/{}/{}/{}"  # attendance/syjc/E/M2/file_name
    fp = fp.format(std,division,subject,file_name)
    default_storage.delete(fp)
    default_storage.save(fp, file)


    attnd = attnd.rename(columns={"Name (Original Name)":"Student","Duration (Minutes)":"Duration"})
    attnd = attnd[["Student","Duration"]]

    attnd["Roll"] = attnd["Student"].map(get_roll_num)

    attnd = attnd[["Duration","Roll"]]
    attnd = attnd.groupby("Roll")["Duration"].sum()
    attnd = pd.DataFrame(attnd)
    attnd = attnd[attnd["Duration"] >= 30]
    attnd.drop("Duration",axis=1,inplace=True)

    present = list(attnd.index)
    start,end,skip = get_expected_students_rolls_range(syjc,subject,division,lecturer)
    present_record = get_present_record(start,end,skip,present)

    insertLecture(syjc,subject,division,lecturer,date,start_time,end_time,num_students,present_record)

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
   if len(df) == 0:
       return pd.DataFrame()
   df.drop("_id",axis=1,inplace=True)

   subjects = {i:j for i,j in Global.subject_choices}
   lecturers = {i:j for i,j in Global.lecturer_choices}

   df["subject"] = df["subject"].map(subjects)
   df["lecturer"] = df["lecturer"].map(lecturers)
   df["syjc"] = df["syjc"].map({True:"SYJC",False:"FYJC"})
   df = df.rename(columns={"syjc":"Class"})

   return df
