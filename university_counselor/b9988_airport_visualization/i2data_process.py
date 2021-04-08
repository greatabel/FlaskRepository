import pandas as pd
import numpy as np
import re

from i2common import *




# generate CSV
def generate_CSV(data, key, file_name):
    dataframe = pd.DataFrame({key[i]: data[i] for i in range(len(key))})
    dataframe.to_csv("static/data/" + file_name + ".csv", index=False, sep=",")


# generate real JSON file
def generate_JSON(data, key, file_name):
    print(file_name)
    f = open("static/data/" + file_name + ".json", "w", encoding="utf-8")
    f.writelines("[\n")

    length = len(data[0])

    for ds in data:
        if ds[0].find(".") >= 0 and ds[0][0].isdigit():
            for i in range(length):
                ds[i] = np.float64(ds[i])
        elif ds[0].isdigit() or (ds[0].find("-") == 0 and ds[0][1:].isdigit()):
            con = False
            for i in range(length):
                if ds[i].find(".") >= 0:
                    con = True
                    break
            if con == True:
                for i in range(length):
                    if ds[i] == "\\N":
                        ds[i] = "null"
                    else:
                        ds[i] = np.float64(ds[i])
            else:
                for i in range(length):
                    if ds[i] == "\\N":
                        ds[i] = "null"
                    else:
                        ds[i] = int(ds[i])
        else:
            for i in range(length):
                if ds[i] == "\\N":
                    ds[i] = "null"
                else:
                    ds[i] = "".join(['"', ds[i], '"'])

    # print([data[i][0] for i in range(len(key))])
    for i in range(len(key)):
        key[i] = "".join(['"', key[i], '"'])
    data_len = len(data[0])
    for i in range(data_len):
        dic = "{"
        for j in range(len(key)):
            dic = " ".join([dic, "".join([key[j], ":", str(data[j][i]), ", "])])
        if dic[-2] == "," and dic[-1] == " ":
            dic = dic[: len(dic) - 2]
        dic = "".join([dic, "},\n" if i < data_len - 1 else "}\n"])
        f.writelines(dic)
    f.writelines("]")


# generate fake JSON-----a .js file
# 需要手动去除双斜杠 以及 将 '\"' 换成 '\''
def generate_fake_JSON(data, key, file_name):
    print(file_name)
    f = open("static/data/" + file_name + ".js", "w", encoding="utf-8")
    f.writelines(file_name + " = '[\\\n")

    length = len(data[0])

    for ds in data:
        if ds[0].find(".") >= 0 and ds[0][0].isdigit():
            for i in range(length):
                ds[i] = np.float64(ds[i])
        elif ds[0].isdigit() or (ds[0].find("-") == 0 and ds[0][1:].isdigit()):
            con = False
            for i in range(length):
                if ds[i].find(".") >= 0:
                    con = True
                    break
            if con == True:
                for i in range(length):
                    if ds[i] == "\\N":
                        ds[i] = "null"
                    else:
                        ds[i] = np.float64(ds[i])
            else:
                for i in range(length):
                    if ds[i] == "\\N":
                        ds[i] = "null"
                    else:
                        ds[i] = int(ds[i])
        else:
            for i in range(length):
                if ds[i].find("'") >= 0:
                    index = ds[i].find("'")
                    try:
                        ds[i] = "".join([ds[i][:index], "\\", ds[i][index:]])
                    except:
                        print([ds[i][:index], "\\", ds[i][index:]])
                        exit(1)
                if ds[i] == "\\N":
                    ds[i] = "null"
                else:
                    ds[i] = "".join(['"', ds[i], '"'])

    # print([data[i][0] for i in range(len(key))])
    for i in range(len(key)):
        key[i] = "".join(['"', key[i], '"'])
    data_len = len(data[0])
    for i in range(data_len):
        dic = "{"
        for j in range(len(key)):
            dic = " ".join([dic, "".join([key[j], ":", str(data[j][i]), ", "])])
        if dic[-2] == "," and dic[-1] == " ":
            dic = dic[: len(dic) - 2]
        dic = "".join([dic, "},\\\n" if i < data_len - 1 else "}\\\n"])
        f.writelines(dic)
    f.writelines("]';")


datasets = []
datasets.append(
    {
        "file_name": "airports",
        "key": [
            "Airport ID",
            "Name",
            "City",
            "Country",
            "IATA",
            "ICAO",
            "Latitude",
            "Longitude",
            "Altitude",
            "Timezone",
            "DST",
            "Tz",
            "Type",
            "Source",
        ],
    }
)
datasets.append(
    {
        "file_name": "airlines",
        "key": [
            "Airline ID",
            "Name",
            "Alias",
            "IATA",
            "ICAO",
            "Callsign",
            "Country",
            "Active",
        ],
    }
)
datasets.append(
    {
        "file_name": "routes",
        "key": [
            "Airline ID",
            "Source airport",
            "Source airport ID",
            "Destination airport",
            "Destination airport ID",
            "Codeshare",
            "Stops",
            "Equipment",
        ],
    }
)
datasets.append(
    {
        "file_name": "planes",
        "key": ["IATA code", "ICAO code"],
    }
)


# format of datas = [[feature1], [feature2],...]
for dataset in datasets:
    datas = extract(dataset["file_name"] + ".dat")

    # generate_CSV(datas, dataset['key'], dataset['file_name'])
    generate_fake_JSON(datas, dataset["key"], dataset["file_name"])
