import mongoengine as mongo

class Global:
    subject_choices = [
        ("ENG","English"),
        ("M1", "Maths 1"),
        ("M2", "Maths 2"),
        ("BK", "Book Keeping"),
        ("OCM", "OCM"),
        ("SP", "SP"),
        ("MAR","Marathi"),
        ("HIN","Hindi")
    ]
    std_choices = [("SYJC","SYJC"),("FYJC","FYJC")]
    division_choices = [
    ("A","A"),
    ("B","B"),
    ("C","C"),
    ("D","D"),
    ("E","E"),
    ("F","F"),
    ("G","G"),
    ("H","H"),
    ("I","I"),
    ("J","J"),
    ]
    lecturer_choices = [
    ("RV","Rajeev Vengurlekar"),
    ("RB","Rajendra Bhende"),
    ("BJ","Bharat Joshi")
    ]

class Lecture(mongo.Document):
    syjc = mongo.BooleanField()
    subject = mongo.StringField()
    division = mongo.StringField()
    lecturer = mongo.StringField()
    date = mongo.DateTimeField()
    start_time = mongo.IntField()
    end_time = mongo.IntField()
    num_students = mongo.IntField()
    present = mongo.MapField(mongo.BooleanField())

    meta = {'collection': 'lectures'}

class ExpectedStudents(mongo.Document):
    syjc = mongo.BooleanField()
    subject = mongo.StringField()
    division = mongo.StringField()
    lecturer = mongo.StringField()
    start_roll_num = mongo.IntField()
    end_roll_num = mongo.IntField()
    skip_roll_nums = mongo.ListField(mongo.IntField())

    meta = {'collection': 'expected_students'}
