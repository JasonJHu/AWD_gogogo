import init_ip
import init_shell
import exp_shell
import time
import sys

strCMD=""


if __name__ == '__main__':
    while 1:
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        print("*"*10+localtime+"*"*10)
        print("欢迎使用宁大附院CTF战队工具——AWD攻击框架")
        print("现有模块：")
        print("1.资产维护    2.shell维护    3.shell利用")
        print("0.退出")
        strCMD =  input("请选择需要加载的模块:")
        
        if strCMD == "1":
            init_ip.main()
        elif strCMD == "2":
            init_shell.main()
        elif strCMD == "3":
            exp_shell.main()
        elif strCMD == "0":
            print("bye!!")
            sys.exit()
        else:
            continue
            
