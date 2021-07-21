import csv
from datetime import datetime, timedelta

'''
根据csv原始数据中： 窑味料量、头煤的变化 去掉一定前后区间的间跃值

 10秒
 10分
 1小时

 https://stackoverflow.com/questions/16286991/converting-yyyy-mm-dd-hhmmss-date-time

'''
targe_filename = "2020_04-2021-05_SouthChinaSea.csv"

path = "data/" + targe_filename

#实际处理 注释掉这行
# path = "HXDataSample/" + targe_filename

newpath = "processeddata/" + targe_filename

bufsize = 65536*6*3
#实际处理 注释掉这行
# bufsize = 5000

#窑味料量
Feeding_index = 28
HeadCoal_index = 29

def process(lines):
    time_need_removed = []
    rows = []
    for i in range(0, len(lines)):

        # print(lines[i], '#'*10)

        if '2020-04' in lines[i] or '2020-05' in lines[i]:
            rows.append(lines[i])
            print(lines[i], '@'*10)
        # else:
        #     print(lines[i])
    return rows







def main():
    # header = get_header(path)
    # print('header=', header)
    # write_count = 0
    with open(path, encoding="UTF-8") as infile:
        while True:
            lines = infile.readlines(bufsize)
            print('len(lines)=', len(lines))
            if not lines:
                break

            rows = process(lines)
            # print('process len(rows)=', len(rows), rows, '-'*10, '\n')
            # for r in rows:
            #     print(r, '#'*10, '\n')
            with open(newpath, "a", newline="") as csvfile:                            
                writer = csv.writer(csvfile) 

                # if write_count == 0:
                #     writer.writerow(header)
                # write_count += 1
                for row in rows:
                    writer.writerow(row.split(','))

if __name__ == "__main__":
    main()
