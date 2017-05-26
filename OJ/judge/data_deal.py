# coding:utf-8
import logging
import os
import shutil

from judge import config
from judge.db import run_sql


def clean_work_dir(solution_id):
    dir_name = os.path.join(config.work_dir, str(solution_id))
    shutil.rmtree(dir_name)


def update_solution_status(solution_id, result):
    if result == 0:
        update_status_sql = "UPDATE app_problem_submit " \
                            "SET status = 1 " \
                            "WHERE id = %s and status = 0" % solution_id

    else:
        update_status_sql = "UPDATE app_problem_submit " \
                            "SET status = 1 , result = %s " \
                            "WHERE id = %s and status = 0" % (result, solution_id)
    run_sql(update_status_sql)


def get_data_count(problem_id):
    """获得测试数据的个数信息"""
    full_path = os.path.join(config.data_dir, str(problem_id))
    try:
        files = os.listdir(full_path)
    except OSError as e:
        logging.error(e)
        return 0
    count = 0
    for item in files:
        if item.endswith(".in") and item.startswith("data"):
            count += 1
    return count


def update_result(result):
    update_result_sql = "UPDATE app_problem_submit " \
                        "SET result = %s , take_time = %s, take_memory = %s " \
                        "WHERE id = %s" % (
                            result['result'], result['take_time'], result['take_memory'], result['solution_id'])
    run_sql(update_result_sql)


def update_compile_info(solution_id, result):
    update_compile_sql = "UPDATE app_problem_submit " \
                         "SET result = %s , take_time = 0, take_memory = 0 " \
                         "WHERE id = %s" % (result, solution_id)
    run_sql(update_compile_sql)


def update_user_ac(user_id):
    update_user_sql = "UPDATE app_user_userprofile " \
                      "SET ac_times = ac_times + 1 " \
                      "WHERE user_id = %s" % user_id
    run_sql(update_user_sql)


def update_problem_ac(problem_id):
    update_problem_sql = "UPDATE app_problem_problem " \
                         "SET accept_times = accept_times + 1 " \
                         "WHERE id = %s" % problem_id
    run_sql(update_problem_sql)

def get_problem_limit(problem_id):
    get_sql = "SELECT time_limit, memory_limit " \
              "FROM app_problem_problem " \
              "WHERE id = %s" % problem_id
    data = run_sql(get_sql)
    return data[0]
