# -*- encoding: utf-8 -*-
import sys
import sqlite3
import random

from PyQt5.QtWidgets import QApplication, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, \
    QLabel, QMainWindow, QLineEdit
from PyQt5 import QtCore

FOLDER_LANGUAGE = []
LANG_NUM = 1  # set_rus = 0 / set_eng = 1


class ManagerCreatWindow(QMainWindow):
    resized = QtCore.pyqtSignal()  # вещь для отслеживания изменения рамера окна

    def __init__(self):
        super().__init__()
        self.setWindowTitle('ManagementPW')  # заголовок
        self.setGeometry(250, 250, 800, 400)  # положение и размер при запуске
        self.setMinimumSize(440, 500)
        self.lang_num = LANG_NUM  # установка номера языка
        self.bool_edit_data = False
        self.pwd = ""

        # переменные
        self.table_arr = []
        self.data = []

        # кнопки
        self.btn_choice_lang = QPushButton(self)
        self.btn_rekey = QPushButton(self)
        self.btn_save = QPushButton(self)
        self.btn_add_new_pte = QPushButton(self)
        self.btn_del_last_pte = QPushButton(self)
        self.btn_generate_random_pwd = QPushButton(self)  # <- кнопка не в основном окне
        self.btn_generate_random_pwd.setVisible(0)
        self.btn_choice_lang_new_pwd = QPushButton(self)
        self.btn_choice_lang_new_pwd.setVisible(0)
        self.btn_conf_new_pwd = QPushButton(self)
        self.btn_conf_new_pwd.setVisible(0)
        self.lbl1_new_pwd = QLabel(self)
        self.lbl1_new_pwd.setVisible(0)
        self.lbl2_new_pwd = QLabel(self)
        self.lbl2_new_pwd.setVisible(0)
        self.lbl_error = QLabel(self)
        self.lbl_error.setVisible(0)

        # таблица
        self.table = QTableWidget(self)

        for _ in self.btn_choice_lang, self.btn_rekey, self.btn_save, self.btn_add_new_pte, \
                 self.btn_del_last_pte, self.table:
            _.setVisible(0)
            _.setEnabled(0)

        con = sqlite3.connect("language.sqlite")
        cur = con.cursor()
        pwd = cur.execute("""SELECT * FROM pwd""").fetchall()
        con.close()
        self.lbl_sovet = QLabel(self)
        self.lbl_lin1 = QLabel(self)
        self.input_line1 = QLineEdit(self)
        self.lbl_lin2 = QLabel(self)
        self.input_line2 = QLineEdit(self)
        self.lbl_lin1.setVisible(0)
        self.input_line1.setVisible(0)
        self.lbl_lin2.setVisible(0)
        self.input_line2.setVisible(0)
        if bool(pwd):  # если пароль существует
            self.lbl1_ent = QLabel(self)
            self.lbl2_ent = QLabel(self)
            self.btn_choice_lang_ent = QPushButton(self)
            self.btn_conf_ent = QPushButton(self)
            self.input_line_enter = QLineEdit(self)
            self.initUI_enter()
        else:  # если пароль не существует
            self.lbl1 = QLabel(self)
            self.lbl2 = QLabel(self)
            self.lbl3 = QLabel(self)
            self.lbl_lin1.setVisible(1)
            self.input_line1.setVisible(1)
            self.lbl_lin2.setVisible(1)
            self.input_line2.setVisible(1)
            self.btn_choice_lang_cr_pwd = QPushButton(self)
            self.btn_conf_cr_pwd = QPushButton(self)
            self.initUI_create_password()

    #######
    # приложение входа
    def initUI_enter(self):
        self.btn_choice_lang_ent.move(10, 10)  # кнопка выборя языка
        self.btn_choice_lang_ent.setText(FOLDER_LANGUAGE[2][self.lang_num])
        self.btn_choice_lang_ent.clicked.connect(self.choice_lang_ent)

        self.lbl1_ent.setText(FOLDER_LANGUAGE[14][self.lang_num])
        self.lbl1_ent.move(10, 40)
        self.lbl1_ent.setFixedWidth(500)

        self.lbl2_ent.setText(FOLDER_LANGUAGE[15][self.lang_num])
        self.lbl2_ent.move(10, 60)
        self.lbl2_ent.setFixedWidth(500)

        self.input_line_enter.resize(150, 25)
        self.input_line_enter.move(10, 90)

        self.btn_conf_ent.move(10, 130)  # кнопка выборя языка
        self.btn_conf_ent.setText("Continue")
        self.btn_conf_ent.clicked.connect(self.continue_ent)

    # установка номера языка
    def choice_lang_ent(self):
        if self.btn_choice_lang_ent.text() == "RUS":
            self.lang_num = 1
            self.btn_choice_lang_ent.setText("ENG")
        else:
            self.btn_choice_lang_ent.setText("RUS")
            self.lang_num = 2
        self.setting_lang_widgets_ent()

    # изменение языка текста виджетов
    def setting_lang_widgets_ent(self):
        self.btn_choice_lang_ent.setText(FOLDER_LANGUAGE[2][self.lang_num])
        self.lbl1_ent.setText(FOLDER_LANGUAGE[14][self.lang_num])
        self.lbl2_ent.setText(FOLDER_LANGUAGE[15][self.lang_num])
        self.btn_generate_random_pwd.setText(FOLDER_LANGUAGE[18][self.lang_num])

    # функция кнопки "continue", дальнейший запуск окна
    def continue_ent(self):
        self.pwd = self.input_line_enter.text()
        for _ in self.lbl1_ent, self.lbl2_ent, self.btn_choice_lang_ent, \
                 self.btn_conf_ent, self.input_line_enter:
            _.setEnabled(0)
            _.setVisible(0)
        for _ in self.btn_choice_lang, self.btn_rekey, self.btn_save, \
                 self.btn_add_new_pte, self.btn_del_last_pte, self.table:
            _.setVisible(1)
            _.setEnabled(1)
        self.initUI_main()

    #######
    # приложение создания пароля
    def initUI_create_password(self):
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle(FOLDER_LANGUAGE[9][self.lang_num])

        self.btn_choice_lang_cr_pwd.move(10, 10)  # кнопка выборя языка
        self.btn_choice_lang_cr_pwd.setText(FOLDER_LANGUAGE[2][self.lang_num])
        self.btn_choice_lang_cr_pwd.clicked.connect(self.choice_lang_cr_pwd)

        self.btn_generate_random_pwd.setVisible(1)
        self.btn_generate_random_pwd.move(200, 10)
        self.btn_generate_random_pwd.resize(200, self.btn_generate_random_pwd.height())
        self.btn_generate_random_pwd.setText(FOLDER_LANGUAGE[18][self.lang_num])
        self.btn_generate_random_pwd.clicked.connect(self.random_password)

        self.lbl1.setText(FOLDER_LANGUAGE[10][self.lang_num])
        self.lbl1.move(10, 40)
        self.lbl1.setFixedWidth(500)
        self.lbl2.setText(FOLDER_LANGUAGE[11][self.lang_num])
        self.lbl2.move(10, 55)
        self.lbl2.setFixedWidth(500)
        self.lbl3.setText(FOLDER_LANGUAGE[17][self.lang_num])
        self.lbl3.move(10, 70)
        self.lbl3.setFixedWidth(500)

        self.lbl_lin1.setText(FOLDER_LANGUAGE[12][self.lang_num])
        self.lbl_lin1.move(40, 100)
        self.lbl_lin1.setFixedWidth(200)
        self.input_line1.resize(150, 30)
        self.input_line1.move(40, 130)

        self.lbl_error.setFixedWidth(800)
        self.lbl_error.move(200, 130)

        self.lbl_lin2.setText(FOLDER_LANGUAGE[13][self.lang_num])
        self.lbl_lin2.move(40, 160)
        self.lbl_lin2.setFixedWidth(200)
        self.input_line2.resize(150, 30)
        self.input_line2.move(40, 190)

        self.btn_conf_cr_pwd.setText("Create")
        self.btn_conf_cr_pwd.move(70, 240)
        self.btn_conf_cr_pwd.clicked.connect(self.check_crt_pwd)

        self.lbl_sovet.setText(FOLDER_LANGUAGE[16][self.lang_num])
        self.lbl_sovet.move(10, 300)
        self.lbl_sovet.setFixedWidth(500)

    # установка номера языка
    def choice_lang_cr_pwd(self):
        if self.btn_choice_lang_cr_pwd.text() == "RUS":
            self.lang_num = 1
            self.btn_choice_lang_cr_pwd.setText("ENG")
        else:
            self.btn_choice_lang_cr_pwd.setText("RUS")
            self.lang_num = 2
        self.setting_lang_widgets_cr_pwd()

    # изменение языка текста виджетов
    def setting_lang_widgets_cr_pwd(self):
        self.lbl1.setText(FOLDER_LANGUAGE[10][self.lang_num])
        self.lbl2.setText(FOLDER_LANGUAGE[11][self.lang_num])
        self.lbl3.setText(FOLDER_LANGUAGE[17][self.lang_num])
        self.lbl_lin1.setText(FOLDER_LANGUAGE[12][self.lang_num])
        self.lbl_lin2.setText(FOLDER_LANGUAGE[13][self.lang_num])
        self.lbl_sovet.setText(FOLDER_LANGUAGE[16][self.lang_num])
        self.btn_generate_random_pwd.setText(FOLDER_LANGUAGE[18][self.lang_num])
        self.lbl_error.setText(FOLDER_LANGUAGE[21][self.lang_num])

    # функция кнопки "continue", сохранение паорля, дальнейший запуск окна
    def check_crt_pwd(self):
        s1 = self.input_line1.text()
        s2 = self.input_line2.text()
        f = self.check_good_pwd(s1, s2)
        if f == 1:
            for _ in self.lbl1, self.lbl2, self.lbl3, self.lbl_lin1, self.input_line1, \
                     self.lbl_lin2, self.input_line2, self.btn_choice_lang_cr_pwd, \
                     self.btn_conf_cr_pwd, self.lbl_sovet, self.btn_generate_random_pwd, \
                     self.lbl_error:
                _.setEnabled(0)
                _.setVisible(0)
            for _ in self.btn_choice_lang, self.btn_rekey, self.btn_save, \
                     self.btn_add_new_pte, self.btn_del_last_pte, self.table:
                _.setVisible(1)
                _.setEnabled(1)
            self.pwd = self.input_line2.text()
            self.save_pwd()
            self.initUI_main()
        else:
            self.lbl_error.setText(f)

    #######
    # основное приложение
    def initUI_main(self):
        x, y = 10, 10

        self.btn_choice_lang.move(x, y)  # кнопка выборя языка
        self.btn_choice_lang.setText(FOLDER_LANGUAGE[2][self.lang_num])
        self.btn_choice_lang.clicked.connect(self.choice_lang)
        x += self.btn_choice_lang.width()
        self.btn_rekey.move(x, y)  # кнопка смены пороля
        self.btn_rekey.setFixedWidth(100)
        self.btn_rekey.clicked.connect(self.create_new_password)
        x += self.btn_rekey.width()
        self.btn_rekey.setText(FOLDER_LANGUAGE[0][self.lang_num])
        self.btn_save.move(x, y)  # кнопка сохранения данных
        self.btn_save.setFixedWidth(100)
        self.btn_save.setText(FOLDER_LANGUAGE[1][self.lang_num])
        self.btn_save.clicked.connect(self.save)
        self.btn_add_new_pte.clicked.connect(self.add_new_pte)  # кнопка создания новых полей
        self.btn_add_new_pte.move(10, self.height() - 28)
        self.btn_add_new_pte.setFixedWidth(150)
        self.btn_add_new_pte.setText(FOLDER_LANGUAGE[3][self.lang_num])
        self.btn_del_last_pte.clicked.connect(self.del_past_pte)  # кнопка удаления последнего поля
        self.btn_del_last_pte.move(160, self.height() - 28)
        self.btn_del_last_pte.setFixedWidth(150)
        self.btn_del_last_pte.setText(FOLDER_LANGUAGE[5][self.lang_num])
        self.table.move(10, 40)  # таблица информации
        self.table.resize(self.width() - 20, self.height() - 75)

        self.load_inform()
        self.first_load_table()
        self.resized.connect(self.setting_resize_widgets)

    # установка номера языка
    def choice_lang(self):
        if self.btn_choice_lang.text() == "RUS":
            self.lang_num = 1
            self.btn_choice_lang.setText("ENG")
        else:
            self.btn_choice_lang.setText("RUS")
            self.lang_num = 2
        self.setting_lang_widgets()

    # изменение языка текста виджетов
    def setting_lang_widgets(self):  # изменение языка текста виджетов
        self.btn_rekey.setText(FOLDER_LANGUAGE[0][self.lang_num])
        self.btn_save.setText(FOLDER_LANGUAGE[1][self.lang_num])
        self.btn_add_new_pte.setText(FOLDER_LANGUAGE[3][self.lang_num])
        if bool(self.data):
            if self.table.item(0, 0).text() == FOLDER_LANGUAGE[4][1] or \
                    self.table.item(0, 0).text() == FOLDER_LANGUAGE[4][2]:
                self.load_table_in_data()
                self.table.setItem(0, 0, QTableWidgetItem(FOLDER_LANGUAGE[4][self.lang_num]))
            if self.table.item(0, 1).text() == FOLDER_LANGUAGE[4][1] or \
                    self.table.item(0, 1).text() == FOLDER_LANGUAGE[4][2]:
                self.load_table_in_data()
                self.table.setItem(0, 1, QTableWidgetItem(FOLDER_LANGUAGE[4][self.lang_num]))
        self.btn_del_last_pte.setText(FOLDER_LANGUAGE[5][self.lang_num])

    def create_new_password(self):
        for _ in self.btn_choice_lang, self.btn_rekey, self.btn_save, self.btn_add_new_pte, \
                 self.btn_del_last_pte, self.table:
            _.setVisible(0)
            _.setEnabled(0)

        for _ in self.lbl_lin1, self.input_line1, self.lbl_lin2, self.input_line2, \
                 self.btn_generate_random_pwd, self.btn_conf_new_pwd, self.lbl1_new_pwd, \
                 self.lbl2_new_pwd, self.btn_choice_lang_new_pwd, self.lbl_error:
            _.setEnabled(1)
            _.setVisible(1)

        self.lbl1_new_pwd.setText(FOLDER_LANGUAGE[19][self.lang_num])
        self.lbl1_new_pwd.move(10, 40)
        self.lbl1_new_pwd.setFixedWidth(700)
        self.lbl2_new_pwd.setText(FOLDER_LANGUAGE[20][self.lang_num])
        self.lbl2_new_pwd.move(10, 55)
        self.lbl2_new_pwd.setFixedWidth(500)

        self.lbl_lin1.setText(FOLDER_LANGUAGE[12][self.lang_num])
        self.lbl_lin1.move(40, 100)
        self.lbl_lin1.setFixedWidth(200)
        self.input_line1.setText("")
        self.input_line1.resize(150, 30)
        self.input_line1.move(40, 130)

        self.lbl_error.setFixedWidth(800)
        self.lbl_error.move(200, 130)

        self.lbl_lin2.setText(FOLDER_LANGUAGE[13][self.lang_num])
        self.lbl_lin2.move(40, 160)
        self.lbl_lin2.setFixedWidth(200)
        self.input_line2.setText("")
        self.input_line2.resize(150, 30)
        self.input_line2.move(40, 190)

        self.btn_generate_random_pwd.move(200, 10)
        self.btn_generate_random_pwd.resize(200, self.btn_generate_random_pwd.height())
        self.btn_generate_random_pwd.setText(FOLDER_LANGUAGE[18][self.lang_num])
        self.btn_generate_random_pwd.clicked.connect(self.random_password)

        self.btn_choice_lang_new_pwd.move(10, 10)  # кнопка выборя языка
        self.btn_choice_lang_new_pwd.setText(FOLDER_LANGUAGE[2][self.lang_num])
        self.btn_choice_lang_new_pwd.clicked.connect(self.choice_lang_new_pwd)

        self.btn_conf_new_pwd.setText("Create")
        self.btn_conf_new_pwd.move(70, 240)
        self.btn_conf_new_pwd.clicked.connect(self.check_new_pwd)

    # установка номера языка
    def choice_lang_new_pwd(self):
        if self.btn_choice_lang_new_pwd.text() == "RUS":
            self.lang_num = 1
            self.btn_choice_lang_new_pwd.setText("ENG")
        else:
            self.btn_choice_lang_new_pwd.setText("RUS")
            self.lang_num = 2
        self.setting_lang_widgets_new_pwd()

    def setting_lang_widgets_new_pwd(self):
        self.btn_choice_lang_new_pwd.setText(FOLDER_LANGUAGE[2][self.lang_num])
        self.lbl_lin1.setText(FOLDER_LANGUAGE[12][self.lang_num])
        self.lbl_lin2.setText(FOLDER_LANGUAGE[13][self.lang_num])
        self.btn_generate_random_pwd.setText(FOLDER_LANGUAGE[18][self.lang_num])
        self.lbl1_new_pwd.setText(FOLDER_LANGUAGE[19][self.lang_num])
        self.lbl2_new_pwd.setText(FOLDER_LANGUAGE[20][self.lang_num])
        self.lbl_error.setText(FOLDER_LANGUAGE[21][self.lang_num])

    def check_new_pwd(self):
        s1 = self.input_line1.text()
        s2 = self.input_line2.text()
        f = self.check_good_pwd(s1, s2)
        if f == 1:
            for _ in self.lbl_lin1, self.lbl_lin2, self.input_line1, self.input_line2, \
                     self.btn_generate_random_pwd, self.btn_choice_lang_new_pwd, \
                     self.btn_conf_new_pwd, self.lbl1_new_pwd, self.lbl2_new_pwd, self.lbl_error:
                _.setEnabled(0)
                _.setVisible(0)
            for _ in self.btn_choice_lang, self.btn_rekey, self.btn_save, self.btn_add_new_pte, \
                     self.btn_del_last_pte, self.table:
                _.setVisible(1)
                _.setEnabled(1)
            self.pwd = self.input_line2.text()
            self.save_pwd()
            self.initUI_main()
        else:
            self.lbl_error.setText(f)

    # изменение размеров и положения виджетов при изменении окна
    def setting_resize_widgets(self):  # изменение размеров и положения виджетов при изменении окна
        self.table.resize(self.width() - 20, self.height() - 75)
        self.btn_add_new_pte.move(10, self.height() - 28)
        self.btn_del_last_pte.move(160, self.height() - 28)

    # функция без которой не работает изменение размеров виджетов
    def resizeEvent(self, event):
        self.resized.emit()
        return super(ManagerCreatWindow, self).resizeEvent(event)

    # загрузка полей из базы данных
    def load_inform(self):
        print(1)
        cur = sqlite3.connect("dinf.sqlite").cursor()
        self.data = cur.execute("""SELECT * FROM information""").fetchall()
        con.close()
        print(2)
        for i in range(len(self.data)):
            if self.data[i][0] == "":
                self.data[i] = ("None", self.data[i][1])
            if self.data[i][1] == "":
                self.data[i] = (self.data[i][0], "None")
            print(self.data[i][0])
            print(self.pwd)
            print(self.data[i][1])
            print(self.decrypt(self.data[i][0], self.pwd))
            print(self.decrypt(self.data[i][1], self.pwd))
            self.data[i] = (self.decrypt(self.data[i][0], self.pwd),
                            self.decrypt(self.data[i][1], self.pwd))
        print(4)

    # выгрузка данных из таблици в массив, для сохранения информации
    def load_table_in_data(self):
        data = []
        for i in range(len(self.data)):
            data.append((self.table.item(i, 0).text(), self.table.item(i, 1).text()))
        if self.data != data:
            self.bool_edit_data = True
        self.data = data

    # загрузка таблицы
    def load_table(self):
        self.table.setColumnCount(2)
        self.table.setRowCount(len(self.data))
        for i, row in enumerate(self.data):
            self.table.setRowCount(self.table.rowCount())
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table.resizeColumnsToContents()

    # первичная загрузка полей с данными
    def first_load_table(self):
        if len(self.data) == 0:
            self.data = [(FOLDER_LANGUAGE[4][self.lang_num], FOLDER_LANGUAGE[4][self.lang_num])]
        self.load_table()

    # функция добавления нового поля без данных
    def add_new_pte(self):
        self.bool_edit_data = True
        self.load_table_in_data()
        self.data.append(("", ""))
        self.load_table()

    # функция удаления последнего поля данных
    def del_past_pte(self):
        self.bool_edit_data = True
        self.load_table_in_data()
        self.data = self.data[:-1]
        self.load_table()

    # функция зашифровки
    def encode(self, h1, h2):  # информация, ключ
        a = "".join("{:02x}".format(ord(c)) for c in str(h1))
        b = "".join("{:02x}".format(ord(c)) for c in str(h2))
        nb = b
        while len(nb) < len(a):
            nb += b
        b = nb[:len(a)]
        return '%x' % (int(a, 16) ^ int(b, 16))

    # функция расшифровки
    def decrypt(self, h1, h2):  # информация, ключ
        a = str(h1)
        b = "".join("{:02x}".format(ord(c)) for c in str(h2))
        nb = b
        while len(nb) < len(a):
            nb += b
        b = nb[:len(a)]
        d = int(a, 16) ^ int(b, 16)
        print(d)
        d = hex(d).split('x')[-1]
        print(d)
        d = bytearray.fromhex(d).decode()
        print(d)
        return d

    # сохранение пароля
    def save_pwd(self):
        con = sqlite3.connect("language.sqlite")  # удаление из базы данных старой информации
        cur = con.cursor()
        cur.execute("""DELETE FROM pwd""")
        con.commit()
        con = sqlite3.connect("language.sqlite")  # загрузка в базу данных новой информации
        cur = con.cursor()
        cur.executemany("INSERT INTO pwd VALUES(?);", self.encode("de", self.pwd))
        con.commit()

    # сохранение данных
    def save_data(self):
        self.load_table_in_data()
        con = sqlite3.connect("dinf.sqlite")  # удаление из базы данных старой информации
        cur = con.cursor()
        cur.execute("""DELETE FROM information""")
        con.commit()
        for i in range(len(self.data)):
            if self.data[i][0] == "":
                self.data[i] = ("None", self.data[i][1])
            if self.data[i][1] == "":
                self.data[i] = (self.data[i][0], "None")
            self.data[i] = (self.encode(self.data[i][0], self.pwd),
                            self.encode(self.data[i][1], self.pwd))
        con = sqlite3.connect("dinf.sqlite")  # загрузка в базу данных новой информации
        cur = con.cursor()
        cur.executemany("INSERT INTO information VALUES(?, ?);", self.data)
        con.commit()

        con = sqlite3.connect("language.sqlite")  # удаление из базы данных старой информации
        cur = con.cursor()
        cur.execute("""DELETE FROM set_language""")
        con.commit()
        con = sqlite3.connect("language.sqlite")  # загрузка в базу данных новой информации
        cur = con.cursor()
        language = ""
        if self.lang_num == 2:
            language = "set_rus"
        else:
            language = "set_eng"
        cur.execute("INSERT INTO set_language VALUES(?)", [language])
        con.commit()
        self.bool_edit_data = False

    # диалоговое окно
    def save(self):
        answer = QMessageBox.question(self, FOLDER_LANGUAGE[8][self.lang_num],
                                      FOLDER_LANGUAGE[6][self.lang_num],
                                      QMessageBox.Save | QMessageBox.Cancel)

        if answer == QMessageBox.Save:
            d = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П",
                 "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я", "а",
                 "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р",
                 "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
            not_vst = True
            data = []
            for i in range(len(self.data)):
                data.append((self.table.item(i, 0).text(), self.table.item(i, 1).text()))
            for i in range(len(data)):
                for b in data[i][0]:
                    if b in d:
                        not_vst = False
                        break
                for b in data[i][1]:
                    if b in d:
                        not_vst = False
                        break

            if not_vst:
                self.save_data()
            else:
                self.dont_save()

    # диалоговое окно
    def closeEvent(self, event):
        if self.bool_edit_data:
            close = QMessageBox.question(self, FOLDER_LANGUAGE[7][self.lang_num],
                                         FOLDER_LANGUAGE[6][self.lang_num],
                                         QMessageBox.Save | QMessageBox.Cancel)
            if close == QMessageBox.Save:
                d = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О",
                     "П",
                     "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я",
                     "а",
                     "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п",
                     "р",
                     "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
                not_vst = True
                data = []
                for i in range(len(self.data)):
                    data.append((self.table.item(i, 0).text(), self.table.item(i, 1).text()))
                for i in range(len(data)):
                    for b in data[i][0]:
                        if b in d:
                            not_vst = False
                            break
                    for b in data[i][1]:
                        if b in d:
                            not_vst = False
                            break

                if not_vst:
                    self.save_data()
                    event.accept()
                else:
                    self.dont_save()
            else:
                event.accept()

    def dont_save(self):
        answer = QMessageBox.question(self, FOLDER_LANGUAGE[25][self.lang_num],
                                      FOLDER_LANGUAGE[26][self.lang_num],
                                      QMessageBox.Ok | QMessageBox.Cancel)
        if QMessageBox.Ok:
            pass

    def random_password(self):
        p = ""
        b = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
             "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H",
             "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
             "Z", "_", ".", ",", "(", ")", "-", "+", "0", "1", "2", "3", "4", "5", "6", "7", "8",
             "9"]
        while True:
            p = ""
            for _ in range(random.randint(8, 14)):
                p += b[random.randint(0, 69)]
            if self.check_good_pwd(p, p) == 1:
                print(p)
                self.input_line1.setText(p)
                break

    def check_good_pwd(self, s1, s2):
        number = alpha_smale = alpha_big = simbol = False
        b = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
             "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H",
             "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
             "Z", "_", ".", ",", "(", ")", "-", "+", "0", "1", "2", "3", "4", "5", "6", "7", "8",
             "9"]
        for i in range(len(s1)):
            if not (s1[i].isalnum()):
                simbol = True
            if s1[i].isalpha() and s1[i].islower():
                alpha_smale = True
            if s1[i].isalpha() and s1[i].isupper():
                alpha_big = True
            if s1[i].isdigit():
                number = True
            if s1[i] not in b:
                return FOLDER_LANGUAGE[25][self.lang_num]
        if not (number and alpha_smale and alpha_big and simbol):
            return FOLDER_LANGUAGE[24][self.lang_num]
        if len(s1) < 8:
            return FOLDER_LANGUAGE[23][self.lang_num]
        if s1 != s2:
            return FOLDER_LANGUAGE[22][self.lang_num]
        return 1


if __name__ == '__main__':
    con = sqlite3.connect("language.sqlite")
    cur1 = con.cursor()
    result = cur1.execute("""SELECT * FROM words_translate""").fetchall()
    cur2 = con.cursor()
    set_lang = cur2.execute("""SELECT * FROM set_language""").fetchall()
    con.close()
    set_lang = list(*set_lang)[0]
    if set_lang == "set_rus":
        LANG_NUM = 2
    else:
        LANG_NUM = 1
    FOLDER_LANGUAGE = [list(_) for _ in result]

    app = QApplication(sys.argv)
    ex = ManagerCreatWindow()
    ex.show()
    sys.exit(app.exec())
