import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                            QTabWidget, QAbstractScrollArea,
                            QVBoxLayout, QHBoxLayout,
                            QTableWidget, QGroupBox,
                            QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._connect_to_db()
        self.setWindowTitle("MyDataBase")
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self._create_tabs()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="lab8_db",
                                     user="postgres",
                                     password="2323",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_tabs(self):
        self.cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
        list_tables = list(self.cursor.fetchall())
        for table in list_tables:
            self._create_tab(table[0])

    def _create_tab(self, name_table):
        shedule_tab = QWidget()
        table = QTableWidget()
        self.tabs.addTab(shedule_tab, name_table)
        svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        shbox2 = QHBoxLayout()
        svbox.addLayout(self.shbox1)
        svbox.addLayout(shbox2)
        self._create_table(name_table, table)
        update_shedule_button = QPushButton("Update")
        shbox2.addWidget(update_shedule_button)
        update_shedule_button.clicked.connect(lambda ch, nt=name_table, tb=table: self._update_table(nt, tb))
        shedule_tab.setLayout(svbox)

    def _create_table(self, name_table,table):
        self.cursor.execute(
            f"select column_name from information_schema.columns where information_schema.columns.table_name='{name_table}'")
        table_list_names = list(self.cursor.fetchall())
        # print(table_list_names)
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table.setColumnCount(len(table_list_names)+2)
        table.setHorizontalHeaderLabels([table_list_names[i][0] for i in range(0, len(table_list_names))]+["Изменить\n/Добавить","Удалить"])
        self._update_table(name_table, table)
        mvbox = QVBoxLayout()
        mvbox.addWidget(table)
        self.shbox1.addLayout(mvbox)

    def _update_table(self, name_table, table):

        self.cursor.execute(
            f"SELECT * FROM {name_table}")
        table_content = list(self.cursor.fetchall())
        # print(table_content)
        table.setRowCount(len(table_content)+1)
        for i, r in enumerate(table_content):
            r = list(r)
            # print(i, r)
            for j in range(len(r)):
                table.setItem(i, j, QTableWidgetItem(str(r[j])))

            editButton = QPushButton("Edit")
            table.setCellWidget(i, len(r), editButton)
            editButton.clicked.connect(
                lambda ch, num=i, nt=name_table, tb=table: self._edit_row_from_table(num, nt, tb))

            deleteButton = QPushButton("Delete")
            table.setCellWidget(i, len(r)+1, deleteButton)
            deleteButton.clicked.connect(lambda ch, num=i, nt=name_table, tb=table: self._delete_row_from_table(num, nt, tb))


        joinButton = QPushButton("Join")
        for j in range(len(table_content[0])):
            table.setItem(len(table_content), j, QTableWidgetItem(""))
        table.setCellWidget(len(table_content), len(table_content[0]), joinButton)
        joinButton.clicked.connect(lambda ch, num=len(table_content), nt=name_table, tb=table: self._join_row_to_table(num, nt, tb))
        table.resizeRowsToContents()

    def _delete_row_from_table(self, num, name_table, table):
        # print(table.item(num, 0).text())
        try:
            self.cursor.execute(f"DELETE FROM {name_table} WHERE id='{str(table.item(num, 0).text())}';")
            self.conn.commit()
        except Exception as e:
            print(e)
        self._update_table(name_table, table)

    def _edit_row_from_table(self, num, name_table, table):
        # print(table.item(num, 0).text())
        self.cursor.execute(
            f"select column_name from information_schema.columns where information_schema.columns.table_name='{name_table}'")
        table_list_names = list(self.cursor.fetchall())
        try:
            for n in range(1, len(table_list_names)):
                self.cursor.execute(f"UPDATE {name_table} SET {table_list_names[n][0]}='{str(table.item(num, n).text())}' WHERE id='{str(table.item(num, 0).text())}'")
                # print(f"UPDATE {name_table} SET {table_list_names[n][0]}='{str(table.item(num, n).text())}' WHERE id='{str(table.item(num, 0).text())}'")
            self.conn.commit()
        except Exception as e:
            print(e)
        self._update_table(name_table, table)

    def _join_row_to_table(self, num, name_table, table):
        self.cursor.execute(
            f"select column_name from information_schema.columns where information_schema.columns.table_name='{name_table}'")
        table_list_names = list(self.cursor.fetchall())
        s=""
        for i in range(1,len(table_list_names)):
            s+=table_list_names[i][0]+", "
        # print([table_list_names[i][0] for i in range(len(table_list_names))])
        # print(s[:-2])
        j=""
        for i in range(1,len(table_list_names)):
            j+="'"+str(table.item(num, i).text())+"'"+", "
        # print(j[:-2])
        try:
            self.cursor.execute(f"INSERT INTO {name_table}({s[:-2]}) VALUES({j[:-2]});")
            self.conn.commit()
        except Exception as e:
            print(e)
        self._update_table(name_table, table)



app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
