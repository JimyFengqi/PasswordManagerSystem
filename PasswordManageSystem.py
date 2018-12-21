# -*- coding: utf-8 -*-
# @Date     : 2018-12-17 16:50:23
# @Author   : Jimy_Fengqi (jmps515@163.com)
# @Link     : https://blog.csdn.net/qiqiyingse
# @Version  : V1.0
# @pyVersion: 3.6

import sys,sqlite3,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import *
import images

import smtplib
from email.mime.text import MIMEText

class SendEmail():
    global send_user
    global email_host
    global password
    password = "abcdefghijklmn" #邮箱授权码
    email_host = "smtp.qq.com"
    send_user = "test@qq.com"
    user_list = ['test@qq.com','jmps515@163.com','meng.jiang@ericsson.com']
    sub = "密码备份"

    def __init__(self):
        self.server = smtplib.SMTP_SSL()
        self.server.connect(email_host,465)
        code,resp=server.login(send_user,password)
        if code in (235, 503):
            print('login success')

        user = "shape" + "<" + send_user + ">"
        self.message = MIMEText(content,_subtype='plain',_charset='utf-8')
        self.message['Subject'] = sub
        self.message['From'] = user
        self.message['To'] = ";".join(user_list)


    def send_textmail(self,content):
        text_plain = MIMEText(content,'plain', 'utf-8')    
        self.message.attach(text_plain)
  

    def __close__(self):
        self.server.close()

    def send_Enclosuremail(self,filename):
        #构造附件
        sendfile=open(filename,'rb').read()
        text_att = MIMEText(sendfile, 'base64', 'utf-8') 
        text_att["Content-Type"] = 'application/octet-stream'  
        #以下附件可以重命名成aaa.txt  
        #text_att["Content-Disposition"] = 'attachment; filename="aaa.txt"'
        #另一种实现方式
        text_att.add_header('Content-Disposition', 'attachment', filename=filename)
        #以下中文测试不ok
        #text_att["Content-Disposition"] = u'attachment; filename="中文附件.txt"'.decode('utf-8')
        message.attach(text_att) 

    def sendmail(self,content,file):
        self.send_mail(content)
        self.send_Enclosuremail(content)
        self.server.sendmail(user,user_list,message.as_string())

class PWKeeper(QMainWindow):

    def __init__(self):
        super(PWKeeper, self).__init__()
        self.initToolbar()
        self.initDB()
        self.initGrid()
        #self.current_row = 0
        self.setGeometry(300, 300, 650, 300)
        self.setWindowTitle('密码管理器')
        self.setWindowIcon(QIcon(':images/logo.jpg'))

    def initToolbar(self):
        newAction = QAction(QIcon(':images/new.png'), 'New Ctrl+N', self)
        editAction = QAction(QIcon(':images/edit.png'), 'Edit Ctrl+E', self)
        delAction = QAction(QIcon(':images/del.png'), 'Delete', self)
        backupAction = QAction(QIcon(':images/backup.png'), 'Backup Ctrl+B', self)
        newAction.setShortcut('Ctrl+N')
        editAction.setShortcut('Ctrl+E')
        delAction.setShortcut('Delete')
        backupAction.setShortcut('Ctrl+B')
        newAction.triggered.connect(self.newAction_def)
        editAction.triggered.connect(self.editAction_def)
        delAction.triggered.connect(self.delAction_def)
        backupAction.triggered.connect(self.backupAction_def)
        self.tb_new = self.addToolBar('New')
        self.tb_edit = self.addToolBar('Edit')
        self.tb_del = self.addToolBar('Del')
        self.tb_backup = self.addToolBar('Backup')
        self.tb_new.addAction(newAction)
        self.tb_edit.addAction(editAction)
        self.tb_del.addAction(delAction)
        self.tb_backup.addAction(backupAction)

    def backupAction_def(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM INFO')
        data = cur.fetchall()
        print(len(data))
        a=' '.join(['Website', 'Username', 'Password', 'Url'])+'\n'
        for items in data:
            for item in items:
                a=a+str(item)+' '
            a =a+'\n'

        myEmail=SendEmail()
        myEmail.sendmail(a,self.dbpath)


    def initDB(self):
        home = os.path.expanduser('~')
        if '.PasswordManageSystem' not in os.listdir(home):
            os.mkdir(os.path.join(home, '.PasswordManageSystem'))

        self.dbpath = os.path.join(home, '.PasswordManageSystem', 'PasswordManagement.db')

        if os.path.exists(self.dbpath):
            self.conn = sqlite3.connect(self.dbpath)
            self.conn.isolation_level = None
        else:
            self.conn = sqlite3.connect(dbpath)
            self.conn.isolation_level = None
            self.conn.execute('''CREATE TABLE INFO
                        (ID int PRIMARY KEY NOT NULL,
                        WEBSITE char(255),
                        USERNAME char(255),
                        PASSWORD char(255),
                        URL char(255))''')
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM INFO')
        self.displayData = cur.fetchall()
        cur.close()
        self.current_row = len(self.displayData)


    def initGrid(self):
        self.grid = QTableWidget()
        self.setCentralWidget(self.grid)
        self.grid.setColumnCount(4)
        self.grid.setRowCount(0)
        column_width = [75, 150, 270, 150]
        for column in range(4):
            self.grid.setColumnWidth(column, column_width[column])
        headerlabels = ['Website', 'Username', 'Password', 'Url']
        self.grid.setHorizontalHeaderLabels(headerlabels)
        self.grid.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.grid.setSelectionBehavior(QAbstractItemView.SelectRows)
        for row in range(len(self.displayData)):#根据数据库数据的数目，决定循环次数
            self.grid.insertRow(row)            #插入一行
            data = self.displayData[row]        #获取一条数据
            for i in range(4):
                item=data[i+1]                #获取一条数据中的一个元素
                #print(row, i, item)
                new_item = QTableWidgetItem(item)    #将数据转化为QTableWidgetItem
                self.grid.setItem(row, i, new_item)    #插入数据

       



    def newAction_def(self):
        data = self.showDialog()
        if data[0]:
            self.current_row += 1
            self.conn.execute("INSERT INTO INFO VALUES(%d, '%s', '%s', '%s', '%s')"
                              % (self.current_row, data[1], data[2], data[3], data[4]))
            self.grid.insertRow(self.current_row - 1)
            for i in range(4):
                new_item = QTableWidgetItem(data[i + 1])
                self.grid.setItem(self.current_row - 1, i, new_item)

    def editAction_def(self):
        selected_row = self.grid.selectedItems()
        if selected_row:
            edit_row = self.grid.row(selected_row[0])
            old_data = []
            for i in range(4):
                old_data.append(self.grid.item(edit_row, i).text())
            new_data = self.showDialog(*old_data)
            if new_data[0]:
                self.conn.execute('''UPDATE INFO SET
                                 WEBSITE = '%s', USERNAME = '%s',
                                 PASSWORD = '%s', URL = '%s'
                                 WHERE ID = '%d' '''
                              % (new_data[1], new_data[2], new_data[3], new_data[4], edit_row + 1))
                for i in range(4):
                    new_item = QTableWidgetItem(new_data[i + 1])
                    self.grid.setItem(edit_row, i, new_item)
        else:
            self.showHint()

    def delAction_def(self):
        selected_row = self.grid.selectedItems()
        if selected_row:
            del_row = self.grid.row(selected_row[0])
            self.grid.removeRow(del_row)
            self.conn.execute("DELETE FROM INFO WHERE ID = %d" % (del_row + 1))
            for index in range(del_row + 2, self.current_row + 1):
                self.conn.execute("UPDATE INFO SET ID = %d WHERE ID = %d" % ((index - 1), index))
            self.current_row -= 1
        else:
            self.showHint()
   
    def showHint(self):
        hint_msg = QMessageBox()
        hint_msg.setText('No selected row!')
        hint_msg.addButton(QMessageBox.Ok)
        hint_msg.exec_()

    def showDialog(self, ws = '', un = '', pw = '', url = ''):
	    edit_dialog = QDialog(self)
	    group = QGroupBox('Edit Info', edit_dialog)

	    lbl_website = QLabel('Website:', group)
	    le_website = QLineEdit(group)
	    le_website.setText(ws)
	    lbl_username = QLabel('Username:', group)
	    le_username = QLineEdit(group)
	    le_username.setText(un)
	    lbl_password = QLabel('Password:', group)
	    le_password = QLineEdit(group)
	    le_password.setText(pw)
	    lbl_url = QLabel('Url:', group)
	    le_url = QLineEdit(group)
	    le_url.setText(url)
	    ok_button = QPushButton('OK', edit_dialog)
	    cancel_button = QPushButton('CANCEL', edit_dialog)

	    ok_button.clicked.connect(edit_dialog.accept)
	    ok_button.setDefault(True)
	    cancel_button.clicked.connect(edit_dialog.reject)

	    group_layout = QVBoxLayout()
	    group_item = [lbl_website, le_website,
	                  lbl_username, le_username,
	                  lbl_password, le_password,
	                  lbl_url, le_url]
	    for item in group_item:
	        group_layout.addWidget(item)
	    group.setLayout(group_layout)
	    group.setFixedSize(group.sizeHint())

	    button_layout = QHBoxLayout()
	    button_layout.addWidget(ok_button)
	    button_layout.addWidget(cancel_button)

	    dialog_layout = QVBoxLayout()
	    dialog_layout.addWidget(group)
	    dialog_layout.addLayout(button_layout)
	    edit_dialog.setLayout(dialog_layout)
	    edit_dialog.setFixedSize(edit_dialog.sizeHint())

	    if edit_dialog.exec_():
	        website = le_website.text()
	        username = le_username.text()
	        password = le_password.text()
	        url = le_url.text()
	        return True, website, username, password, url
	    return False, None, None, None, None


class Login():
    pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pwk = PWKeeper()
    pwk.show()
    app.exec_()
    pwk.conn.close()
    sys.exit(0)