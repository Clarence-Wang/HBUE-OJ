# coding:utf-8
import codecs
import os

from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render

from app_problem.models import Problem
from app_problem.models import Submit
from app_user.models import UserProfile

from judge import config
from judge.config import result_code

# Create your views here.

# 获取所有题目显示在前台界面
def problem(request):
    if request.method == 'GET':
        # 如果在题目界面搜索各种信息，返回的界面如下
        if request.GET.has_key('search_problem'):
            search_problem = request.GET['search_problem']
            problem_list = Problem.objects.filter(Q(title__contains=search_problem) |
                                                  Q(id__contains=search_problem) |
                                                  Q(source__contains=search_problem) |
                                                  Q(level__contains=search_problem))

        if request.GET.has_key('classify'):
            problem_classify = request.GET['classify']
            problem_list = Problem.objects.filter(classify=problem_classify)

        else :
            problem_list = Problem.objects.all()

        classify_list = Problem.objects.values("classify").annotate(number=Count("classify"))

        paginator = Paginator(problem_list, 10)
        page = paginator.num_pages
        cur_page = request.path.split('/')[2]
        try:
            cur_page_problem = paginator.page(cur_page)
        except:
            cur_page_problem = paginator.page(1)

        return render(request, 'problem.html', {'cur_page_problem':cur_page_problem,
                                                'page':range(1, page+1),
                                                'classify_list':classify_list
                                                }
                      )




def ranking(request):
    return render(request, 'ranking.html')


def submit(request):
    # 由界面获取当前题目ID
    cur_pro_id = request.path.split('/')[-2]
    cur_pro_id = int(cur_pro_id)
    if request.method == 'GET':
        # 由当前题目ID获取当前题目
        cur_pro = Problem.objects.get(id=cur_pro_id)
        # 由当前题目ID 和 当前用户 取得当前用户在改题目下的提交，并且由提交顺序排反序
        cur_pro_submit = Submit.objects.filter(problem_id=cur_pro_id, user_id=request.user.id).order_by("-id")
        for i in cur_pro_submit:
            i.result = result_code[i.result]
        return render(request, 'submit_code.html', {'cur_pro': cur_pro, 'cur_pro_submit': cur_pro_submit})

    if request.method == 'POST':
        # 取得用户提交的代码
        user = request.user
        code = request.POST['code']
        language = request.POST['language']
        code_length = len(code)

        user_profile = UserProfile.objects.get(user_id=user.id)
        user_profile.submit_times = user_profile.submit_times + 1
        user_profile.save()

        cur_pro = Problem.objects.get(id=cur_pro_id)
        cur_pro.submit_times = cur_pro.submit_times + 1
        cur_pro.save()

        cur_submit = Submit()
        cur_submit.language = language
        cur_submit.codeLength = code_length
        cur_submit.code = code
        cur_submit.user_id_id = user.id
        cur_submit.problem_id_id = cur_pro_id
        cur_submit.save()
        return HttpResponseRedirect('/submit/1')


def submit_home_page(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')

    errors = {}
    user_submit_list = Submit.objects.filter(user_id=request.user.id).order_by("-id")

    for i in user_submit_list:
        i.result = result_code[i.result]
        errors[i.id] = get_error(i.id)

    paginator = Paginator(user_submit_list, 10)
    page = paginator.num_pages
    cur_page = request.path.split('/')[2]
    try:
        cur_page_submit = paginator.page(cur_page)
    except:
        cur_page_submit = paginator.page(1)
    return render(request, 'submit.html', {"cur_page_submit": cur_page_submit,
                                           "page": range(1, page+1),
                                           "errors": errors
                                           })


def view_submit_code(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    cur_submit_id = request.path.split('/')[3]
    cur_submit = Submit.objects.get(id=cur_submit_id)
    code = get_code(cur_submit.id, cur_submit.language)
    error = get_error(cur_submit.id)
    return render(request, 'view_submit_code.html', {'cur_submit': cur_submit, 'code': code, 'error':error})


def get_error(solution_id):
    try:
        err_text_path = os.path.join('work_dir/', str(solution_id), 'error.txt')
        f = codecs.open(err_text_path, 'r')
        error = f.read()
        f.close()
        return error
    except:
        pass


def get_code(solution_id, language):
    code_text_path = os.path.join('work_dir/', str(solution_id), config.file_name[language])
    f = codecs.open(code_text_path, 'r')
    code = f.read()
    f.close()
    return code
