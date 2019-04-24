from django.shortcuts import render,redirect
import json
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from .models import *
from django.core.paginator import PageNotAnInteger
from .tables import ProfessorCourseTable, HomeworkTable, HomeworkGradeTable, ExamTable, ExamGradeTable, CapTeamTable, FinalScoreTable
import xlrd
import re
import hashlib
from django_tables2 import SingleTableView
from django.views.generic import CreateView, UpdateView, DeleteView
from . import global_variable



def professor_courses(request):
    c = {}
    c['title'] = 'Professor'
    professor = Professor.objects.get(email=global_variable.global_user)
    prof_team = Prof_team_members.objects.filter(professor=professor)
    sections = []
    for p in prof_team:
        section = Sections.objects.get(teaching_team_id=p.teaching_team_id)
        sections.append(section)
    if sections:
        pass
    else:
        c['is_data'] = "false"
    # page turning
    try:
        page = request.GET.get("page", 1)
    except PageNotAnInteger:
        page = 1
    c["page"] = page
    try:
        table = ProfessorCourseTable(sections)
        table.paginate(page=page, per_page=10)
        c['section_table'] = table
    except Exception as e:
        pass

    c.update(csrf(request))
    return render(request, 'app/professor_courses.html', c)


def homework_list(request, id):
    c = {}
    c['title'] = 'Professor'
    section = Sections.objects.get(pk=id)
    c['id'] = id
    c['course_name'] = section.course_id.course_name
    homeworks = Homework.objects.filter(section=section)
    c['homeworks'] = homeworks
    if homeworks:
        pass
    else:
        c['is_data'] = "false"
    # page turning
    try:
        page = request.GET.get("page", 1)
    except PageNotAnInteger:
        page = 1
    c["page"] = page
    try:
        table = HomeworkTable(homeworks)
        table.paginate(page=page, per_page=10)
        c['homework_table'] = table
    except Exception as e:
        pass
    c.update(csrf(request))
    return render(request, 'app/professor_homework_list.html', c)


class HomeworkCreate(CreateView):
    model = Homework
    template_name = "app/professor_new_homework.html"
    fields = ['section', 'hw_details']

    def get_success_url(self):
        id = self.kwargs.get("id")
        return '/professor/homeworks/' + str(id) + '/'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        context['id'] = id
        context['title'] = 'Homework Manage'
        return context


def change_homework_score(request, id):
    c = {}
    c['title'] = 'Professor'
    c['id'] = id
    homework = Homework.objects.get(pk=id)
    grades = Homework_grades.objects.filter(homework=homework)
    if not grades:
        section = homework.section
        students = Enrolls.objects.filter(section=section)
        for s in students:
            student = s.student
            new_grade = Homework_grades(homework=homework, student=student, grades=0)
            new_grade.save()
        grades = Homework_grades.objects.filter(homework=homework)

    if request.method == "POST":
        # print('post')
        score = request.POST.get("score", -1)
        current_id = request.POST.get("current_id", None)
        # print(score, current_id)
        if score == -1:
            pass
        else:
            score = float(score)
            grade = Homework_grades.objects.get(pk=current_id)
            grade.grades = score
            grade.save()
        return HttpResponse(json.dumps('success'))

    # sort
    sort = request.GET.get("sort", "")
    if sort:
        try:
            grades = grades.order_by(sort)
            c["sort"] = sort
        except Exception as e:
            pass
    if grades:
        pass
    else:
        c['is_data'] = "false"
    # page turning
    try:
        page = request.GET.get("page", 1)
    except PageNotAnInteger:
        page = 1
    c["page"] = page
    try:
        table = HomeworkGradeTable(grades)
        table.paginate(page=page, per_page=10)
        c['grade_table'] = table
    except Exception as e:
        pass

    c.update(csrf(request))
    return render(request, 'app/professor_homework_score.html', c)


def exam_list(request, id):
    c = {}
    c['title'] = 'Professor'
    section = Sections.objects.get(pk=id)
    c['id'] = id
    c['course_name'] = section.course_id.course_name
    exams = Exams.objects.filter(section=section)
    c['exams'] = exams
    if exams:
        pass
    else:
        c['is_data'] = "false"
    # page turning
    try:
        page = request.GET.get("page", 1)
    except PageNotAnInteger:
        page = 1
    c["page"] = page
    try:
        table = ExamTable(exams)
        table.paginate(page=page, per_page=10)
        c['exam_table'] = table
    except Exception as e:
        pass
    c.update(csrf(request))
    return render(request, 'app/professor_exam_list.html', c)


class ExamCreate(CreateView):
    model = Exams
    template_name = "app/professor_new_exam.html"
    fields = ['section', 'exam_details']

    def get_success_url(self):
        id = self.kwargs.get("id")
        return '/professor/exams/' + str(id) + '/'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        context['id'] = id
        context['title'] = 'Exam Manage'
        return context
    

def change_exam_score(request, id):
    c = {}
    c['title'] = 'Professor'
    c['id'] = id
    exam = Exams.objects.get(pk=id)
    grades = Exam_grades.objects.filter(exam=exam)
    if not grades:
        section = exam.section
        students = Enrolls.objects.filter(section=section)
        for s in students:
            student = s.student
            new_grade = Exam_grades(exam=exam, student=student, grades=0)
            new_grade.save()
        grades = Exam_grades.objects.filter(exam=exam)

    if request.method == "POST":
        # print('post')
        score = request.POST.get("score", -1)
        current_id = request.POST.get("current_id", None)
        # print(score, current_id)
        if score == -1:
            pass
        else:
            score = float(score)
            grade = Exam_grades.objects.get(pk=current_id)
            grade.grades = score
            grade.save()
        return HttpResponse(json.dumps('success'))

    # sort
    sort = request.GET.get("sort", "")
    if sort:
        try:
            grades = grades.order_by(sort)
            c["sort"] = sort
        except Exception as e:
            pass
    if grades:
        pass
    else:
        c['is_data'] = "false"
    # page turning
    try:
        page = request.GET.get("page", 1)
    except PageNotAnInteger:
        page = 1
    c["page"] = page
    try:
        table = ExamGradeTable(grades)
        table.paginate(page=page, per_page=10)
        c['grade_table'] = table
    except Exception as e:
        pass

    c.update(csrf(request))
    return render(request, 'app/professor_exam_score.html', c)


def cap_list(request, id):
    c = {}
    c['title'] = 'Cap Group'
    c['id'] = id
    c['members'] = []
    professor = Professor.objects.get(email=global_variable.global_user)
    section = Sections.objects.get(pk=id)
    cap_sections = Capstone_section.objects.filter(section=section, sponsor_id=professor)
    all_team = []
    for project in cap_sections:
        teams = Capstone_Team.objects.filter(project_no=project)
        all_team.append(teams)
    team = None
    if all_team:
        team = all_team[0]
        for i in range(1, len(all_team)):
            team = team | all_team[1]
    if team:
        pass
    else:
        c['is_data'] = "false"
    # page turning
    try:
        page = request.GET.get("page", 1)
    except PageNotAnInteger:
        page = 1
    c["page"] = page
    try:
        table = CapTeamTable(team)
        table.paginate(page=page, per_page=10)
        c['team_table'] = table
    except Exception as e:
        pass

    if request.method == "POST":
        flag = request.POST.get("flag", "")
        if flag == "new":
            upload_file = request.FILES.get("myfile", None)
            if not upload_file:
                return HttpResponse("no files for upload!")
            else:
                file = upload_file.read()
            result = ''
            try:
                workbook = xlrd.open_workbook(file_contents=file)
                count = 0
                for sheet in workbook.sheets():
                    nrows = sheet.nrows
                    print(nrows)
                    new_cap = Capstone_section(section=section, sponsor_id=professor)
                    new_cap.save()
                    new_team = Capstone_Team(project_no=new_cap)
                    new_team.save()
                    for row in range(1, nrows):
                        values = sheet.row_values(row)
                        student = Student.objects.filter(email=values[0])
                        if student:
                            count += 1
                            student = student.first()
                            new_member = Capstone_Team_Members(student=student, team=new_team)
                            new_member.save()
                            enroll = Enrolls.objects.filter(student=student, section=section)
                            if enroll:
                                pass
                            else:
                                new_enroll = Enrolls(student=student, section=section)
                                new_enroll.save()

                result += 'added ' + str(count) + ' members successfully!'
            except Exception as e:
                print(e)
            return HttpResponse(json.dumps(result))
        elif flag == 'members':
            current_id = request.POST.get("current_id", None)
            if current_id:
                t = Capstone_Team.objects.get(pk=current_id)
                members = Capstone_Team_Members.objects.filter(team=t)
                ms = []
                for m in members:
                    ms.append(m.student.name)
                print(ms)
                return HttpResponse(json.dumps(ms))
        elif flag == 'score':
            score = request.POST.get("score", -1)
            current_id = request.POST.get("current_id", None)
            # print(score, current_id)
            if score == -1:
                pass
            else:
                score = int(score)
                t = Capstone_Team.objects.get(pk=current_id)
                grade = Capstone_grades.objects.filter(team=t)
                if grade:
                    grade = grade.first()
                else:
                    grade = Capstone_grades(team=t)
                grade.grade = score
                grade.save()
                print(score, grade.grade)
            return HttpResponse(json.dumps('success'))
    c.update(csrf(request))
    return render(request, 'app/professor_cap_detail.html', c)


def score_sheet(request, id):
    c = {}
    c['title'] = 'Score Sheet'
    c['id'] = id
    section = Sections.objects.get(pk=id)
    c['section_name'] = section.section_name
    enrolls = Enrolls.objects.filter(section=section)
    students = []
    for e in enrolls:
        students.append(e.student)
    if section.section_type == 'Reg':
        homeworks = Homework.objects.filter(section=section)
        exams = Exams.objects.filter(section=section)
        for s in students:
            h_grades = []
            for h in homeworks:
                grade = Homework_grades.objects.get(student=s, homework=h).grades
                h_grades.append(grade)
            e_grades = []
            for e in exams:
                grade = Exam_grades.objects.get(student=s, exam=e).grades
                e_grades.append(grade)
            final = sum(h_grades) / len(h_grades) + sum(e_grades) / len(e_grades)
            final = int(final/2)
            # print(final)
            f_grade = FinalScore.objects.filter(section=section, student=s)
            if f_grade:
                f_grade = f_grade.first()
                f_grade.grade = final
            else:
                f_grade = FinalScore(section=section, student=s, grade=final)
            f_grade.save()
            # print('score', final)

    else:
        for s in students:
            print(s.name)
            teams = Capstone_Team_Members.objects.filter(student=s)

            c_grades = []
            for t in teams:
                grade = Capstone_grades.objects.get(team=t.team).grade
                c_grades.append(grade)
            print(c_grades)
            exams = Exams.objects.filter(section=section)
            e_grades = []
            for e in exams:
                grade = Exam_grades.objects.get(student=s, exam=e).grades
                e_grades.append(grade)
            final = sum(c_grades) / len(c_grades) + sum(e_grades) / len(e_grades)
            final = int(final / 2)
            print(final)
            f_grade = FinalScore.objects.filter(section=section, student=s)
            if f_grade:
                f_grade = f_grade.first()
                f_grade.grade = final
            else:
                f_grade = FinalScore(section=section, student=s, grade=final)
            f_grade.save()
    
    scores = FinalScore.objects.filter(section=section)
    total = []
    for sc in scores:
        total.append(sc.grade)
    avg = sum(total) / len(total)
    c['avg'] = avg
    # get max and min
    scores = scores.order_by('grade')
    c['lowest'] = scores.first().grade
    scores = scores.order_by('-grade')
    c['highest'] = scores.first().grade
    # sort
    sort = request.GET.get("sort", "")
    if sort:
        try:
            scores = scores.order_by(sort)
            c["sort"] = sort
        except Exception as e:
            pass
    if scores:
        pass
    else:
        c['is_data'] = "false"
    # page turning
    try:
        page = request.GET.get("page", 1)
    except PageNotAnInteger:
        page = 1
    c["page"] = page
    try:
        table = FinalScoreTable(scores)
        table.paginate(page=page, per_page=10)
        c['score_table'] = table
    except Exception as e:
        pass
    c.update(csrf(request))
    return render(request, 'app/professor_section_score.html', c)
            





