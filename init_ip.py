# coding=utf-8
# 可对index.php/现有的后门/已经植入的不死马进行check

import requests, time
import common
from multiprocessing import Process

# 定义预制变量
localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
sIPFile="./config/IP_list.txt"
sLogFile="log.txt"
strIP1="192.168.1.1"
strIP2="192.168.1.2"
strIPPart1="192.168.1"
intIP_From=1
intIP_To=254
strIPPart2=""
webshell_path="/index.php"
strCheck="html"

def chkShell_get(shell_url):
    url = "http://"+shell_url + webshell_path

    common.log("[CHECK_URL]Checking %s" % url)
    
    try:
        res = requests.get(url,timeout=0.5)
        if res.status_code==200:
            if res.content.decode("utf-8").find(strCheck) != -1:
                content = "http://"+shell_url
                print("    %s is ACTIVE. "%url)
                # print("  Contents==>%s "%url)
                common.file_write(sIPFile, content)
            else :
                print("    %s is ACTIVE but ERROR !! "%url)
    except:
        pass

def chkFile():
    if (common.file_check(sIPFile) and common.file_check(sLogFile)):
        cmd = input("IP列表和日志文件已存在，是否清除（y/n）？")
        if (cmd.upper() == "Y"):
            common.file_remove(sIPFile)
            common.file_remove(sLogFile)
        else:
            print("...忽略删除...")

def main():
    print("====" + localtime + "====")

    # 检查相关文件是否存在
    chkFile()

    ### 资产发现开始
    pro_start_time = time.time()
    # 定义进程池
    p_lst = []
    # 限定进程数为10
    for IPRange in range(intIP_From,intIP_To+1,10):
        for i in range(10):
            ip = strIPPart1+str(IPRange+i)+strIPPart2 
            if (ip!=strIP1 and ip!=strIP2):
                p = Process(target=chkShell_get, args=(ip,))
                p.start()
                p_lst.append(p)
        [pp.join() for pp in p_lst]

    print(str(intIP_To+1-intIP_From)+" 个资产扫描完成，耗时: " + str(round(time.time() - pro_start_time, 2)) + " 秒")
    ### 资产发现结束
    
    return
    
if __name__ == '__main__':
    main()