# coding:utf-8
import os
import shlex

import lorun

import logging

from judge import config
from judge.protect import low_level


def judge_one(solution_id,
              problem_id,
              data_num,
              time_limit,
              mem_limit,
              language):
    low_level()
    input_path = os.path.join(
        config.data_dir, str(problem_id), 'data%s.in' % data_num)
    try:
        input_data = open(input_path, 'r')
    except:
        return False

    output_path = os.path.join(config.work_dir, str(solution_id), 'out%s.txt' % data_num)
    temp_out_data = open(output_path, 'w')

    if language == 'java':
        cmd = 'java -cp %s Main' % (os.path.join(config.work_dir,
                         str(solution_id)))
        main_exe = shlex.split(cmd)

    elif language == 'python2':
        cmd = 'python2 %s' % (
            os.path.join(config.work_dir,
                         str(solution_id),
                         'main.pyc'))
        main_exe = shlex.split(cmd)

    elif language == 'python3':
        cmd = 'python3 %s' % (
            os.path.join(config.work_dir,
                         str(solution_id),
                         '__pycache__/main.cpython-33.pyc'))
        main_exe = shlex.split(cmd)

    else:
        main_exe = [os.path.join(config.work_dir, str(solution_id), 'main'), ]

    runfig = {
        'args':main_exe,
        'fd_in' : input_data.fileno(),
        'fd_out' : temp_out_data.fileno(),
        'timelimit':time_limit,
        'memorylimit':mem_limit,
    }

    low_level()
    rst = lorun.run(runfig)
    input_data.close()
    temp_out_data.close()
    logging.debug(rst)
    return rst
