import sys
sys.path.append('/usr/local/lib/python3.5/site-packages/')
from PyQt4.QtCore import  *
from PyQt4.QtGui import  *
import sqlite3
import configparser
import shift_edit

def get_days(day = 0):
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    if day == 0:
        cur.execute("""SELECT month,day FROM day_data;""")
        a = cur.fetchall()
        conn.commit()
        conn.close()
    return a

def get_mems():
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT name,workcnt,worktime FROM mem_data;""")
    a = cur.fetchall()
    for i in range(len(a)):
        a[i] = "{0}:{1}回:{2}h".format(a[i][0],a[i][1],a[i][2])
    conn.commit()
    conn.close()
    return a

def get_workmem():
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT name1,name2,name3 FROM day_data;""")
    a = cur.fetchall()
    conn.commit()
    conn.close()
    return a


def get_req():
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT id,req FROM req_data;""")
    a = cur.fetchall()
    conn.commit()
    conn.close()
    return a


def coloring_holiday(table):
    conn = sqlite3.connect('./day_data.db')
    cur = conn.cursor()
    cur.execute("""SELECT isholi,ispreholi FROM day_data;""")
    a = cur.fetchall()
    for j in range(table.columnCount()):
        if a[j][0] == 1:
            for i in range(table.rowCount()):
                if table.item(i,j) == None:
                    table.setItem(i,j,QTableWidgetItem())
                table.item(i,j).setBackground(QColor("pink"))

def table_connect(table):
    table.cellWidget(1,1).currentIndexChanged.connect(lambda:print("changed",1,1,"cell"))
    table.cellWidget(2,2).currentIndexChanged.connect(lambda:print("changed",2,2,"cell"))
    table.cellWidget(3,3).currentIndexChanged.connect(lambda:print("changed",3,3,"cell"))
    table.cellWidget(4,4).currentIndexChanged.connect(lambda:print("changed",4,4,"cell"))
    table.cellWidget(5,5).currentIndexChanged.connect(lambda:print("changed",5,5,"cell"))


'''class ApplyButton(QWidget):

    emit_list = pyqtSignal(object)

    def __init__(self,parent=None):
        QWidget.__init__(self,parent=parent)
        self.interval = 10
        self.setup_ui()

    def slot1(self):
        self.emit_list.emit(get_table())

    def slot2(self,arg):
        print("arg",arg)

    def setup_ui(self):
        self.apply_button = QPushButton("Apply",self)
        layout = QVBoxLayout()
        layout.addWidget(self.apply_button)
        self.setLayout(layout)

        self.apply_button.clicked.connect(self.slot1)
        self.emit_list.connect(self.slot2)

'''


def main():
    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_window.setWindowTitle("Main Table")

    table = QTableWidget()
    tableItem = QTableWidgetItem()

    table.setWindowTitle("Shift Table")

    days = ["{0}/{1}".format(a,b) for (a,b) in get_days() ]
    table.setColumnCount(len(days))
    mem = get_mems()
    table.setRowCount(len(mem))


    table.setVerticalHeaderLabels(mem);
    table.setHorizontalHeaderLabels(days);

    workmem = get_workmem()
    for i in range(len(days)):
        for j in range(len(mem)):
            combo = QComboBox()
            combo.addItem("")
            combo.addItem("X")
            combo.addItem("O")
            combo.addItem("{0}-{1}".format(i,j))
            table.setCellWidget(j,i,combo)
            table.cellWidget(j,i).setMaxVisibleItems(2)
            table.cellWidget(j,i).currentIndexChanged.connect(lambda:print("changed","cell"))
            if workmem[i][0] == (j+1) or workmem[i][1] == (j+1) or workmem[i][2] == (j+1) :
                table.cellWidget(j,i).setCurrentIndex(2)


    req = get_req()
    for j in range(len(mem)):
        req_day = req[j][1].split(",")
        if req_day[0] != '' :
            for i in range(len(req_day)):
                table.cellWidget(j,i).setCurrentIndex(1)
        req_day = 0

    #table_connect(table)

    table.horizontalHeader().setDefaultSectionSize(50)
    coloring_holiday(table)


    quit_button = QPushButton("QUIT")
    quit_button.clicked.connect(app.quit)
    apply_button = QPushButton("Apply")

    # apply_button.apply_button.clicked.connect(apply_button.apply_change(table))

    apply_button.clicked.connect(emit(table))
    #apply_button = ApplyButton()


    panel = QWidget()
    panel_layout = QVBoxLayout()
    panel_layout.addWidget(table)
    button_box = QWidget()
    button_layout = QGridLayout()
    button_layout.addWidget(quit_button,0,0)
    button_layout.addWidget(apply_button,0,1)
    button_box.setLayout(button_layout)
    panel_layout.addWidget(button_box)
    panel.setLayout(panel_layout)


    main_window.setCentralWidget(panel)
    main_window.resize(1200,800)
    main_window.show()

    app.exec_()

if __name__ == '__main__':
    main()
