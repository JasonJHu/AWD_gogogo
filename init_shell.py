# coding=utf-8
# 现有后门相关维护
import os
import time
import common
import requests

localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
sShellFile = "./config/shell_list.txt"
sIPFile = "./config/ip_list.txt"


def chkShell_get(sURL):
    blnResult = False
    sResult = ""
    try:
        res = requests.get(sURL, timeout=1)
        if res.status_code == 200:
            sResult = sURL + " status is " + str(res.status_code)
            blnResult = True
        else:
            sResult = sURL + " status is " + str(res.status_code)
    except:
        pass

    if blnResult:
        print("[+]%s" % sResult)
    common.log("[CHECK_SHELL]" + sResult)


def removeShell():
    print("...进行清理操作")
    if common.file_check(sShellFile):
        backupShell()
        common.file_remove(sShellFile)
    print("...清理完成")


def backupShell():
    if common.file_check(sShellFile):
        strBakFile = "./config/shell_list_" + str(time.strftime("%Y%m%d_%H%M%S", time.localtime())) + ".txt"
        print("...进行备份操作")
        sFile = common.file_load(sShellFile)
        common.file_write(strBakFile,sFile.strip())
        print("        ==>%s" % strBakFile)
        print("...备份完成")
    else:
        print("...未发现源文件")


def showShell():
    if common.file_check(sShellFile):
        strShells = common.file_load(sShellFile)
        print("====>%s<====" % sShellFile)
        print(strShells)
    else:
        print("...未发现源文件")


def addShell(sShell="",sMedthod="",sArg=""):
    print("...进行新增操作")
    blnContinue = True

    while 1:
        if sShell=="":
            print("-" * 16)
            print("当前位置：/Shell管理/新增")
            strURI = input("请输入shell的相对位置（例如：/shell/shell.php,输入0返回）：")
            if strURI == "0":
                return
        else:
            strURI = sShell

        if sMedthod=="":
            print("-" * 16)
            print("当前位置：/Shell管理/新增--%s" % strURI)
            print("1.get_eval    2.get_system")
            print("3.post_eval    4.post_system")
            print("    eval:eval/assert/...")
            print("    system:system/passthru/shell_exec/exec/popen/...")

            strMethod = input("请选择调用方式：")

            if strMethod == "1":
                strMethod = "get_eval"
            elif strMethod == "2":
                strMethod = "get_system"
            elif strMethod == "3":
                strMethod = "post_eval"
            elif strMethod == "4":
                strMethod = "post_system"
            else:
                print("选择错误！")
                continue
        else:
            strMethod=sArg

        if sArg=="":
            print("-" * 16)
            print("当前位置：/Shell管理/新增--%s,%s" % (strURI, strMethod))
            strArg = input("请输入调用参数（例如：x）：")
        else:
            strArg=sArg

        common.file_write(sShellFile, strURI + "," + strMethod + "," + strArg)
        print("...已插入    %s,%s,%s" % (strURI, strMethod, strArg))
        if input("    回车继续，返回输(0):").upper() == '0':
            break


def checkShell():
    print("...进行验证操作")
    if (common.file_check(sShellFile) == False):
        print("    shell文件未生成，请先生成shell清单！")
        return

    if (common.file_check(sIPFile) == False):
        print("    IP文件未生成，请先生成IP清单！")
        return

    lstIP = []
    strIPs = common.file_load(sIPFile).split("\r\n")

    for strIP in strIPs:
        if (strIP not in lstIP and len(strIP) > 0):
            lstIP.append(strIP)
    # print(lstIP)

    lstShell = []
    strShells = common.file_load(sShellFile).split("\r\n")

    for strShell in strShells:
        if (strShell not in lstShell and len(strShell) > 0):
            lstShell.append(strShell)
    # print(lstShell)

    for strIP in lstIP:
        for strShell in lstShell:
            ls = strShell.split(",")
            strURI = ls[0]
            strMethod = ls[1]
            strArg = ls[2]

            chkShell_get(strIP + strURI)


def main():
    print("====" + localtime + "====")
    print("shell文件操作开始\n请确认shell存放位置：%s" % sShellFile)
    while 1:
        print("-" * 16)
        print("当前位置：/Shell管理")
        print("1.清除    2.显示    3.备份    4.新增")
        print("5.验证    0.返回")
        strCMD = input("请选择操作类型：")

        if strCMD == "1":
            removeShell()
        elif strCMD == "2":
            showShell()
        elif strCMD == "3":
            backupShell()
        elif strCMD == "4":
            addShell()
        elif strCMD == "5":
            checkShell()
        elif strCMD == "0":
            return
        else:
            pass
    return
    
if __name__ == '__main__':
    main()