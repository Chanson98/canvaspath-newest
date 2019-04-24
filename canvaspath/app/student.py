from django.shortcuts import render,redirect
import json
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from .models import *
from django.core.paginator import PageNotAnInteger
from .tables import StudentCourseTable, MyCourseTable
import xlrd
import re
import hashlib
from django_tables2 import SingleTableView
from django.views.generic import CreateView, UpdateView, DeleteView
from . import global_variable


def change_info(request):
    c = {}
    c['title'] = 'Student'
    student = Student.objects.get(email=global_variable.global_user)
    c['username'] = student.email

    if request.method == "POST":
        street = request.POST.get("street", "")
        phone = request.POST.get("phone", "")
        if street:
            student.street = street
        if phone:
            student.phone = phone
        student.save()
        return HttpResponse(json.dumps('success'))

    c.update(csrf(request))
    return render(request, 'app/student_change_info.html', c)


def student_courses(request):
    c = {}
    c['title'] = 'Student'
    course_name = request.GET.get('course_name', "")
    courses = Course.objects.all()
    c['course_name'] = course_name
    if course_name:
        courses = courses.filter(course_name__contains=course_name)
    # sort
    sort = request.GET.get("sort", "")
    if sort:
        try:
            courses = courses.order_by(sort)
            c["sort"] = sort
        except Exception as e:
            pass
    if courses:
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
        table = StudentCourseTable(courses)
        table.paginate(page=page, per_page=10)
        c['course_table'] = table
    except Exception as e:
        pass


    c.update(csrf(request))
    return render(request, 'app/student_choose_course.html', c)


def choose_course(request, id):
    print(global_variable.global_user)
    student = Student.objects.get(email=global_variable.global_user)
    if id:
        success = False
        sections = Sections.objects.filter(course_id=id)
        for section in sections:
            if Enrolls.objects.filter(section=section, student=student).exists():
                return HttpResponse('you have already chose this course')
            enroll = Enrolls.objects.filter(section=section)
            if len(enroll) >= section.limit:
                pass
            else:
                new_enroll = Enrolls(section=section, student=student)
                new_enroll.save()
                success = True
                break
        if success is False:
            return HttpResponse('There is no remaining amount for this course')
        else:
            return HttpResponse('success')
    return HttpResponse('failed')


def my_courses(request):
    c = {}
    c['title'] = 'Student'
    student = Student.objects.get(email=global_variable.global_user)
    enroll = Enrolls.objects.filter(student=student)
    sections = []
    for e1 in enroll:
        sections.append(e1.section)

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
        table = MyCourseTable(sections)
        table.paginate(page=page, per_page=10)
        c['section_table'] = table
    except Exception as e:
        pass

    c.update(csrf(request))
    return render(request, 'app/student_my_courses.html', c)


def reg_detail(request, id):
    c = {}
    c['title'] = 'Student'
    section = Sections.objects.get(pk=id)
    student = Student.objects.get(email=global_variable.global_user)
    final_score = FinalScore.objects.filter(section=section, student=student)
    if final_score:
        final_score = final_score.first()
        c['final_score'] = final_score.grade
    course = section.course_id
    c['description'] = course.course_description
    c['course_name'] = course.course_name
    professors = Prof_team_members.objects.filter(teaching_team_id=section.teaching_team_id)
    c['professors'] = professors
    # homeworks
    homeworks = Homework.objects.filter(section=section)
    c['homeworks'] = homeworks
    homework_dict = []
    for h in homeworks:
        tmp = {}
        grade = Homework_grades.objects.get(homework=h, student=student).grades
        tmp['grade'] = grade
        tmp['no'] = h.pk
        tmp['detail'] = h.hw_details
        homework_dict.append(tmp)
    c['homeworks'] = homework_dict
    # exams
    exams = Exams.objects.filter(section=section)
    c['exams'] = exams
    exam_dict = []
    for e in exams:
        tmp = {}
        grade = Exam_grades.objects.get(exam=e, student=student).grades
        tmp['no'] = e.pk
        tmp['grade'] = grade
        tmp['detail'] = e.exam_details
        exam_dict.append(tmp)
    c['exams'] = exam_dict
    c.update(csrf(request))
    return render(request, 'app/student_reg_detail.html', c)


def cap_detail(request, id):
    c = {}
    c['title'] = 'Student'
    student = Student.objects.get(email=global_variable.global_user)
    section = Sections.objects.get(pk=id)
    final_score = FinalScore.objects.filter(section=section, student=student)
    if final_score:
        final_score = final_score.first()
        c['final_score'] = final_score.grade
    course = section.course_id
    c['description'] = course.course_description
    c['course_name'] = course.course_name
    # cap_group
    cap_team = Capstone_Team_Members.objects.filter(student=student)
    if cap_team:
        cap_team = cap_team.first()
        project = cap_team.team.project_no
        c['professor'] = project.sponsor_id.email
        members = []
        mems = Capstone_Team_Members.objects.filter(team=cap_team.team)
        c['members'] = members
        for m in mems:
            members.append(m.student.name)
        score = Capstone_grades.objects.get(team=cap_team.team).grade
        c['c_grade'] = score
        # exams
        exams = Exams.objects.filter(section=section)
        c['exams'] = exams
        exam_dict = []
        for e in exams:
            tmp = {}
            grade = Exam_grades.objects.get(exam=e, student=student).grades
            tmp['no'] = e.pk
            tmp['grade'] = grade
            tmp['detail'] = e.exam_details
            exam_dict.append(tmp)
        c['exams'] = exam_dict
    c.update(csrf(request))
    return render(request, 'app/student_cap_detail.html', c)


