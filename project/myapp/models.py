from django.db import models

# Create your models here.

#1. user_login - id, uname, passwd, u_type
class user_login(models.Model):
    uname = models.CharField(max_length=100)
    passwd = models.CharField(max_length=25)
    u_type = models.CharField(max_length=10)

    def __str__(self):
        return self.uname

class user_details(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=200)
    gender = models.CharField(max_length=25)
    age = models.IntegerField()
    addr = models.CharField(max_length=500)
    pin = models.IntegerField()
    contact = models.IntegerField()
    email = models.CharField(max_length=25)

    def __str__(self):
        return self.fname


#2. designation_type - id, designation
class designation_type(models.Model):
    id = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=100)


#3. staff_details - id, user_id, desg_id, fname, lname, addr, pin, email, contact, status
class staff_details(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    desg_id = models.IntegerField()
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    addr = models.CharField(max_length=1000)
    pin = models.CharField(max_length=10)
    email = models.CharField(max_length=250)
    contact = models.CharField(max_length=20)
    status = models.CharField(max_length=10)


#4. student_details -  id, user_id, rollno, fname, lname, dob, gender, addr, pin, email, contact, status
class student_details(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    rollno = models.CharField(max_length=20)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    dob = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    addr = models.CharField(max_length=1000)
    pin = models.CharField(max_length=10)
    email = models.CharField(max_length=250)
    contact = models.CharField(max_length=20)
    status = models.CharField(max_length=10)

#5. staff_student_map - id, staff_id, student_id
class staff_student_map(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.IntegerField()
    student_id = models.IntegerField()


#6. staff_messages - id, staff_id, sub, msg, dt, tm, status
class staff_messages(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.IntegerField()
    sub = models.CharField(max_length=100)
    msg = models.CharField(max_length=350)
    dt = models.CharField(max_length=20)
    tm = models.CharField(max_length=20)
    status = models.CharField(max_length=10)


#7. student_assignment - id, student_id, title, remarks, dt, tm, type_id, status
class student_assignment(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.IntegerField()
    title = models.CharField(max_length=10)
    remarks = models.CharField(max_length=10)
    dt = models.CharField(max_length=10)
    tm = models.CharField(max_length=10)
    type_id = models.IntegerField()
    status = models.CharField(max_length=10)


#8. assignment_details_1 - id, assignment_id, file, analysis_score, status
class assignment_details_1(models.Model):
    id = models.AutoField(primary_key=True)
    assignment_id = models.IntegerField()
    file = models.CharField(max_length=250)
    analysis_score = models.CharField(max_length=10)
    status = models.CharField(max_length=10)


#9. assignment_details_2 - id, assignment_id, file, links, analysis_score, status
class assignment_details_2(models.Model):
    id = models.AutoField(primary_key=True)
    assignment_id = models.IntegerField()
    file = models.CharField(max_length=250)
    links = models.CharField(max_length=250)
    analysis_score = models.CharField(max_length=10)
    status = models.CharField(max_length=10)


#10. assignment_details_3 - id, assignment_id, content, links_content, analysis_score, status
class assignment_details_3(models.Model):
    id = models.AutoField(primary_key=True)
    assignment_id = models.IntegerField()
    content = models.CharField(max_length=1000)
    links_content = models.CharField(max_length=1000)
    analysis_score = models.CharField(max_length=10)
    status = models.CharField(max_length=10)

class data_set(models.Model):
    #id
    text = models.CharField(max_length=400)
    type_name = models.CharField(max_length=100)