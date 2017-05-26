# coding:utf-8
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from app_user.config import student_class_list
from forms import LoginForm, RegisterForm, ChangePasswordForm
from models import UserProfile


# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    errors = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            # print username, password
            if login_validate(request, username, password):
                return HttpResponseRedirect('/problem/1')
            else:
                errors.append('Please input the correct password')
    else:
        form = LoginForm()
    return render(request, 'login_form.html', {'errors': errors, 'form': form})


def login_validate(request, username, password):
    rtvalue = False
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return True
    return rtvalue


def register(request):
    errors = []
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            email = data['email']
            password = data['password']
            password2 = data['password2']
            real_name = data['real_name']
            student_id = data['student_id']
            # 我也不知道为什么class取不到，只能通过post取得
            student_class = request.POST["student_class"]
            if student_class not in student_class_list:
                errors.append('您所在的班级没有注册权限')

            if not User.objects.all().filter(username=username):
                if form.pwd_validate(password, password2):

                    user = User()
                    user.username = username
                    user.set_password(password)
                    user.email = email
                    user.save()

                    # 用户扩展信息 profile
                    profile = UserProfile()
                    profile.user_id = user.id
                    profile.real_name = real_name
                    profile.student_id = student_id
                    profile.student_class = student_class
                    profile.save()

                    login_validate(request, username, password)
                    return HttpResponseRedirect('/problem/1')
                else:
                    errors.append('Please input the same password')
            else:
                errors.append('The username has existed,please change your username')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form,
                                             'errors': errors,})


def logout(request):
    auth.logout(request)
    return render(request, 'logout.html')


def changePassword(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    
    if request.method == 'GET':
        return render(request, 'user_homePage.html')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = request.user.username
            old_password = data['old_password']
            new_password = data['new_password']
            confirm_password = data['confirm_password']

            # 判断用户名密码是否匹配
            user = authenticate(username=username, password=old_password)
            if user is not None:
                # 已经匹配
                # 判断两次输入的密码是否相同
                if form.pwd_validate(new_password, confirm_password):
                    # 如果用户名、原密码匹配则更新密码
                    user.set_password(new_password)
                    user.save()
                    info = 'Yes'
                    return render(request, 'changepwd_result.html', {'info': info})
                else:
                    info = '两次输入密码不相同'
            else:
                info = '用户名密码不匹配'
        else:
            form = ChangePasswordForm()
            info = u'请输入完整信息'
    return render(request, "changepwd_result.html", {'info': info, 'form': form})
