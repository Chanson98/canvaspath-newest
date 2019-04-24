from django.db import models


class Zipcode(models.Model):
    def __str__(self):
        return self.zipcode
    zipcode = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)


#Create your models here.
class Student(models.Model):
    def __str__(self):
        return self.name

    email = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=300, null=True, default="123456")
    name = models.CharField(max_length=50, null=True)
    age = models.IntegerField(default=0, null=True)
    gender = models.CharField(max_length=2, null=True)
    major = models.CharField(max_length=50, null=True)
    street = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    # zipcode = models.ForeignKey(Zipcode)
    zipcode = models.CharField(max_length=50, null=True)


class Department(models.Model):
    def __str__(self):
        return self.dept_name
    # id is auto
    dept_head = models.CharField(max_length=50, null=True)
    dept_name = models.CharField(max_length=50, null=True)


class Professor(models.Model):
    email = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=300, null=True, default="123456")
    name = models.CharField(max_length=50, null=True)
    age = models.IntegerField(default=0, null=True)
    gender = models.CharField(max_length=2, null=True)
    office_address = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)  # position
    department = models.ForeignKey(Department)


class Administrator(models.Model):
    email = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True, default="123456")


class Prof_teams(models.Model):
    def __str__(self):
        return self.team_name
    team_name = models.CharField(max_length=50, null=True)


class Prof_team_members(models.Model):
    professor = models.ForeignKey(Professor)
    teaching_team_id = models.ForeignKey(Prof_teams)


class Course(models.Model):
    def __str__(self):
        return self.course_name
    course_id = models.CharField(max_length=50, null=True)
    course_name = models.CharField(max_length=50, null=True)
    course_description = models.CharField(max_length=1000, null=True)


class Sections(models.Model):
    def __str__(self):
        return self.section_name
    course_id = models.ForeignKey(Course)
    section_no = models.IntegerField(default=1)
    section_name = models.CharField(max_length=50, null=True)
    TYPE_CHOICE = (
        ('Reg', 'regular'),
        ('Cap', 'capstone')
    )
    section_type = models.CharField(max_length=10, choices=TYPE_CHOICE, default='Reg')
    limit = models.IntegerField(default=50)
    teaching_team_id = models.ForeignKey(Prof_teams, null=True)


class Enrolls(models.Model):
    student = models.ForeignKey(Student)
    section = models.ForeignKey(Sections)


class Homework(models.Model):
    section = models.ForeignKey(Sections)
    hw_no = models.IntegerField(default=1)
    hw_details = models.CharField(max_length=1000, null=True)


class Homework_grades(models.Model):
    student = models.ForeignKey(Student)
    homework = models.ForeignKey(Homework, null=True)
    grades = models.DecimalField(max_digits=4, decimal_places=2, null=False, default=0.00)  # float


class Exams(models.Model):
    section = models.ForeignKey(Sections)
    exam_no = models.IntegerField(default=1)
    exam_details = models.CharField(max_length=1000, null=True)


class Exam_grades(models.Model):
    student = models.ForeignKey(Student)
    exam = models.ForeignKey(Exams)
    grades = models.DecimalField(max_digits=4, decimal_places=2, null=False, default=0.00)  # float


class Capstone_section(models.Model):
    section = models.ForeignKey(Sections)
    project_no = models.IntegerField(default=1)
    sponsor_id = models.ForeignKey(Professor)


class Capstone_Team(models.Model):
    project_no = models.ForeignKey(Capstone_section)


class Capstone_Team_Members(models.Model):
    team = models.ForeignKey(Capstone_Team)
    student = models.ForeignKey(Student)


class Capstone_grades(models.Model):
    team = models.ForeignKey(Capstone_Team)
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=False, default=0.00)  # float


class FinalScore(models.Model):
    section = models.ForeignKey(Sections)
    student = models.ForeignKey(Student)
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=False, default=0.00)  # float

