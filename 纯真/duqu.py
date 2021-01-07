import csv
import pandas as pd
import numpy as np

# csv_file=csv.reader(open('场所ap ip.csv','r'))
# print(csv_file) #可以先输出看一下该文件是什么样的类型
#
# content=[] #用来存储整个文件的数据，存成一个列表，列表的每一个元素又是一个列表，表示的是文件的某一行
#
# for line in csv_file:
#     # print(line) #打印文件每一行的信息
#     content.append(line)
# print("该文件中保存的数据为:\n",content[1:])


with open("111.csv","r") as f:
    # reader = csv.reader(f)
    reader = csv.DictReader(f)
    csvFile = open("222.csv", "w" ,newline='')  # 创建csv文件
    writer = csv.writer(csvFile)  # 创建写的对象
    writer.writerow(["site_ap_ip", " ", "address"])  # 写入列的名称
    for row in reader:
        print(row['site_ap_ip'])
        print("------")
        # 先写入columns_name
        # 写入多行用writerows
        writer.writerow([row['site_ap_ip'], ' ', '浙江杭州'])
    csvFile.close()




# csvFile = open("222.csv", "w")  # 创建csv文件
# writer = csv.writer(csvFile)  # 创建写的对象
# writer.writerow(["site_ap_ip", " ", "address"])  # 写入列的名称
# writer.writerow(['1111111', ' ', '浙江杭州'])