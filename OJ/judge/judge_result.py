# coding:utf-8
import logging
import os

from judge import config
from judge.protect import low_level


def judge_result(program_id, solution_id, data_num):
    low_level()
    logging.debug("Judging result")
    correct_result = os.path.join(
        config.data_dir, str(program_id), 'data%s.out' % data_num
    )

    user_result = os.path.join(
        config.work_dir, str(solution_id), 'out%s.txt' % data_num
    )

    try:
        correct = file(correct_result).read().replace('\r', '').rstrip()
        user = file(user_result).read().replace('\r', '').rstrip()
    except:
        return False
    if correct == user:
        return "Accepted"
    if correct.split() == user.split():
        return "Presentation Error"
    if correct in user:
        return "Output limit"
    return "Wrong Answer"
