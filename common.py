import os
import time

# 是否记录日志，打印明细
blnPrint = False

# 运行日志记录
sLogFile = "log.txt"


def file_load(filepath):
    try:
        file = open(filepath, "rb")
        return str(file.read().decode("utf-8"))
    except:
        print("File %s Not Found!" % filepath)
        return False

def file_write(filepath, filecontent):
    file = open(filepath, "a")
    file.write(filecontent+"\n")
    file.close()


def file_remove(filepath):
    os.remove(filepath)


def file_check(filepath):
    return os.path.exists(filepath)

def file_list(filepath):
    lstFile=[]
    for i in os.listdir(filepath):
        lstFile.append(i)
    return lstFile

def log(strInput):
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if blnPrint:
        print(strInput)
    file_write(sLogFile, "-"*16+"\n"+localtime + " " * 4 + strInput)
