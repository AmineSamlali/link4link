# amine 9ade sql online 9ade mashalkeel dtsawer dm1
import bcrypt
import clipboard
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QSpinBox
import sys
from PyQt5.uic import loadUiType
import os
import source_rc
from os import path
import datetime
import sqlite3
import random
import webbrowser
from hashlibb import *
##########
superuser_username = 'admin'
superuser_password = 'admin'
##########
## calculator variables
after = False
error_after = False
ans = None
##########
value_link = None
"""
Program programmer : "Amine Samlali"
mail : samlaliamine2@gmail.com
number phone = '212 619135651'
Donation On PayPal : https://paypal.me/AmineSamlali
"""
ui, _ = loadUiType('Main.ui')
ui_Login, _ = loadUiType('Login.ui')
ui_profile, _ = loadUiType('profile.ui')
ui_admin, _ = loadUiType('admin.ui')
username_PRF = None
password_PRF = None
redirectnum1 = None
run = []
db_name = 'links4link.db'
def CreateTables():
    global db_name
    conn = sqlite3.connect(f'{db_name}')
    accounts = conn.cursor().execute(''' CREATE TABLE  IF NOT EXISTS "accounts" (
			"user_id"	INTEGER NOT NULL,
			"username"	text,
			"email"	text,
			"password"	text,
			PRIMARY KEY("user_id")
		) ''')
    profiles = conn.cursor().execute(''' CREATE TABLE  IF NOT EXISTS "profiles" 
					(
                        "profile_id"	INTEGER NOT NULL,
                        "username"	TEXT UNIQUE,
                        "First_Name"	text,
                        "Last_Name"	text,
                        "Phone_Number"	text,
                        "WebSite_URL"	text,
                        "administration"	text,
                        "user_points"	INTEGER DEFAULT 0,
                        "mylinks"	INTEGER DEFAULT 0,
                        "refferal_by"	TEXT,
                        "refferal_code"	TEXT,
                        "date"	NUMERIC,
                        "refP"	INTEGER DEFAULT 0,
                        "level"	TEXT DEFAULT 'جديد',
                        PRIMARY KEY("profile_id")  
			) ''')
    addlinks = conn.cursor().execute(''' CREATE TABLE  IF NOT EXISTS "addlinks" (
	"id"	INTEGER,
	"username"	INTEGER,
	"short_link"	TEXT,
	"Sherelink"	TEXT,
	"clickes"	INTEGER,
	"Total_Clicks"	INTEGER DEFAULT 0,
	"Va_Code"	INTEGER UNIQUE,
	"status"	TEXT DEFAULT 'Pending',
	"date"	TEXT,
	"report_users"	INTEGER DEFAULT 0,
	"Earned_users"	TEXT,
	"report_skiped"	TEXT DEFAULT 'None,',
	PRIMARY KEY("id")
) ''')
    settings = conn.cursor().execute(''' CREATE TABLE  IF NOT EXISTS "settings" (
		"oneclick"	INTEGER,
		"Earn_points"	INTEGER,
		"min_points"	INTEGER,
		"Refferal_earn"	INTEGER,
		"Refferal_shoud"	INTEGER,
		"id"	INTEGER,
		"auto"	INTEGER DEFAULT 0,
		"title"	INTEGER,
		PRIMARY KEY("id"))  ''')
    payment = conn.cursor().execute(''' CREATE TABLE IF NOT EXISTS "payment" (
	"name"	TEXT,
	"method"	TEXT,
	"more_information"	TEXT) ''')
    conn.commit()
CreateTables()
class MainAppLogin(QMainWindow, ui_Login):
    def __init__(self, parent=None):
        super(MainAppLogin, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Connection()
        self.profile()
        global redirectnum1
        if redirectnum1 == 'logout':
            self.lineEdit.setText('')
            self.lineEdit_3.setText('')
            self.checkBox.setChecked(False)
            file = open('log_login.txt', 'w')
            file.write(' ')
            file.close()
    def Open_signup(self):
        self.window2 = MainApp()
        self.close()
        self.window2.show()
    def Login_app_and_redirect(self):
        try:
            global username_PRF
            global password_PRF
            global superuser_username
            global superuser_password
            global db_name
            username = self.lineEdit.text()
            password = self.lineEdit_3.text()
            conn = sqlite3.connect(f'{db_name}')
            c = conn.cursor()
            p = conn.cursor()
            c.execute(f'''SELECT * FROM accounts WHERE username="{username}" ''')
            if str(superuser_username) == str(username) and str(password) == str(superuser_password):
                username_PRF = superuser_username
                password_PRF = superuser_password
                self.close()
                self.window8 = MainAppAdmin()
                self.window8.show()
            elif len(username) == 0 or len(password) == 0:
                QMessageBox.warning(self, 'Error', "Please Enter True Values")
            elif username == 'username':
                pass
            elif username != 'username':
                login_db = list(c.fetchone())
                c.execute(f'''SELECT * FROM accounts WHERE username="{username}" ''')
                p.execute(f''' SELECT administration FROM profiles WHERE username="{username}" ''')
                data = c.fetchone()
                login_redirec = p.fetchone()
                if data[0] != "True":
                    # if login_db[1] == username and (login_db[3] == password):
                    if login_db[1] == username and check_pw_hash(password , login_db[3]) == True:
                        if login_redirec[0] != 'True':
                            if self.checkBox.isChecked():
                                log_login = [username, password, True]
                                file = open('log_login.txt', 'w')
                                file.write(f'{log_login}')
                                file.close()
                                username_PRF = username
                                password_PRF = password
                                self.window2 = MainAppProfile()
                                self.close()
                                self.window2.show()
                            else:
                                if self.checkBox.isChecked() == False:
                                    file = open('log_login.txt', 'w')
                                    file.write(' ')
                                    file.close()
                                    QMessageBox.information(self, 'Done', f'WELCOME BACK {username}')
                                    username_PRF = username
                                    password_PRF = password
                                    password_PRF = password
                                    self.window2 = MainAppProfile()
                                    self.close()
                                    self.window2.show()
                        else:
                            self.window5 = MainAppAdmin()
                            self.close()
                            self.window5.show()
                    else:
                        QMessageBox.warning(self, 'خطأ', 'اسم المستخدم او الرقم السري غير صحيح')
                        print('amine')
        except:
            QMessageBox.warning(self, 'خطأ', 'اسم المستخدم او الرقم السري غير صحيح')
            print('aminee')

    def profile(self):
        try:
            file = open('log_login.txt', 'r')
            data = file.read()
            final_data = data[2:-1].replace("'", '').replace(',', '').split(' ')
            self.lineEdit.setText(final_data[0])
            self.lineEdit_3.setText(final_data[1])
            self.checkBox.setChecked(True)
            file.close()
        except:
            pass

    def Connection(self):
        self.pushButton.clicked.connect(self.Login_app_and_redirect)
        self.pushButton_5.clicked.connect(self.Open_signup)


class MainAppAdmin(QMainWindow, ui_admin):
    def __init__(self, parent=None):
        super(MainAppAdmin, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.connections()
        self.add_items()
        global username_PRF
        global password_PRF
        global superuser_username
        global superuser_password
        global db_name
        if username_PRF == superuser_username:
            self.pushButton.setEnabled(True)
        try:
            self.admin_links_managments()
            self.admin_man()
            self.comboBox_items_add()
            conn = sqlite3.connect(f'{db_name}')
            c = conn.cursor()
            t = conn.cursor()
            panding_links = conn.cursor()
            managments = conn.cursor()
            setting_DATA = conn.cursor()
            setting_Complete = conn.cursor()
            setting_Running = conn.cursor()
            refferal_sys = conn.cursor()
            c.execute(''' SELECT username FROM accounts''')
            self.pushButton_5.setEnabled(False)
            self.checkBox.setEnabled(False)
            setting_DATA.execute(''' SELECT * FROM settings ''')
            datax = setting_DATA.fetchall()
            self.lineEdit_4.setText(str(datax[0][7]))
            self.lineEdit.setText(str(datax[0][0]))
            self.lineEdit_2.setText(str(datax[0][1]))
            self.lineEdit_6.setText(str(datax[0][2]))
            self.lineEdit_14.setText(str(datax[0][3]))
            self.lineEdit_15.setText(str(datax[0][4]))
            self.setWindowTitle(str(datax[0][7]))
            if datax[0][6] == 1:
                self.checkBox_2.setChecked(True)
            else:
                self.checkBox_2.setChecked(False)
            self.links_tables()
        except:
            pass
    def comboBox_items_add(self):
        global db_name
        conn = sqlite3.connect(f'{db_name}').cursor().execute(''' SELECT name FROM payment ''').fetchall()
        self.comboBox_7.clear()
        self.comboBox_7.addItem('------------------')
        for item  in conn:
            self.comboBox_7.addItem(str(item[0]))
    def admin_man(self):
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        setting_DATA = conn.cursor()
        setting_Complete = conn.cursor()
        setting_Running = conn.cursor()
        setting_Complete.execute(''' SELECT * FROM addlinks WHERE status="Completed" ''')
        setting_DATA.execute(''' SELECT * FROM addlinks WHERE status="Pending" ''')
        setting_Running.execute(''' SELECT * FROM addlinks WHERE status="Running" ''')
        self.label_26.setText(str(len(setting_DATA.fetchall())))
        self.label_24.setText(str(len(setting_Complete.fetchall())))
        self.label_23.setText(str(len(setting_Running.fetchall())))
        self.links_tables()
    def auto(self):
        global db_name
        conn = sqlite3.connect(f"{db_name}")
        boool = self.checkBox_2.isChecked()
        if boool == False:
            J = conn.cursor().execute(''' UPDATE settings SET  auto="0" WHERE id=1 ''')
            conn.commit()
        else:
            J = conn.cursor().execute(''' UPDATE settings SET  auto="1" WHERE id=1 ''')
            conn.commit()
    def links_tables(self):
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        c = conn.cursor()
        statuss = self.comboBox_2.currentText()
        if statuss == '------------------':
            managmentss = c.execute(''' SELECT * FROM addlinks''')
        else:
            managmentss = c.execute(f''' SELECT * FROM addlinks WHERE status="{statuss}" ''')
        links_data = managmentss.fetchall()
        self.label_21.setText(str(len(links_data)))
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, item in enumerate(links_data):
            for cul, items in enumerate(item):
                self.tableWidget.setItem(row, cul, QTableWidgetItem(str(items)))
                cul += 1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
    def ONOROF(self):
        global db_name
        try:
            conn = sqlite3.connect(f'{db_name}')
            c = conn.cursor()
            onoroff = self.comboBox_3.currentText()
            id = self.lineEdit_3.text()
            if onoroff == 'On':
                c.execute(f''' UPDATE addlinks SET status="Running" WHERE id="{int(id)}" ''')
                conn.commit()
                self.lineEdit_3.setText('')
                self.admin_man()
            elif onoroff == 'Off':
                c.execute(f''' UPDATE addlinks SET status="Blocked" WHERE id="{int(id)}" ''')
                conn.commit()
                self.lineEdit_3.setText('')
                self.admin_man()
            else:
                pass
        except:
            QMessageBox.information(self, 'خطأ', 'جرب مرة اخرى')
            self.lineEdit_3.setText('')
    def add_items(self):
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        c = conn.cursor()
        c.execute(''' SELECT username FROM profiles''')
        for item in c.fetchall():
            if item[0] == username_PRF:
                continue
            else:
                self.comboBox.addItem(item[0])
    def Search_user(self):
        global amine
        global db_name
        text = self.lineEdit_13.text()
        self.comboBox.clear()
        conn = sqlite3.connect(f'{db_name}')
        clean = conn.cursor()
        clean.execute(''' SELECT username FROM profiles  ''')
        check = conn.cursor()
        for item in clean.fetchall():
            if item[0].startswith(f'{text}'):
                self.comboBox.addItem(item[0])
            else:
                continue
        if self.comboBox.count() == 0:
            QMessageBox.information(self, 'Error', 'There is no user with this name')
            self.lineEdit_13.setText('')
            self.add_items()
    def Profile_admin_status(self):
        try:
            global username_PRF
            global password_PRF
            global superuser_username
            global superuser_password
            global db_name
            conn = sqlite3.connect(f'{db_name}')
            c = conn.cursor()
            t = conn.cursor()
            c.execute(''' SELECT username FROM accounts''')
            comboBox = self.comboBox.currentText()
            if comboBox == '-------------------':
                self.lineEdit_8.setText('')
                self.lineEdit_9.setText('')
                self.lineEdit_10.setText('')
                self.lineEdit_11.setText('')
                self.lineEdit_12.setText('')
                self.lineEdit_20.setText('')
                self.lineEdit_21.setText('')
                self.spinBox.setValue(0)
                self.checkBox.setChecked(False)
            else:
                if username_PRF == superuser_username and password_PRF == superuser_password:
                    if len(comboBox) != 0:
                        self.pushButton_5.setEnabled(True)
                        self.checkBox.setEnabled(True)
                        self.lineEdit_8.setEnabled(True)
                        self.lineEdit_9.setEnabled(True)
                        self.lineEdit_10.setEnabled(True)
                        self.lineEdit_11.setEnabled(True)
                        self.lineEdit_12.setEnabled(True)
                        self.lineEdit_20.setEnabled(True)
                        self.lineEdit_21.setEnabled(True)
                        self.pushButton_4.setEnabled(True)
                        self.spinBox.setEnabled(True)
                else:
                    self.pushButton_5.setEnabled(False)
                    self.checkBox.setEnabled(False)
                conn = sqlite3.connect(f'{db_name}')
                c = conn.cursor()
                t = conn.cursor()
                c.execute(f''' SELECT * FROM profiles WHERE username = "{comboBox}" ''')
                t.execute(f'''SELECT email  FROM accounts WHERE username ="{comboBox}"''')
                email_data = t.fetchall()
                data = c.fetchall()
                self.lineEdit_8.setText(data[0][2])
                self.lineEdit_9.setText(data[0][3])
                self.lineEdit_10.setText(email_data[0][0])
                self.lineEdit_11.setText(data[0][4])
                self.lineEdit_12.setText(data[0][5])
                self.lineEdit_20.setText(data[0][10])
                self.lineEdit_21.setText(str(data[0][8]))
                self.spinBox.setValue(int(data[0][7]))
                if data[0][6] == 'False':
                    self.checkBox.setChecked(False)
                else:
                    self.checkBox.setChecked(True)
        except:
            QMessageBox.warning(self,'Error' , 'Please Try Again !')
    def ProfileEditeInformations(self):
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        c = conn.cursor()
        username = self.comboBox.currentText()
        First_Name = self.lineEdit_8.text()
        Last_Name = self.lineEdit_9.text()
        Email_Name = self.lineEdit_10.text()
        Phone_Number = self.lineEdit_11.text()
        WebSite_URL = self.lineEdit_12.text()
        user_points = self.spinBox.value()
        reffera_code = self.lineEdit_20.text()
        refferal_by = self.lineEdit_21.text()
        if self.checkBox.isChecked():
            administration = 'True'
        else:
            administration = 'False'
        c.execute(
            f''' UPDATE profiles SET First_Name='{First_Name}' , Last_Name='{Last_Name}' , Phone_Number='{Phone_Number} ', WebSite_URL='{WebSite_URL}' , administration='{administration}',user_points="{user_points}",refferal_by="{refferal_by}",refferal_code="{reffera_code}" WHERE username="{username}"''')
        t = conn.cursor()
        t.execute(f''' UPDATE accounts SET email='{Email_Name}' WHERE username="{username}"''')
        QMessageBox.information(self, 'Done', 'The information has been saved successfully')
        QMessageBox.information(self, 'Done', 'The information has been saved successfully')
        conn.commit()
    def DELETE_profile(self):
        global db_name
        username = self.comboBox.currentText()
        conn = sqlite3.connect(f'{db_name}')
        delate = conn.cursor()
        delate_user = conn.cursor()
        delate_user.execute(f''' DELETE FROM accounts WHERE username= "{username}" ''')
        delate.execute(f''' DELETE FROM profiles WHERE username='{username}'  ''')
        delate_links = conn.cursor().execute(f''' DELETE FROM addlinks WHERE username="{username}" ''')
        conn.commit()
        self.comboBox.clear()
        self.add_items()
    def admin_settings_link(self):
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        setting = conn.cursor()
        p = conn.cursor()
        setting_DATA = conn.cursor()
        oneclick = self.lineEdit.text()
        Earn_points = self.lineEdit_2.text()
        min_points = self.lineEdit_6.text()
        Refferal_earn = self.lineEdit_14.text()
        Refferal_shoud = self.lineEdit_15.text()
        title = self.lineEdit_4.text()
        p.execute(''' SELECT * FROM settings ''')
        try:
            if p.fetchall() == []:
                setting.execute(
                    f''' INSERT INTO settings (oneclick,Earn_points ,min_points,Refferal_earn,Refferal_shoud , title) VALUES ("{oneclick}","{Earn_points}","{min_points}","{Refferal_earn}","{Refferal_shoud}" ,"{title}") ''')
                conn.commit()
                QMessageBox.information(self, 'منجز', 'تم تسجيل الإعدادات')
            else:
                setting.execute(
                    f''' UPDATE settings SET oneclick="{oneclick}",Earn_points="{Earn_points}",min_points="{min_points}",Refferal_earn="{Refferal_earn}",Refferal_shoud="{Refferal_shoud}" ,title="{title}" WHERE id=1 ''')
                conn.commit()
                QMessageBox.information(self, 'تم تحديث الإعدادات', 'تم تحديث الإعدادات')
        except:
            QMessageBox.warning(self, 'Error', 'Please Try Again !')

    def admin_links_managments(self):
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        c = conn.cursor()
        managmentss = c.execute(''' SELECT * FROM addlinks ''')
        links_data = managmentss.fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, item in enumerate(links_data):
            for cul, items in enumerate(item):
                self.tableWidget.setItem(row, cul, QTableWidgetItem(str(items)))
                cul += 1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
        status = self.comboBox_2.currentText()
        if status == '------------------':
            self.tableWidget.setRowCount(0)
            self.tableWidget.insertRow(0)
            for row, item in enumerate(links_data):
                for cul, items in enumerate(item):
                    self.tableWidget.setItem(row, cul, QTableWidgetItem(str(items)))
                    cul += 1
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
        else:
            conn = sqlite3.connect(f'{db_name}')
            c = conn.cursor()
            status = self.comboBox_2.currentText()
            filter = c.execute(f''' SELECT * FROM addlinks WHERE status="{status}" ''')
            links_data = filter.fetchall()
            self.tableWidget.setRowCount(0)
            self.tableWidget.insertRow(0)
            for row, item in enumerate(links_data):
                for cul, items in enumerate(item):
                    self.tableWidget.setItem(row, cul, QTableWidgetItem(str(items)))
                    cul += 1
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)

    def payment(self):
        global db_name
        name = self.lineEdit_31.text()
        way = self.lineEdit_32.text()
        info = self.textEdit.toPlainText()
        combo = self.comboBox_7.currentText()
        if combo == '------------------':
            if len(name) != 0 and len(way) != 0 and len(info) != 0:
                self.pushButton_17.setEnabled(False)
                conn = sqlite3.connect(f'{db_name}')
                conn.cursor().execute(f''' INSERT INTO payment(name,method,more_information) VALUES("{name}"  , "{way}" ,  "{info}") ''')
                conn.commit()
                QMessageBox.information(self ,'تم',"تم اضافة الوسلة بنجاح")
                self.comboBox_items_add()
                self.lineEdit_31.setText('')
                self.lineEdit_32.setText('')
                self.textEdit.setText('')

            else:
                QMessageBox.warning(self , 'خطأ' ,'المرجو ملء جميع الحقول')
        else:
            if len(name) != 0 and way != 0 and info != 0:
                db = sqlite3.connect(f'{db_name}')
                o = db.cursor().execute(f''' UPDATE payment SET name ="{name}", method ="{way}", more_information="{info}" WHERE name="{combo}" ''')
                db.commit()
                QMessageBox.information(self, 'نجاح', 'تم التعديل بنجاح')
                self.comboBox_items_add()
                self.lineEdit_31.setText('')
                self.lineEdit_32.setText('')
                self.textEdit.setText('')

    def edite_payment(self):
        combo = self.comboBox_7.currentText()
        name = self.lineEdit_31.text()
        way = self.lineEdit_32.text()
        info = self.textEdit.toPlainText()
        if combo != '------------------':
            self.pushButton_16.setText('تعديل')
            conn = sqlite3.connect(f'{db_name}').cursor().execute(f''' SELECT name,method,more_information FROM payment WHERE name="{combo}" ''').fetchone()
            self.lineEdit_31.setText(conn[0])
            self.lineEdit_32.setText(conn[1])
            self.textEdit.setText(conn[2])
            self.pushButton_17.setEnabled(True)
        else:
            self.pushButton_16.setText('اضف الوسيلة')
            self.lineEdit_31.setText('')
            self.lineEdit_32.setText('')
            self.textEdit.setText('')
            self.pushButton_17.setEnabled(False)
    def Delete_A_payment(self):
        global db_name
        name = self.lineEdit_31.text()
        conn = sqlite3.connect(f'{db_name}')
        delate_user = conn.cursor()
        delate_user.execute(f''' DELETE FROM payment WHERE name="{name}" ''')
        conn.commit()
        self.comboBox_items_add()
        QMessageBox.information(self,'تم','تم حدف الوسيلة بنجاح')
        self.lineEdit_31.setText('')
        self.lineEdit_32.setText('')
        self.textEdit.setText('')
    def connections(self):
        self.pushButton_3.clicked.connect(self.Profile_admin_status)
        self.pushButton_4.clicked.connect(self.ProfileEditeInformations)
        self.pushButton_5.clicked.connect(self.DELETE_profile)
        self.pushButton_6.clicked.connect(self.Search_user)
        self.pushButton.clicked.connect(self.admin_settings_link)
        self.pushButton_2.clicked.connect(self.admin_links_managments)
        self.pushButton_7.clicked.connect(self.ONOROF)
        self.pushButton.clicked.connect(self.auto)
        self.pushButton_16.clicked.connect(self.payment)
        self.pushButton_15.clicked.connect(self.edite_payment)
        self.pushButton_17.clicked.connect(self.Delete_A_payment)
class MainAppProfile(QMainWindow, ui_profile):
    def __init__(self, parent=None):
        super(MainAppProfile, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.connections()
        global username_PRF
        global password_PRF
        global superuser_username
        global superuser_password
        global db_name
        self.Profile()
        self.link_home()
        self.Refferal_SYS()
        self.COUNTERLINKS()
        self.account_level()
        try:
            self.label_35.setText(username_PRF)
            conn = sqlite3.connect(f'{db_name}')
            ky = conn.cursor().execute(
                ''' SELECT Refferal_earn , Refferal_shoud  FROM settings WHERE id='1' ''').fetchone()
            c = conn.cursor()
            link_clicks_one = conn.cursor()
            text1 = ' سوف يتم إضافة ' + f'{ky[0]}' f' نقطة إلى رصيدك مباشرة عندما يقوم المستخدم الذي قمت بإستدعائه بربح {ky[1]} نقاط في حسابه كما يظهر لك في الجدول جميع المستخدمين المتسجلون في الموقع من خلالك و حالتهم قيد الإنتضار  مازال لم يضف رابط , مفعل  تمت إضافة النقاط لرصيدك '
            self.plainTextEdit_10.setPlainText(text1)
            link_clicks_one.execute(''' SELECT  min_points,oneclick FROM  settings WHERE id=1 ''')
            dataas = link_clicks_one.fetchall()
            self.label_30.setText(str(dataas[0][0]))
            self.spinBox.setMinimum(dataas[0][0])
            self.label_27.setText(str(dataas[0][1]))
        except:
            pass
        data = conn.cursor().execute(''' SELECT name FROM payment  ''').fetchall()
        for item in data:
            self.comboBox.addItem(item[0])
        VCODEe = conn.cursor()
        VCODEe.execute(''' SELECT Va_Code FROM addlinks  ''')
        VCODEes = VCODEe.fetchone()
        VCODE = random.randrange(138718, 19873981)
        VCODE = self.lineEdit_9.setText(str(VCODE))
        self.mylinks_link()
        conn = sqlite3.connect(f'{db_name}')
        c = conn.cursor()
        c.execute(''' SELECT username FROM accounts''')
        titile = conn.cursor().execute(''' SELECT title FROM settings WHERE id=1 ''').fetchone()
        try:
            self.setWindowTitle(str(titile[0]))
        except:
            self.setWindowTitle(str('Links4link'))
    def payment(self):
        global db_name
        try:
            conn = sqlite3.connect(f'{db_name}').cursor()
            getname = self.comboBox.currentText()
            get = conn.execute(f''' SELECT method , more_information FROM payment WHERE name="{getname}"  ''').fetchone()
            self.lineEdit_32.setText(str(get[0]))
            self.textEdit_2.setText(str(get[1]))
        except:
            pass
    def account_level(self):
        global username_PRF
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        level = conn.cursor().execute(f''' SELECT level FROM profiles WHERE username="{username_PRF}" ''').fetchone()
        lenn = conn.cursor().execute(
            f''' SELECT short_link FROM addlinks WHERE username="{username_PRF}" ''').fetchall()
        if len(lenn) < 20:
            conn.cursor().execute(f''' UPDATE profiles SET level="جديد" ''')
        elif 19 < len(lenn) < 30:
            conn.cursor().execute(f''' UPDATE profiles SET level="نشط" ''')
        elif 30 < len(lenn):
            conn.cursor().execute(f''' UPDATE profiles SET level="موتوق" ''')
        conn.commit()
        self.label_10.setText(level[0])
    def COUNTERLINKS(self):
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        count_links = conn.cursor()
        dataC = count_links.execute(f''' SELECT id FROM addlinks WHERE username="{username_PRF}" ''')
        self.label_8.setText(str(len(dataC.fetchall())))

    def Profile(self):
        global username_PRF
        global password_PRF
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        c = conn.cursor()
        checking = conn.cursor()
        username = username_PRF
        First_Name = self.lineEdit.text()
        Last_name = self.lineEdit_2.text()
        Phone_Number = self.lineEdit_3.text()
        WebSite_URL = self.lineEdit_4.text()
        c.execute("""SELECT username FROM profiles """)
        checking.execute(
            f''' SELECT First_Name , Last_Name , Phone_Number ,WebSite_URL FROM profiles WHERE username="{username}"''')
        check = checking.fetchall()
        if check[0][0] == "NUll" or check[0][1] == 'NUll' or check[0][2] == 'NUll' or check[0][3] == "NUll":
            self.tabWidget.setCurrentIndex(0)
            if username_PRF != None and len(First_Name) != 0 and len(Last_name) != 0 and len(Phone_Number) != 0:
                c.execute(
                    f''' UPDATE profiles SET First_Name="{First_Name}" ,Last_Name="{Last_name}" ,Phone_Number="{Phone_Number}" ,WebSite_URL="{WebSite_URL}" ,administration="False" WHERE username="{username}"''')
                conn.commit()
                QMessageBox.information(self, 'منجز', 'تم تسجيل ملفك الشخصي ')
                self.tabWidget.setCurrentIndex(1)
        elif check[0][0] != "NUll" and check[0][1] != 'NUll' and check[0][2] != 'NUll' and check[0][3] != 'NUll':
            self.tabWidget.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, 'خطأ', 'الرجاء إدخال القيم الحقيقية ')

    def exite_logout(self):
        global username_PRF
        global password_PRF
        global redirectnum1
        redirectnum1 = 'logout'
        username_PRF = None
        password_PRF = None
        self.window9 = MainAppLogin()
        self.close()
        self.window9.show()

    def Refferal_SYS(self):
        global username_PRF
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        c = conn.cursor()
        t = conn.cursor()
        plus = conn.cursor()
        addself = conn.cursor()
        addrefpoints = conn.cursor()
        getpoints = conn.cursor()
        getsettings = conn.cursor()
        data_settings = getpoints.execute(''' SELECT Refferal_earn,Refferal_shoud FROM settings WHERE id=1 ''')
        finnalsetting = data_settings.fetchone()
        selfpoints = getpoints.execute(f''' SELECT user_points FROM profiles WHERE username="{username_PRF}"  ''')
        selfpointsx = selfpoints.fetchall()
        RFF = t.execute(f''' SELECT refferal_code FROM profiles WHERE username="{username_PRF}" ''')
        data1 = RFF.fetchall()
        self.lineEdit_12.setText(data1[0][0])
        self.lineEdit_7.setText(data1[0][0])
        data = c.execute(f''' SELECT username ,refP FROM profiles WHERE refferal_by="{data1[0][0]}"''')
        finnal_data = data.fetchall()
        self.label_47.setText(str(len(finnal_data)))
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        for row, item in enumerate(finnal_data):
            for cul, items in enumerate(item):
                if items == 1:
                    self.tableWidget_2.setItem(row, cul, QTableWidgetItem(str('مفعل')))
                elif items == 0:
                    self.tableWidget_2.setItem(row, cul, QTableWidgetItem(str('في الانتظار')))
                else:
                    self.tableWidget_2.setItem(row, cul, QTableWidgetItem(str(items)))
                cul += 1

            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)
        for user in finnal_data:
            plusw = plus.execute(f''' SELECT user_points,refP FROM profiles WHERE username="{user[0]}" ''')
            datta = plus.fetchone()
            if datta[1] == 0:
                if datta[0] >= finnalsetting[1]:
                    addrefpoints.execute(
                        f''' UPDATE profiles SET user_points={int(datta[0] + finnalsetting[1])},refP=1 WHERE username="{user[0]}" ''')
                    data_seelf_ser = addself.execute(
                        f''' UPDATE profiles SET user_points={int(selfpointsx[0][0] + finnalsetting[1])} WHERE username="{username_PRF}" ''')
                    conn.commit()
                else:
                    continue
            self.link_home()

    def link_home(self):
        global username_PRF
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        c = conn.cursor()
        c.execute(f''' SELECT * FROM profiles WHERE username='{username_PRF}' ''')
        points = c.fetchone()
        self.label_7.setText(str(points[7]))
        self.label_8.setText(str(points[8]))
        self.lineEdit_7.setText(str(points[10]))
        self.lineEdit_12.setText(str(points[10]))
        self.label_19.setText(str(points[7]))
        self.label_18.setText(str(points[7]))
        self.label_46.setText(str(points[7]))

    def copy(self):
        text = self.lineEdit_12.text()
        textx = text.strip()
        clipboard.copy(f"{textx}")

    def copy2(self):
        text = self.lineEdit_7.text()
        textx = text.strip()
        clipboard.copy(f"{textx}")

    def link_ADDLINKS(self):
        global username_PRF
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        c = conn.cursor()
        o = conn.cursor()
        link = conn.cursor()
        c.execute(''' SELECT * FROM settings WHERE id=1 ''')
        data = c.fetchall()
        o.execute(f''' SELECT user_points FROM profiles WHERE username="{username_PRF}" ''')
        SHORTCODE = self.lineEdit_10.text()
        SHERELINK = self.lineEdit_11.text()
        clickes_number = self.spinBox.value()
        VCODE = self.lineEdit_9.text()
        if len(SHORTCODE) != 0 and len(SHERELINK) != 0 and clickes_number != 0:
            try:
                if int(clickes_number) >= int(data[0][2]):
                    datta = o.fetchall()
                    if int(datta[0][0]) >= int(data[0][2]) * int(clickes_number):
                        try:
                            link.execute(
                                f''' INSERT INTO addlinks (username,short_link,Sherelink,clickes,Total_Clicks,Va_Code,status,date,report_users,Earned_users) VALUES("{username_PRF}","{SHORTCODE}","{SHERELINK}","{clickes_number}" ,"0","{VCODE}", "Pending","{datetime.datetime.now()}","0","{username_PRF},") ''')
                        except Exception:
                            VCODE = random.randrange(13831718, 198739211)
                        num1 = int(data[0][2]) * int(clickes_number)
                        points_user = int(datta[0][0])
                        o.execute(
                            f''' UPDATE profiles SET user_points="{points_user - num1}" WHERE username="{username_PRF}" ''')
                        conn.commit()
                        self.account_level()
                        self.label_7.setText(str(points_user - num1))
                        self.label_8.setText(str(points_user - num1))
                        # self.lineEdit_7.setText(str(points_user-num1))
                        self.label_19.setText(str(points_user - num1))
                        self.label_18.setText(str(points_user - num1))
                        self.label_46.setText(str(points_user - num1))
                        self.mylinks_link()
                        self.lineEdit_9.setText(str(random.randrange(138718, 19873981)))
                        QMessageBox.information(self, 'نجاح', 'رابطك قيد المعالجة')
                        self.lineEdit_10.setText('')
                        self.lineEdit_11.setText('')
                        self.spinBox.setValue(0)
                        self.COUNTERLINKS()
                    else:
                        QMessageBox.warning(self, "خطأ", 'لا تمتكل العدد المطلوب من النقاط')
            except IndexError:
                QMessageBox.warning(self, "خطأ", 'لا تمتكل العدد المطلوب من النقاط')
        else:
            QMessageBox.warning(self, "خطأ", 'الموجو ادخال جميع الحقول')

    def mylinks_link(self):
        global username_PRF
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        c = conn.cursor()
        c.execute(
            f''' SELECT short_link ,clickes ,report_users,Total_Clicks,status FROM addlinks WHERE username="{username_PRF}" ''')
        data = c.fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, item in enumerate(data):
            for cul, items in enumerate(item):
                self.tableWidget.setItem(row, cul, QTableWidgetItem(str(items)))
                cul += 1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    def Running_links(self):
        global username_PRF
        global value_link
        global db_name
        try:
            conn = sqlite3.connect(f'{db_name}')
            c = conn.cursor()
            s = conn.cursor()
            setting_data = s.execute(''' SELECT Earn_points FROM settings WHERE id=1 ''')
            setting_data_f = setting_data.fetchone()
            safe_links = []
            c.execute(
                ''' SELECT Sherelink ,Va_Code , Earned_users ,report_skiped FROM addlinks WHERE status="Running" ''')
            data = c.fetchall()
            for link in data:
                if link[2] != None and link[3] != None:
                    if username_PRF in link[2] or username_PRF in link[3]:
                        continue
                    else:
                        safe_links.append(link)
                else:
                    safe_links.append(link)
            webbrowser.open(f'{safe_links[0][0]}')
            value_link = safe_links[0][0]
            print(f'{value_link}')
        except Exception:
            QMessageBox.warning(self, 'المعدرة', 'لا توجد اي روابط')
    def Running_links_VEri(self):
        global value_link
        global username_PRF
        global db_name
        if value_link != None:
            conn = sqlite3.connect(f'{db_name}')
            c = conn.cursor()
            u = conn.cursor()
            e = conn.cursor()
            ee = conn.cursor()
            setting = conn.cursor().execute(''' SELECT Earn_points FROM settings WHERE id=1 ''')
            pointts = setting.fetchone()
            eee = ee.execute(f''' SELECT user_points FROM profiles WHERE username="{username_PRF}" ''')
            up = conn.cursor()
            eeee = eee.fetchone()
            VVcode = self.lineEdit_8.text()
            get_instanse = e.execute(f''' SELECT Earned_users FROM addlinks WHERE Va_Code="{VVcode}" ''')
            c.execute(f''' SELECT Va_Code , Total_Clicks ,clickes FROM addlinks WHERE Sherelink="{value_link}" ''')
            d = c.fetchone()
            print(d[0])
            get_instansee = get_instanse.fetchone()
            if str(d[0]) == str(VVcode):
                getself = conn.cursor()
                dattaa = getself.execute(f''' SELECT Total_Clicks FROM addlinks WHERE Va_Code="{VVcode}" ''')
                points = dattaa.fetchone()
                u.execute(
                    f''' UPDATE addlinks SET Earned_users="{get_instansee[0]},{username_PRF}" ,Total_Clicks={int(points[0] + 1)} WHERE Va_Code="{VVcode}" ''')
                adddd = up.execute(
                    f''' UPDATE profiles SET user_points="{int(eeee[0] + pointts[0])}" WHERE username="{username_PRF}" ''')
                conn.commit()
                if str(d[1]) == str(d[2]):
                    complated = conn.cursor().execute(
                        f''' UPDATE addlinks SET status="Completed" WHERE Va_Code="{d[0]}" ''')
                    conn.commit()
                self.link_home()
                QMessageBox.information(self, 'نجاح', 'تم اضافة النقاط الى حسابك')
                self.lineEdit_8.setText('')
                value_link = None
            else:
                QMessageBox.warning(self, 'خطأ', 'المرجو ادخال الشفرة الصحيحة')
        else:
            QMessageBox.warning(self, 'خطأ', 'المرجو فتح الرابط للرابط')

    def report_for_link(self):
        try:

            global value_link
            print(f'--- {value_link}')
            global username_PRF
            global db_name
            conn = sqlite3.connect(f'{db_name}')
            aut = conn.cursor().execute(''' SELECT auto FROM settings WHERE id=1 ''').fetchone()
            CODE = conn.cursor().execute(
                f''' SELECT Va_Code ,report_skiped , report_users FROM addlinks WHERE Sherelink="{value_link}" ''').fetchone()
            if int(aut[0]) == 0:
                o = conn.execute(
                    f''' UPDATE addlinks SET report_users={int(CODE[2]) + 1} ,report_skiped="{CODE[1]}-{username_PRF}" WHERE Va_Code="{CODE[0]}" ''')
            else:
                if int(CODE[2]) >= 5:
                    o = conn.execute(
                        f''' UPDATE addlinks SET report_users={int(CODE[2])} ,report_skiped="{CODE[1]}-{username_PRF}",status="Blocked" WHERE Va_Code="{CODE[0]}" ''')
            conn.commit()
            QMessageBox.information(self, 'شكرا', 'شكرا لقد ابلغة على الرابط')
            value_link = None
            # print("POLPPPO")
        except:
            QMessageBox.warning(self, 'خطأ', 'المرجو فتح الرابط للرابط')

    def account_mdps(self):
        global username_PRF
        global db_name
        try:
            conn = sqlite3.connect(f'{db_name}')
            auto = conn.cursor().execute(
                f''' SELECT password FROM accounts WHERE username="{username_PRF}" ''').fetchone()
            autoo = conn.cursor()
            old_pass = self.lineEdit_5.text()
            Npassword1 = self.lineEdit_6.text()
            Npassword2 = self.lineEdit_13.text()
            # if auto[0] == old_pass:
            if len(old_pass) != 0 and  len(Npassword1) != 0 and len(Npassword2) != 0:
                if check_pw_hash(old_pass , auto[0]) == True:
                    if len(Npassword1) > 8 and len(Npassword2) > 8:
                        if Npassword1 == Npassword2:
                            autoo.execute(
                                f''' UPDATE accounts SET password="{make_pw_hash(Npassword2)}" WHERE username="{username_PRF}" ''')
                            conn.commit()
                            QMessageBox.information(self, 'صحيح', '! لقد تم التعديل على كلمة المرور')
                            self.lineEdit_5.setText('')
                            self.lineEdit_6.setText('')
                            self.lineEdit_13.setText('')
                        else:
                            QMessageBox.warning(self, 'خطأ', 'كلمة اسر غير متطابقة')
                    else:
                        QMessageBox.warning(self, 'خطأ', 'يجب ان تكون كلمة السر اكبر من 8 احرف')
                else:
                    QMessageBox.warning(self, 'خطأ', 'خطأ في كلمة السر اقديمة')
            else:
                QMessageBox.warning(self, 'خطأ', 'المرجو ادخال جميع المعلومات')
        except:
            QMessageBox.warning(self, 'خطأ', 'حاول مرة اخرى')
    def connections(self):
        self.pushButton.clicked.connect(self.Profile)
        self.pushButton_32.clicked.connect(self.link_ADDLINKS)
        self.pushButton_33.clicked.connect(self.mylinks_link)
        self.pushButton_29.clicked.connect(self.Running_links)
        self.pushButton_30.clicked.connect(self.Running_links_VEri)
        self.pushButton_31.clicked.connect(self.report_for_link)
        self.pushButton_2.clicked.connect(self.copy)
        self.pushButton_26.clicked.connect(self.copy2)
        self.pushButton_34.clicked.connect(self.account_mdps)
        self.action.triggered.connect(self.exite_logout)
        self.action_2.triggered.connect(lambda: self.close())
        self.pushButton_3.clicked.connect(self.payment)
class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.connection()
    def signUp(self):
        global db_name
        conn = sqlite3.connect(f'{db_name}')
        c = conn.cursor()
        profile = conn.cursor()
        checkinnng = conn.cursor()
        username = self.lineEdit.text()
        email = self.lineEdit_2.text()
        password1 = self.lineEdit_3.text()
        password2 = self.lineEdit_4.text()
        check_box = self.checkBox.isChecked()
        reefferalBY = self.lineEdit_6.text()
        if len(username) == 0 or len(email) == 0 or len(password1) == 0 or len(password2) == 0:
            QMessageBox.warning(self, "Error", 'Please Don\'t Enter  Empty information\'s')
        else:
            if '@' in email:
                if len(username) >= 8:
                    if len(password1) >= 8:
                        if password1 == password2:
                            if password1 != username or password2 != username:
                                if check_box:
                                    emty_list = []
                                    for i in c.execute(''' SELECT username FROM accounts'''):
                                        username_db = i[0]
                                        emty_list.append(username_db)
                                    if username in emty_list:
                                        QMessageBox.warning(self, 'خطأ', 'أسم المستخدم مأخوذ مسبقا')
                                    else:
                                        c.execute(
                                            f''' INSERT INTO accounts (  username ,email , password ) values(  "{username}"  , "{email}"  , "{make_pw_hash(password1)}")''')
                                        conn.commit()
                                        if len(reefferalBY) == 0:
                                            refferal = random.randrange(1, 90)
                                            profile.execute(
                                                f''' INSERT INTO profiles (username , First_Name,Last_Name,Phone_Number,WebSite_URL,administration,refferal_by,refferal_code,date) VALUES ("{username}" ,"NUll","NUll","NUll","NUll","NUll","NUll","{username}-{refferal}","{datetime.datetime.now()}") ''')
                                            conn.commit()
                                            QMessageBox.information(self, 'منجز', 'تم تسجيل حسابك  ')
                                            self.lineEdit.setText('')
                                            self.lineEdit_2.setText('')
                                            self.lineEdit_3.setText('')
                                            self.lineEdit_4.setText('')
                                            self.checkBox.setChecked(False)
                                            self.window4 = MainAppLogin()
                                            self.close()
                                            self.window4.show()
                                        else:
                                            checking_ref = checkinnng.execute(
                                                f''' SELECT username FROM profiles WHERE refferal_code="{reefferalBY}" ''')
                                            data_ref = checking_ref.fetchall()
                                            if not data_ref:
                                                QMessageBox.warning(self, 'خطأ', 'رمز الإحالة هذا غير صالح')
                                            else:
                                                refferal = random.randrange(12,123)
                                                profile.execute(
                                                    f''' INSERT INTO profiles (username , First_Name,Last_Name,Phone_Number,WebSite_URL,administration,refferal_by,refferal_code,date) VALUES ("{username}" ,"NUll","NUll","NUll","NUll","NUll","{reefferalBY}","{username}-{refferal}","{datetime.datetime.now()}") ''')
                                                conn.commit()
                                                QMessageBox.information(self, 'منجز', 'تم تسجيل حسابك  ')
                                                self.lineEdit.setText('')
                                                self.lineEdit_2.setText('')
                                                self.lineEdit_3.setText('')
                                                self.lineEdit_4.setText('')
                                                self.checkBox.setChecked(False)
                                                self.window4 = MainAppLogin()
                                                self.close()
                                                self.window4.show()
                                else:
                                    QMessageBox.warning(self, 'خطأ', 'يرجى تأكيد خانة الاختيار ')
                            else:
                                QMessageBox.warning(self, 'خطأ',
                                                    'اسم المستخدم مشابه جدًا لكلمة المرور يرجى المحاولة مرة أخرى ! ')
                        else:
                            QMessageBox.warning(self, 'خطأ', 'أدخل نفس كلمة المرور ')
                    else:
                        QMessageBox.warning(self, 'خطأ', 'يجب أن تحتوي كلمة المرور على 8 أحرف على الأقل ')
                else:
                    QMessageBox.warning(self, 'خطأ', 'يجب أن يحتوي اسم المستخدم على 8 أحرف على الأقل ')
            else:
                QMessageBox.warning(self, 'خطأ', 'الرجاء إدخال بريد إلكتروني صحيح')
    def Open_Login(self):
        self.window = MainAppLogin()
        self.close()
        self.window.show()
    def connection(self):
        self.pushButton.clicked.connect(self.signUp)
        self.pushButton_4.clicked.connect(self.Open_Login)
def main_login():
    app = QApplication(sys.argv)
    window = MainAppLogin()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main_login()