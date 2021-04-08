import pandas as pd
import numpy as np
import re


def seperate(line):
    l = []
    s = ""
    hasQuotation = False
    commas = 1
    i = 0
    while i < len(line):

        if line[i] == "," and hasQuotation == False:
            l.append(s)
            s = ""
            commas += 1
        else:
            if line[i] == '"':
                hasQuotation = not hasQuotation
            elif line[i] == "\\":
                s = "".join([s, line[i : i + 2]])
                i += 1
            else:
                s = "".join([s, line[i]])
        i += 1
    if len(s) != 0:
        l.append(s)
    while len(l) < commas:
        l.append("")
    return l


# 按类存放在
def extract(file_name):
    file = open("static/data/" + file_name, "rt", encoding="utf-8")

    lines = file.readlines()

    # string 里可能会有comma啊啊啊....
    # 得自己手动分离数据
    line = seperate(lines[0].rstrip())
    num_of_features = len(line)
    datas = [[] for i in range(num_of_features)]

    for line in lines:
        temp_data = seperate(line.rstrip())

        for i in range(num_of_features):
            try:
                name = temp_data[i]
            except:
                print(num_of_features, temp_data)
            try:
                datas[i].append(
                    name[1 : len(name) - 1]
                    if name.startswith('"') and name.endswith('"')
                    else name
                )
            except:
                print("Wrong data!")
    return datas