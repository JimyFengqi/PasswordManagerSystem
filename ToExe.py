# -*- coding: utf-8 -*-
# @Date     : 2018-12-21 10:09:50
# @Author   : Jimy_Fengqi (jmps515@163.com)
# @Link     : https://blog.csdn.net/qiqiyingse
# @Version  : V1.0
# @pyVersion: 3.6


import  os

if __name__ == '__main__':
    from PyInstaller.__main__ import *
    opts=['PasswordManageSystem.py','-F','-w','--icon=logo.ico','-p','images.py','--hidden-import','images']
    run(opts)