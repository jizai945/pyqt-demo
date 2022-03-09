import sys
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('动画组')
        self.resize(500, 500)
        self.move(400, 200)
        self.btn1 = QPushButton('点击',self)
        self.btn1.installEventFilter(self)
        self.init_ui()

    def eventFilter(self, object, event):
        if object == self.btn1:
            if event.type() == QEvent.Enter:
                print('enter')
                self.dialog_preview( 0, '设置地址对非hex文件有效' )
            
                return True
            elif event.type() == QEvent.Leave:
                print('leave')
                self.dialog_preview( 1, '设置地址对非hex文件有效' )

        return False

    def init_ui(self):
        self.btn1.resize(50, 50)
        self.btn1.move(0, 0)
        self.btn1.setStyleSheet('QPushButton{border: none; background: pink;}')

        animation1 = QPropertyAnimation(self.btn1, b"geometry", self)

        # 设置状态机
        machine = QStateMachine(self)

        # 设置状态
        startState = QState(machine)
        endState = QState(machine)

        # 设置动作
        startState.assignProperty(self.btn1, "geometry", QRect(0, 50, 50, 50))
        endState.assignProperty(self.btn1, "geometry", QRect(100, 100, 300, 300))

        # 初始化状态
        machine.setInitialState(startState);

        # 单次切换
        transition1 = startState.addTransition(self.btn1.clicked, endState)
        transition2 = endState.addTransition(self.btn1.clicked, startState)
        # 添加动作
        transition1.addAnimation(animation1)
        transition2.addAnimation(animation1)

        # 启动状态机 只需启动一次
        machine.start()
       
    def dialog_preview(self, state:int, info:str):
        
        try:
            self.preview_dialog.close()
            self.preview_dialog.deleteLater()
        except:
            pass

        # 判断坐标让弹窗不挡住鼠标
        x = QCursor.pos().x()
        y = QCursor.pos().y()
        # print(f'x:{x} y:{y}')
        width = 200
        heigh = 80
        dialog_x = x+30
        dialog_y = y+100

        if state == 0:
            self.preview_dialog = QDialog(self)
            self.preview_dialog.setWindowTitle('提示')
            flags = self.preview_dialog.windowFlags()
            self.preview_dialog.setWindowFlags(flags & ~Qt.WindowContextHelpButtonHint & ~Qt.WindowCloseButtonHint)  # 去除问号按钮
            # self.preview_dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
            pre_lb = QLabel(info)

            v_box_layout = QVBoxLayout(self.preview_dialog) 
            v_box_layout.addWidget(pre_lb)
            self.preview_dialog.setGeometry(dialog_x, dialog_y, width, heigh)
            self.preview_dialog.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
