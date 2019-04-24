from django.shortcuts import render,redirect
import json
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from .models import *
from django.core.paginator import PageNotAnInteger
from .tables import import_students_table,import_professors_table, CourseTable, SectionTable
import xlrd
import re
import hashlib
from django_tables2 import SingleTableView
from django.views.generic import CreateView, UpdateView, DeleteView
from . import global_variable


def show_students(request):
    c = {}
    c['title'] = 'Import Students'
    students = Student.objects.all()
    # sort
    sort = request.GET.get("sort", "")
    if sort:
        try:
            students = students.order_by(sort)
            c["sort"] = sort
        except Exception as e:
            pass
    if students:
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
        table = import_students_table(students)
        table.paginate(page=page, per_page=10)
        c['student_table'] = table
    except Exception as e:
        pass
    c.update(csrf(request))
    return render(request, 'app/admin_student_management.html', c)


def import_students(request):
    if request.method == "POST":
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
                for row in range(1, nrows):
                    values = sheet.row_values(row)
                    if Student.objects.filter(email=values[0]).exists():
                        # result += 'the email ' + values[0] + ' has been registered;'
                        pass
                    else:
                        count += 1
                        m2 = hashlib.md5()
                        m2.update(values[1].encode('utf-8'))
                        password = m2.hexdigest()
                        student = Student(email=values[0], password=password, name=values[2], age=int(values[3]), gender=values[4], major=values[5], street=values[6], phone=str(values[7]), zipcode=str(values[8]))
                        student.save()
            result += 'registered ' + str(count) + ' students successfully!'
        except Exception as e:
            print(e)
        return HttpResponse(json.dumps({'result': result}))


def show_professors(request):
    c = {}
    c['title'] = 'Import Professors'
    professors = Professor.objects.all()
    # sort
    sort = request.GET.get("sort", "")
    if sort:
        try:
            professors = professors.order_by(sort)
            c["sort"] = sort
        except Exception as e:
            pass
    if professors:
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
        table = import_professors_table(professors)
        table.paginate(page=page, per_page=10)
        c['professor_table'] = table
    except Exception as e:
        pass
    c.update(csrf(request))
    return render(request, 'app/administrator_professor_management.html', c)


def import_professors(request):
    if request.method == "POST":
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
                for row in range(1, nrows):
                    values = sheet.row_values(row)
                    if Professor.objects.filter(email=values[0]).exists():
                        # result += 'the email ' + values[0] + ' has been registered;'
                        pass
                    else:
                        count += 1
                        depts = Department.objects.filter(dept_head=values[7], dept_name=values[8])
                        if depts:
                            dept = depts.first()
                        else:
                            dept = Department(dept_head=values[7], dept_name=values[8])
                            dept.save()
                        m2 = hashlib.md5()
                        m2.update(values[1].encode('utf-8'))
                        password = m2.hexdigest()
                        professor = Professor(email=values[0], password=password, name=values[2], age=int(values[3]), gender=values[4], office_address=values[5], title=values[6], department=dept)
                        professor.save()
            result += 'registered ' + str(count) + ' professors successfully!'
        except Exception as e:
            print(e)
        return HttpResponse(result)


class CourseList(SingleTableView):

    model = Course
    table_class = CourseTable
    template_name = "app/admin_course_list.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['title'] = 'Course Manage'
        courses = Course.objects.all()
        if courses:
            pass
        else:
            context['is_data'] = "false"

        # 排序
        sort = self.request.GET.get("sort", "")
        if sort:
            courses = courses.order_by(sort)
            context["sort"] = sort
        # 翻页
        try:
            page = self.request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1
        context["page"] = page
        try:
            table = CourseTable(courses)
            table.paginate(page=page, per_page=10)
            context['course_table'] = table
        except Exception as e:
            pass
        return context


class CourseCreate(CreateView):
    success_url = '/administrator/course_management/'
    model = Course
    template_name = "app/admin_new_course.html"
    fields = ['course_id', 'course_name', 'course_description']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['title'] = 'Course Manage'
        return context


class CourseUpdate(UpdateView):
    success_url = '/administrator/course_management/'
    model = Course
    template_name = "app/admin_update_course.html"
    fields = ['course_id', 'course_name', 'course_description']

    def get_object(self, queryset=None):
        try:
            course_id = self.kwargs.get("id")
            return Course.objects.get(pk=course_id)
        except Exception as e:
            return None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['title'] = 'Course Manage'
        return context


class CourseDelete(DeleteView):
    success_url = '/administrator/course_management/'
    model = Course
    template_name = "app/admin_delete_course.html"

    def get_object(self, queryset=None):
        try:
            course_id = self.kwargs.get("id")
            return Course.objects.get(pk=course_id)
        except Exception as e:
            return None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['title'] = 'Course Manage'
        return context


class SectionList(SingleTableView):
    model = Course
    table_class = CourseTable
    template_name = "app/admin_section_list.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['title'] = 'Section Manage'
        course_id = self.kwargs.get("id")
        context['id'] = course_id
        course = Course.objects.get(pk=course_id)
        sections = Sections.objects.filter(course_id=course)
        if sections:
            pass
        else:
            context['is_data'] = "false"

        # 排序
        sort = self.request.GET.get("sort", "")
        if sort:
            sections = sections.order_by(sort)
            context["sort"] = sort
        # 翻页
        try:
            page = self.request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1
        context["page"] = page
        try:
            table = SectionTable(sections)
            table.paginate(page=page, per_page=10)
            context['section_table'] = table
        except Exception as e:
            pass
        return context


class SectionCreate(CreateView):

    model = Sections
    template_name = "app/admin_new_section.html"
    fields = ['course_id', 'section_name', 'section_type', 'limit']

    def get_success_url(self):
        id = self.kwargs.get("id")
        print(id)
        return '/administrator/section_management/' + str(id) + '/'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")
        context['title'] = 'Section Manage'
        context['id'] = id
        print(id)
        return context


def section_prof_team(request, id):
    c = {}
    c['title'] = 'Section Manage'
    c['id'] = id
    section = Sections.objects.get(pk=id)
    if section.teaching_team_id:
        team = section.teaching_team_id
        print(team)
    else:
        team = Prof_teams(team_name='new_section_team')
        team.save()
        section.teaching_team_id = team
        section.save()
        print('new_team')
    members = Prof_team_members.objects.filter(teaching_team_id=team)
    c['members'] = members

    if request.method == "POST":
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
                for row in range(1, nrows):
                    values = sheet.row_values(row)
                    professors = Professor.objects.filter(email=values[0])
                    if professors:
                        professor = professors.first()
                        if members.filter(professor=professor).exists():
                            pass
                        else:
                            count += 1
                            mem = Prof_team_members(teaching_team_id=team, professor=professor)
                            mem.save()
            result += 'added ' + str(count) + ' members successfully!'
        except Exception as e:
            print(e)
        return HttpResponse(result)
    c.update(csrf(request))
    return render(request, 'app/admin_section_team.html', c)
