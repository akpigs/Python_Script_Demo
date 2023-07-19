import os
import datetime
import argparse

def change_file_modified_date(file_path, new_date):
    # 获取文件的当前修改日期和访问日期
    stat = os.stat(file_path)
    current_date = datetime.datetime.fromtimestamp(stat.st_mtime)

    # 计算新的访问日期时间差
    time_delta = new_date - current_date

    # 修改文件的修改日期和访问日期
    os.utime(file_path, (stat.st_atime + time_delta.total_seconds(), stat.st_mtime + time_delta.total_seconds()))

def change_files_in_directory(directory, new_date):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            change_file_modified_date(file_path, new_date)
            print(f"Modified date of '{file_path}' has been changed to {new_date}")

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description="Change file modification dates.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-a", "--all", type=str, help="Change all files in the specified directory")
group.add_argument("-f", "--file", type=str, help="Change the modification date of a specific file")
parser.add_argument("date", type=str, help="New date (YYYY-MM-DD)")

# 解析命令行参数
args = parser.parse_args()

# 解析日期参数
new_date = datetime.datetime.strptime(args.date, "%Y-%m-%d")

if args.all:
    # 修改指定目录下所有文件的修改日期
    directory = args.all
    if os.path.isdir(directory):
        change_files_in_directory(directory, new_date)
    else:
        print("Invalid directory path.")
elif args.file:
    # 修改指定文件的修改日期
    file_path = args.file
    if os.path.isfile(file_path):
        change_file_modified_date(file_path, new_date)
        print(f"Modified date of '{file_path}' has been changed to {args.date}")
    else:
        print("Invalid file path.")



# import os
# import time
# import datetime
#
# # 简易版本
# def change_file_modified_date(file_path, new_date):
#     # 将日期转换为时间戳
#     timestamp = time.mktime(new_date.timetuple())
#
#     # 修改文件的修改日期
#     os.utime(file_path, (timestamp, timestamp))
#
# # 示例用法
# file_path = 'C:/Users/admin/OneDrive/桌面/shellcode测试.txt'  # 替换为你要修改的文件路径
# new_date = datetime.datetime(1999, 5, 10)  # 替换为你想要的日期
#
# change_file_modified_date(file_path, new_date)
# print("修改成功！")