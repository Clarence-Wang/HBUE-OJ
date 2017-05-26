# coding:utf-8
import time

from judge.data_deal import update_solution_status, clean_work_dir
from judge.db import run_sql
from judge.get_code import get_code
from judge.protect import q, dblock


def put_task_into_queue():
    while True:
        q.join()
        sql = "SELECT id, problem_id_id, user_id_id, language " \
              "FROM app_problem_submit " \
              "WHERE status = 0"
        data = run_sql(sql)
        time.sleep(0.2)
        for i in data:
            solution_id, problem_id, user_id, language = i
            dblock.acquire()
            ret = get_code(solution_id, language)
            dblock.release()
            if ret == False:
                time.sleep(0.5)
                dblock.acquire()
                ret = get_code(solution_id, language)
                dblock.release()
            if ret == False:
                dblock.acquire()
                update_solution_status(solution_id=solution_id, result=11)
                dblock.release()
                clean_work_dir(solution_id)
                continue
            task = {
                "solution_id":solution_id,
                "problem_id":problem_id,
                "user_id":user_id,
                'language':language,
            }
            q.put(task)
            dblock.acquire()
            update_solution_status(solution_id, 0)
            dblock.release()
        time.sleep(0.5)