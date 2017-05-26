# coding:utf-8
import logging

from judge.data_deal import update_user_ac, update_problem_ac
from judge.judge_one import judge_one
from judge.judge_result import judge_result
from judge.protect import low_level


def judge(solution_id, problem_id, data_count, time_limit, mem_limit, program_info, result_code, language):
    low_level()
    max_mem = 0
    max_time = 0
    if language in ['java', 'python2', 'python3']:
        time_limit = time_limit * 10
        mem_limit = mem_limit * 10
        print range(data_count)
    for i in range(data_count):
        ret = judge_one(solution_id, problem_id, i + 1, time_limit + 10, mem_limit, language)
        if ret == False:
            continue
        if ret['result'] == 5:
            program_info['result'] = result_code["Runtime Error"]
            return program_info
        if ret['result'] == 2 :
            program_info['result'] = result_code["Time Limit Exceeded"]
            program_info['take_time'] = time_limit + 10
            return program_info
        if ret['result'] == 3:
            program_info['result'] = result_code["Memory Limit Exceeded"]
            program_info['take_memory'] = mem_limit
            return program_info

        if max_time < ret['timeused']:
            max_time = ret['timeused']
        if max_mem < ret['memoryused']:
            max_mem = ret['memoryused']

        result = judge_result(problem_id, solution_id, i + 1)
        if result == False:
            continue
        if result == "Wrong Answer" or result == "Output limit":
            program_info['result'] = result_code[result]
            break
        elif result == "Presentation Error":
            program_info[result] = result_code[result]
        # 终于是走到这一步了
        elif result == "Accepted":
            if program_info['result'] != "Presentation Error":
                program_info['result'] = result_code[result]
                # 在这里修改用户ac和题目ac

        else:
            logging.error("judge did not get result")
    program_info['take_time'] = max_time
    program_info['take_memory'] = max_mem
    return program_info