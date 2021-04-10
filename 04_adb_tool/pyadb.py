import os
import sys
import time
import datetime
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyadb_ui import Ui_Form
import subprocess, datetime, os, time, signal  

def adb_shell(cmd):
    result = subprocess.getstatusoutput(cmd)
    return result

class Pyqt5_adb(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(Pyqt5_adb, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("pudu adb file tool")
        self.ip_0.setValidator(QIntValidator(0, 255))
        self.ip_1.setValidator(QIntValidator(0, 255))
        self.ip_2.setValidator(QIntValidator(0, 255))
        self.ip_3.setValidator(QIntValidator(0, 255))
        self.con_stat.setStyleSheet("color:red")
        # 表格模型绑定
        self.model = QStandardItemModel(0,2)
        self.model.setHorizontalHeaderLabels(['文件名', '操作'])
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #所有列自动拉伸，充满界面
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents) # 自适应宽度
        # self.tableView.setColumnWidth(0, 200)    
        # self.tableView.setColumnWidth(1, 200) 
        # 设置被选中时的颜色
        self.tableView.setStyleSheet("selection-background-color:lightblue;")
        result = adb_shell(r'.\adb devices -l')
        print(result[1])
        new_str = result[1][len('List of devices attached\n'):]
        print(new_str)
        if new_str == '':
            self.con_stat.setText('未连接')
        else:
            self.con_stat.setText('已连接的设备:\n'+new_str)
            self.con_stat.setStyleSheet("color:green")

        self.ip = None
        self.init()

    def init(self):
        # 网络连接按钮
        self.ip_con_btn.clicked.connect(self.start_ip_con)
        # usb连接
        self.usb_con_btn.clicked.connect(self.start_usb_con)
        # 刷新文件
        self.fresh_btn.clicked.connect(self.fresh_file_func)
        # 上传固件按钮
        self.chose_btn.clicked.connect(self.openFileDialog)

    # ip连接按钮点击事件
    def start_ip_con(self):
        if self.ip_con_btn.text() == '开始连接':
            if self.ip_0.text()=='' or self.ip_1.text()=='' or self.ip_2.text()=='' or self.ip_3.text()=='':
                QMessageBox.warning(self, "警告", "IP错误")
                return
            con_ip = self.ip_0.text() +'.'+self.ip_1.text()+'.'+self.ip_2.text()+'.'+self.ip_3.text()
            print(con_ip)

            self.ip_con_btn.setEnabled(False)
            self.ip_con_btn.setText('连接中...')
            QtWidgets.QApplication.processEvents()    # 实时刷新
            try:
                res = adb_shell(r'.\adb connect '+con_ip)
                if not res[0]:
                    self.con_stat.setText('已连接')
                    self.ip = con_ip
                    self.con_stat.setStyleSheet("color:blue")
                    self.ip_con_btn.setEnabled(True)
                    self.ip_con_btn.setText('关闭连接')
                    self.fresh_file_func()
                else:
                    QMessageBox.warning(self, "失败", "连接失败")
                    self.ip = None
                    self.con_stat.setText('连接失败')
                    self.con_stat.setStyleSheet("color:red")
                    self.ip_con_btn.setEnabled(True)
                    self.ip_con_btn.setText('开始连接')
            except:
                QMessageBox.warning(self, "失败", "连接失败")
                self.ip = None
                self.con_stat.setText('连接失败')
                self.con_stat.setStyleSheet("color:red")
                self.ip_con_btn.setEnabled(True)
                self.ip_con_btn.setText('开始连接')
        else:
            self.ip = None
            print('start stop con')
            self.ip_con_btn.setEnabled(False)
            self.ip_con_btn.setText('断开中...')
            res = adb_shell(r'.\adb disconnect')
            if not res[0]:
                self.con_stat.setText('已断开')
                self.con_stat.setStyleSheet("color:red")
                self.ip_con_btn.setEnabled(True)
                self.ip_con_btn.setText('开始连接')
            else:
                QMessageBox.warning(self, "失败", "断开失败")
        
    def start_usb_con(self):
        result = adb_shell(r'.\adb disconnect')
        print(result[0])
        result = adb_shell(r'.\adb get-state')
        print(result[0])
        if not result[0]:
            self.con_stat.setText('已连接')
            self.con_stat.setStyleSheet("color:blue")
            self.fresh_file_func()
        else:
            self.con_stat.setText('连接失败')
            self.con_stat.setStyleSheet("color:red")

    def cellButtonClicked(self):
        print("Cell Button Clicked", self.sender().property('id'))   
        print("remove ", self.sender().property('file'))

        res = adb_shell(r'.\adb shell rm -rf sdcard/pudu/test_mcu_bin/'+self.sender().property('file'))
        if not res[0]:
            self.con_stat.setText('删除成功')
            self.con_stat.setStyleSheet("color:green")
            self.fresh_file_func()
        else:
            self.con_stat.setText('删除失败')
            self.con_stat.setStyleSheet("color:red")
        
    # 刷新
    def fresh_file_func(self):
        # if self.ip == None:
        #     QMessageBox.warning(self, "失败", "未连接")
        #     return
        res = adb_shell(r'.\adb shell ls '+self.file_path_label.text())
        print(res)
        if not res[0]:
            long_str = res[1]  
            self.con_stat.setText('查询成功')
            self.con_stat.setStyleSheet("color:green")
            strlist = long_str.splitlines(False)	
            self.table_append_file(strlist)
        else:
            self.con_stat.setText('查询失败')
            self.con_stat.setStyleSheet("color:red")
            self.table_append_file([])

    def table_append_file(self, file_list):
        self.model.removeRows(0, self.model.rowCount())
        now_time = datetime.datetime.now()
        self.model.appendRow([QStandardItem('查询时间:  '+str(now_time))])
        for i in range(1, len(file_list)+1):
            button_read = QPushButton(
                self.tr('删除'),
                self.parent(),
                clicked=self.cellButtonClicked
            )
            button_read.setProperty('id', i)
            button_read.setProperty('file', file_list[i-1])

            self.model.appendRow([ QStandardItem(file_list[i-1])])
            self.tableView.setIndexWidget(self.model.index(self.model.rowCount()-1, 1), button_read)

    # 选择文件弹窗
    def openFileDialog(self):
        # 生成文件对话框对象
        dialog = QFileDialog()
        # 设置文件过滤器，这里是任何文件，包括目录噢
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            up_file = fileNames[0]
        else:
            return

        print(up_file)
        (filepath,tempfilename) = os.path.split(up_file)
        # (filename,extension) = os.path.splitext(up_file)
        self.up_flie_label.setText(tempfilename)
        self.chose_btn.setEnabled(False)
        self.chose_btn.setText('上传中...')
        QtWidgets.QApplication.processEvents()    # 实时刷新
        result = adb_shell(r'.\adb shell mkdir -p '+self.file_path_label.text())
        print(result[0])
        try:
            result = adb_shell(r'.\adb push '+up_file+' '+self.file_path_label.text()+'/'+tempfilename)
            print(result[0])
        except:
            # 处理中文路径会崩溃的问题
            result = [0]
            print('gbk bug')
        self.chose_btn.setEnabled(True)
        self.chose_btn.setText('选择上传')
        if not result[0]:
            self.con_stat.setText('上传成功')
            self.con_stat.setStyleSheet("color:green")
            self.fresh_file_func()
        else:
            self.con_stat.setText('上传失败')
            self.con_stat.setStyleSheet("color:red")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    try :
        myshow = Pyqt5_adb()
        myshow.show()
        sys.exit(app.exec_())
    except Exception as e:
        app.quit()
        msg_box = QMessageBox(QMessageBox.Critical, 'error', str(e))
        app.exit(msg_box.exec_())
        app.exec_()