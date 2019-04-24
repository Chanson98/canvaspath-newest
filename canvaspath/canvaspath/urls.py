"""canvaspath URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from app.views import *
from app.administrator import *
from app.student import *
from app.professor import *

urlpatterns = [
    url('^$', login),
    url(r'^change_pw/$', change_pw),
    url(r'^admin/', admin.site.urls),
    url(r'^administrator/show_students/$', show_students),
    url(r'^administrator/import_students/$', import_students),
    url(r'^administrator/show_professors/$', show_professors),
    url(r'^administrator/import_professors/$', import_professors),
    url(r'^administrator/course_management/$', CourseList.as_view()),
    url(r'^administrator/course_management/new/$', CourseCreate.as_view()),
    url(r'^administrator/course_management/update/(?P<id>.+)/$', CourseUpdate.as_view()),
    url(r'^administrator/course_management/delete/(?P<id>.+)/$', CourseDelete.as_view()),
    url(r'^administrator/section_management/(?P<id>.+)/$', SectionList.as_view()),
    url(r'^administrator/new_section/(?P<id>.+)/$', SectionCreate.as_view()),
    url(r'^administrator/section_prof_team/(?P<id>.+)/$', section_prof_team),
]

urlpatterns += [
    url(r'^student/change_info/$', change_info),
    url(r'^student/show_courses/$', student_courses),
    url(r'^student/choose_course/(?P<id>.+)/$', choose_course),
    url(r'^student/my_courses/$', my_courses),
    url(r'^student/reg_detail/(?P<id>.+)/$', reg_detail),
    url(r'^student/cap_detail/(?P<id>.+)/$', cap_detail),
]

urlpatterns += [
    url(r'^professor/courses/$', professor_courses),
    url(r'^professor/homeworks/(?P<id>.+)/$', homework_list),
    url(r'^professor/homework/new/(?P<id>.+)/$', HomeworkCreate.as_view()),
    url(r'^professor/homework/score/(?P<id>.+)/$', change_homework_score),
    url(r'^professor/exams/(?P<id>.+)/$', exam_list),
    url(r'^professor/exam/new/(?P<id>.+)/$', ExamCreate.as_view()),
    url(r'^professor/exam/score/(?P<id>.+)/$', change_exam_score),
    url(r'^professor/cap/(?P<id>.+)/$', cap_list),
    url(r'^professor/score_sheet/(?P<id>.+)/$', score_sheet),
]
