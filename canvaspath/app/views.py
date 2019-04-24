from django.shortcuts import render,redirect
import json
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from .models import *
from . import global_variable
import hashlib

# Create your views here.
def login(request):
    c = {}
    c['title'] = 'Login'
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        m2 = hashlib.md5()
        m2.update(password.encode('utf-8'))
        pw = m2.hexdigest()
        user_type = request.POST.get('user_type', 'Student')
        if user_type == 'Student':
            user = Student.objects.filter(email=email)
        elif user_type == 'Professor':
            user = Professor.objects.filter(email=email)
        else:
            user = Administrator.objects.filter(email=email)
        if user:
            user = user.first()
            u_pw = user.password
            if (password != u_pw) and (u_pw != pw):
                c['email'] = email
                c['password'] = ""
                c['password_error'] = "password error!"
                c['password'] = ""
                c['email_error'] = ""
            else:
                global_variable.global_user = email
                global_variable.user_type = user_type
                if user_type == 'Student':
                    return HttpResponseRedirect('/student/show_courses/')
                elif user_type == 'Professor':
                    return HttpResponseRedirect('/professor/courses/')
                else:
                    return HttpResponseRedirect('/administrator/show_students/')
        else:
            c['email'] = ""
            c['password'] = ""
            c['email_error'] = "this user does not exist!"
            c['password_error'] = ""
            c['email'] = ""
        c.update(csrf(request))
    return render(request, 'app/login.html', c)


def change_pw(request):
    c = {}
    c['title'] = 'change_pw'

    # 判断是否已登录
    try:
        if global_variable.user_type == 'Student':
            current_user = Student.objects.get(email=global_variable.global_user)
        elif global_variable.user_type == 'Professor':
            current_user = Professor.objects.get(email=global_variable.global_user)
        else:
            current_user = Administrator.objects.get(email=global_variable.global_user)
    except Exception as e:
        c['no_user'] = "no user"
        return redirect('/')

    c['username'] = current_user.email
    if request.method == 'POST':
        pre_password = request.POST.get('pre_password', None)
        new_password = request.POST.get('new_password', None)
        password_confirm = request.POST.get('password_confirm', None)
        result = ''
        m2 = hashlib.md5()
        m2.update(pre_password.encode('utf-8'))
        pre_pw = m2.hexdigest()

        m2 = hashlib.md5()
        m2.update(new_password.encode('utf-8'))
        pw = m2.hexdigest()
        if pre_password != current_user.password and pre_pw != current_user.password:
            result = 'pre_pwd_error'
        else:
            if new_password != password_confirm:
                result = 'pwd_confirm_error'
            else:
                current_user.password = pw
                current_user.save()
                result = 'success'
        print(result)
        return HttpResponse(json.dumps({'result': result}))
    return render(request, 'app/change_pw.html', c)


# def login(request):
#     template = loader.get_template('app/login.html')
#     context = {}
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         usertype = request.POST.get('type')
#         if email and password and usertype:
#             email = email.strip()
#             user = None
#             try:
#                 if usertype == "student":
#                     user = models.Students.objects.get(emailAddress=email)
#                 elif usertype == "professor":
#                     user = models.FacultyMembers.objects.get(emailAddress=email)
#                 elif usertype == "admin":
#                     user = models.Administrator.objects.get(emailAddress=email)
#                 else:
#                     return HttpResponse(template.render(context, request))
#                 m2 = hashlib.md5()
#                 m2.update(password.encode('utf-8'))
#                 password = m2.hexdigest()
#                 print(password)
#                 print(user.password)
#                 if user and user.password == password:
#                     request.session['user'] = email
#                     return redirect('./index')
#             except:
#                 context['error'] = 'wrong password!'
#                 return HttpResponse(template.render(context, request))
#     return HttpResponse(template.render(context, request))
#
# def index(request):
#     if not request.session.get("user",default=None):
#         return redirect('./login')
#     template = loader.get_template('app/index.html')
#     return HttpResponse(template.render({}, request))
#
#
# def logout(request):
#     if request.session.get("user",default=None):
#         del request.session["user"]
#     return redirect('./login')