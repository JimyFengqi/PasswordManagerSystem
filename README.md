# PasswordManagerSystem

- GUI Password Manager by PyQt5 
- 这是一个简单，但拥有基本功能的桌面单机版密码管理软件
- 采用SQLite，全部数据保存在单个文件中，便于备份

## 最大特点：能够把数据备份发送到邮箱中

## 采用 PyQt5 编写：开源、容易修改、跨平台

- Python 是一种简洁易读的语言，Qt 文档非常详细
- 采用 PyQt5 编写的程序，三大桌面平台均可轻松运行
- PyQt5 用来写些自用的带 GUI 界面的小软件，是一个很好的选择
- 本软件虽然简单但一些常用的桌面GUI基用法都用到了，完全可以作为一个入门参考示例

## 安装和使用

1. 安装 Python3（我自己用的3.6.6）
2. `pip install PyQt5`
`pip install sqlite3`
'pip3 install pyqt5'
'pip3 install pyqt5-tools'
'pip3 install sqilte3'
'pip3 install Image'
'pip3 install pyinstaller'

3. 下载本程序源代码
  - https://github.com/JimyFengqi/PasswordManagerSystem/archive/master.zip

4. `python PasswordManageSystem.py`
  - 这一步正式运行程序
  
5.如果想要使用邮箱备份功能，请申请一个自己的邮箱授权码

修改以下代码中的  password,send_user,user_list
class SendEmail():
    global send_user
    global email_host
    global password
    password = "abcdefghijklmn" #邮箱授权码
    email_host = "smtp.qq.com"
    send_user = "test@qq.com"
    user_list = ['test@qq.com','test@163.com']