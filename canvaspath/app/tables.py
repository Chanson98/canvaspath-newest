from __future__ import unicode_literals, absolute_import
import django_tables2 as tables
from .models import Student, Professor, Course, Sections, Homework, Homework_grades, Exams, Exam_grades, Capstone_Team, FinalScore


class import_students_table(tables.Table):
    class Meta:
        model = Student
        fields = ['name', 'email', 'major', 'phone']


class import_professors_table(tables.Table):
    class Meta:
        model = Professor
        fields = ['name', 'email', 'title', 'department']


class CourseTable(tables.Table):
    url1 = tables.TemplateColumn('<a id="update" href="/administrator/course_management/update/{{record.pk}}/">update</a>',
                                 verbose_name='op', orderable=False)
    url2 = tables.TemplateColumn('<a id="delete" href="/administrator/course_management/delete/{{record.pk}}/">delete</a>',
                                 verbose_name="op", orderable=False)
    url3 = tables.TemplateColumn('<a id="tasks" href="/administrator/section_management/{{record.pk}}/">sections</a>',
                                 verbose_name="op", orderable=False)
    class Meta:
        model = Course
        fields = ['course_id', 'course_name', "url1", 'url2', 'url3']


class SectionTable(tables.Table):
    url1 = tables.TemplateColumn(
        '<a id="team" href="/administrator/section_prof_team/{{record.pk}}/">prof_team</a>',
        verbose_name='op', orderable=False)
    class Meta:
        model = Sections
        fields = ['section_name', 'section_type', "limit", 'url1']


class StudentCourseTable(tables.Table):
    url1 = tables.TemplateColumn(
        '<a id="update" href="/student/choose_course/{{record.pk}}/">choose</a>',
        verbose_name='op', orderable=False)
    class Meta:
        model = Course
        fields = ['course_id', 'course_name', "url1"]


class MyCourseTable(tables.Table):
    url1 = tables.TemplateColumn(
        '{% if record.section_type == "Reg" %}'
        '<a id="update" href="/student/reg_detail/{{record.pk}}/">detail</a>'
        '{% else %}'
        '<a id="update" href="/student/cap_detail/{{record.pk}}/">detail</a>'
        '{% endif %}',
        verbose_name='op', orderable=False)
    class Meta:
        model = Sections
        fields = ['course_id.course_name', 'section_name', 'section_type', "url1"]


class ProfessorCourseTable(tables.Table):
    url1 = tables.TemplateColumn(
        '{% if record.section_type == "Reg" %}'
        '<a id="update" href="/professor/homeworks/{{record.pk}}/">homeworks</a>'
        '{% else %}'
        '<a id="update" href="/professor/cap/{{record.pk}}/">cap</a>'
        '{% endif %}',
        verbose_name='op', orderable=False)
    url2 = tables.TemplateColumn(
        '<a id="delete" href="/professor/exams/{{record.pk}}/">exams</a>',
        verbose_name="op", orderable=False)
    url3 = tables.TemplateColumn(
        '<a id="update" href="/professor/score_sheet/{{record.pk}}/">score_sheet</a>',
        verbose_name='op', orderable=False)

    class Meta:
        model = Sections
        fields = ['course_id.course_name', 'section_name', 'section_type', "url1", 'url2', 'url3']


class HomeworkTable(tables.Table):
    url1 = tables.TemplateColumn(
        '<a id="score" href="/professor/homework/score/{{record.pk}}/">score</a>',
        verbose_name="op", orderable=False)
    class Meta:
        model = Homework
        fields = ['pk', 'hw_details', "url1"]


class HomeworkGradeTable(tables.Table):
    url1 = tables.TemplateColumn(
        '<a class="url_info" href="javascript:void(0)" onclick="change_score('"'{{record.pk}}'"')">change score</a>',
        verbose_name='op', orderable=False)
    class Meta:
        model = Homework_grades
        fields = ['student.name', 'grades', "url1"]


class ExamTable(tables.Table):
    url1 = tables.TemplateColumn(
        '<a id="score" href="/professor/exam/score/{{record.pk}}/">score</a>',
        verbose_name="op", orderable=False)

    class Meta:
        model = Exams
        fields = ['pk', 'exam_details', "url1"]


class ExamGradeTable(tables.Table):
    url1 = tables.TemplateColumn(
        '<a class="url_info" href="javascript:void(0)" onclick="change_score('"'{{record.pk}}'"')">change score</a>',
        verbose_name='op', orderable=False)
    class Meta:
        model = Exam_grades
        fields = ['student.name', 'grades', "url1"]


class CapTeamTable(tables.Table):
    url1 = tables.TemplateColumn(
        '<a class="url_info" href="javascript:void(0)" onclick="show_members('"'{{record.pk}}'"')">members</a>',
        verbose_name='op', orderable=False)
    url2 = tables.TemplateColumn(
        '<a class="url_info" href="javascript:void(0)" onclick="change_score('"'{{record.pk}}'"')">change score</a>',
        verbose_name='op', orderable=False)

    class Meta:
        model = Capstone_Team
        fields = ['id', "url1", 'url2']


class FinalScoreTable(tables.Table):
    class Meta:
        model = FinalScore
        fields = ['student', "grade"]
