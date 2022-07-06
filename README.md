## 简介

宁大附院CTF战队工具【AWD测试攻击框架】，当前版本v0.2

虽然之前借用了好多大佬的工具，还是难逃重复造轮子的覆辙，毕竟还是自己搓的最顺手。

## 使用环境
python3

## 使用方式
python3 main.py

## 功能模块

- **main.py：**  主程序入口

- **init_ip.py：**  生成IP池，校验index.php是否存在  

    - ⚠️**核对本文件，确认靶机范围和白名单IP**
    
- **init_shell.py：**  shell清单维护,可选择get/post两种方式，eval/system两种函数调用
    
- **exp_shell.py：**  shell利用,遍历IP池和Shell清单，对所有资产进行操作

    - 支持直接获取flag/自动定时获取flag/上传shell目录中木马/执行自定义命令 
    
    - ⚠️**核对本文件中靶机flag存放位置以及正则匹配式**
 
- **common.py：**  公用函数库
    
- **config目录：** 保存资产列表、Shell清单
    
- **shell目录：**  保存已经收集的shell样本
    
- **log.txt：**  运行监控日志，可删除
    
- **flag.txt：**  保存历史flag，可删除
    
## 更新日志

[v0.2](https://github.com/JasonJHu/AWD_gogogo/releases/tag/v0.2) 命令行版本基本功能已完成，尝试重构GUI版本

