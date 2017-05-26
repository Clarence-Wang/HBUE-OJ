# coding:utf-8
import codecs
import os
import subprocess

import config
from judge.data_deal import update_compile_info
from judge.protect import low_level, dblock


def compile_code(solution_id, language):
    low_level()
    language = language
    dir_work = os.path.join(config.work_dir, str(solution_id))

    # 编译参数
    build_cmd = {
        "gcc":
            "gcc main.c -o main -Wall -lm -O2 -std=c99 --static -DONLINE_JUDGE",
        "g++": "g++ main.cpp -O2 -Wall -lm --static -DONLINE_JUDGE -o main",
        "java": "javac Main.java",
        "ruby": "reek main.rb",
        "perl": "perl -c main.pl",
        "pascal": 'fpc main.pas -O2 -Co -Ct -Ci',
        "go": '/opt/golang/bin/go build -ldflags "-s -w"  main.go',
        "lua": 'luac -o main main.lua',
        "python2": 'python2 -m py_compile main.py',
        "python3": 'python3 -m py_compile main.py',
        "haskell": "ghc -o main main.hs",
    }

    # 如果选择语言不存在
    if language not in build_cmd.keys():
        return False
    p = subprocess.Popen(
        build_cmd[language],
        shell=True,
        cwd=dir_work,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate()   # 获取编译错误信息
    err_text_path = os.path.join(config.work_dir, str(solution_id), 'error.txt')

    # codecs模块帮我们在读文件时自动转换编码，直接读出unicode
    f = codecs.open(err_text_path, 'w')
    f.write(err)
    f.write(out)
    f.close()
    # 成功
    if p.returncode == 0:
        return True

    # 数据库加锁问题，未解决
    dblock.acquire()
    update_compile_info(solution_id, 7)  # 编译失败,更新题目的编译错误信息
    dblock.release()
    return False
