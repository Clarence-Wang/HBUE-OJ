# coding:utf-8

# work评判目录
work_dir = "../work_dir"
# data测试数据目录
data_dir = "../data_dir"


# 数据库地址
db_host = "localhost"

db_user = "root"

db_password = "wcy0890"

db_name = "oj"

db_charset = "utf8"

queue_size = 4

auto_clean = False


count_thread = 1


file_name = {
        "gcc": "main.c",
        "g++": "main.cpp",
        "java": "Main.java",
        'ruby': "main.rb",
        "perl": "main.pl",
        "pascal": "main.pas",
        "go": "main.go",
        "lua": "main.lua",
        'python2': 'main.py',
        'python3': 'main.py',
        "haskell": "main.hs"
    }

result_code = {"": "Waiting",
               "0": "Waiting",
               "1": "Accepted",
               "2": "Time Limit Exceeded",
               "3": "Memory Limit Exceeded",
               "4": "Wrong Answer",
               "5": "Runtime Error",
               "6": "Output limit",
               "7": "Compile Error",
               "8": "Presentation Error",
               "11": "System Error",
               "12": "Judging",
               }
