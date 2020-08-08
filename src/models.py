import mongoengine as mongo

class Global:
    std_choices = [("SYJC","SYJC"),("FYJC","FYJC")]
    host_path = "http://ec2-15-207-80-251.ap-south-1.compute.amazonaws.com/"

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

    meta = {
        'collection': 'lectures'
        }

class ExpectedStudents(mongo.Document):
    syjc = mongo.BooleanField()
    subject = mongo.StringField()
    division = mongo.StringField()
    lecturer = mongo.StringField()
    start_roll_num = mongo.IntField()
    end_roll_num = mongo.IntField()
    skip_roll_nums = mongo.ListField(mongo.IntField())

    meta = {'collection': 'expected_students'}
