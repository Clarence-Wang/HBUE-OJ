# coding=utf-8

# 题目编号 解决编号 使用语言 测试数据  当前用户ID
import logging

from judge.check_danger_code import check_danger_code
from judge.compile import compile_code
from judge.data_deal import get_problem_limit
from judge.judge_main import judge
from judge.protect import low_level, dblock


def run(problem_id, solution_id, language, data_count, user_id):
    low_level()
    dblock.acquire()
    time_limit, mem_limit = get_problem_limit(problem_id)
    dblock.release()

    program_info = {
        "solution_id": solution_id,
        "problem_id": problem_id,
        "take_time": 0,
        "take_memory": 0,
        "user_id": user_id,
        "result": 0,
    }

    result_code = {
        "Waiting": 0,
        "Accepted": 1,
        "Time Limit Exceeded": 2,
        "Memory Limit Exceeded": 3,
        "Wrong Answer": 4,
        "Runtime Error": 5,
        "Output limit": 6,
        "Compile Error": 7,
        "Presentation Error": 8,
        "System Error": 11,
        "Judging": 12,
    }

    # if check_danger_code(solution_id, language):
    #     program_info['result'] = result_code["Runtime Error"]
    #     return program_info

    # 编译
    compile_result = compile_code(solution_id, language)
    if compile_result is False:
        program_info['result'] = result_code["Compile Error"]
        return program_info

    if data_count == 0:  # 没有测试数据
        program_info['result'] = result_code["System Error"]
        return program_info

    result = judge(
        solution_id,
        problem_id,
        data_count,
        time_limit,
        mem_limit,
        program_info,
        result_code,
        language)
    logging.debug(result)
    return result