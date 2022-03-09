import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class FloatBtn(QPushButton):
    def __init__(self, title='', parent=None, icon=''):
        super().__init__(title, parent)
        # self.parent = parent
        self.isMove = False
        self.m_start = 0
        self.m_end = 0
        self.m_leftButtonPressed = False

        self.setWindowFlag(Qt.WindowStaysOnTopHint);

        self.resize(32, 32)

        self.setStyleSheet("background:transparent");
        self.setIcon(QIcon(icon));
        self.setIconSize(QSize(32, 32))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isMove = False
            self.m_leftButtonPressed = True
            self.m_start = event.globalPos()
        elif event.button() == Qt.RightButton:
            self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.isMove:
                self.released.emit()
            self.m_leftButtonPressed = False
            self.isMove = False

    def mouseMoveEvent(self, event):
        if self.m_leftButtonPressed:
            size = self.size() # 当前窗口大小
            parentSize = self.parentWidget().size() # 父窗口大小
            curPos = self.geometry().topLeft() + (event.globalPos() - self.m_start) # 移动后的位置
            if(curPos.x() < 0): # left
                curPos.setX(0)

            if(curPos.y() < 0):  # top
                curPos.setY(0)

            if( (curPos.x()+size.width()) > parentSize.width()): # right
                curPos.setX(parentSize.width() - size.width());

            if( (curPos.y()+size.height()) > parentSize.height()): # bottom
                curPos.setY(parentSize.height() - size.height())

            self.move(curPos) # 移动
            self.isMove = True
            # 将鼠标在屏幕中的位置替换为新的位置
            self.m_start = event.globalPos()

class Demo(QMainWindow):
    def __init__(self,parent=None):
        super(Demo, self).__init__(parent)

        bar=self.menuBar()
        btn = FloatBtn(self, icon="./acc.png")
        # btn.clicked.connect(lambda: print('right clicked')) # 只有右键按下才能触发
        btn.released.connect(lambda: print('released')) # 左击并释放
        btn.setContextMenuPolicy(Qt.CustomContextMenu)  # 打开右键菜单的策略
        btn.customContextMenuRequested.connect(self.btnItemFun)  # 绑定事件
        btn.setGeometry(self.width()/2, self.height()/2, btn.width(), btn.height())

        # self.setFixedSize(600, 600)
        self.resize(600, 600)
        self.setWindowTitle('悬浮按钮例程')

    def btnItemFun(self, pos):
        popMenu = QMenu()
        popMenu.setStyleSheet("QMenu {border-radius:5px;font-family:'Arial';color:white;background-color:rgb(40, 44, 52)}"
                                " QMenu::item {height:35px; width:120px;padding-left:25px;border: 1px solid none;}"
                                "QMenu::item:selected {background-color:rgb(189, 147, 249);\
                                padding-left:25px;border: 1px solid rgb(65,173,255);}")
        popMenu.addAction(QAction(u'选项1', self))
        popMenu.addAction(QAction(u'选项2', self))
        popMenu.triggered[QAction].connect(self.processtrigger)
        popMenu.exec_(QCursor.pos())

    def processtrigger(self, q):
        print(q.text())

if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=Demo()
    demo.show()
    sys.exit(app.exec_())