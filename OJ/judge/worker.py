# coding:utf-8
import threading

import logging

from judge import config
from judge.data_deal import get_data_count, clean_work_dir, update_result, update_user_ac, update_problem_ac
from judge.protect import q, dblock
from judge.run import run


def get_task_from_queue():
    while True:
        if q.empty() is True:
            logging.info("%s idle" % (threading.current_thread()))
        task = q.get()
        solution_id = task['solution_id']
        problem_id = task['problem_id']
        language = task['language']
        user_id = task['user_id']
        data_count = get_data_count(task['problem_id'])
        logging.info("judging %s " % solution_id)
        result = run(
            problem_id,
            solution_id,
            language,
            data_count,
            user_id,
        )

        logging.info(
            "%s result %s" % (result['solution_id'], result['result'])
        )

        dblock.acquire()
        update_result(result)
        if result['result'] == 1:
            update_user_ac(result["user_id"])
            update_problem_ac(result["problem_id"])
        dblock.release()
        if config.auto_clean:
            clean_work_dir(result['solution_id'])
        q.task_done()