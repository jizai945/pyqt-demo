import sys
from PyQt5.Qt import *


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('动画组')
        self.resize(500, 500)
        self.move(400, 200)
        self.btn1 = QPushButton(self)
        self.btn2 = QPushButton(self)
        self.init_ui()

    def init_ui(self):
        self.btn1.resize(50, 50)
        self.btn1.move(0, 0)
        self.btn1.setStyleSheet('QPushButton{border: none; background: pink;}')

        self.btn2.resize(50, 50)
        self.btn2.move(50, 50)
        self.btn2.setStyleSheet('border: none; background: cyan')

        # 按钮1的动画
        animation1 = QPropertyAnimation(self.btn1, b'pos', self)
        animation1.setKeyValueAt(0, QPoint(0, 0))
        animation1.setKeyValueAt(0.25, QPoint(450, 0))
        animation1.setKeyValueAt(0.5, QPoint(450, 450))
        animation1.setKeyValueAt(0.75, QPoint(0, 450))
        animation1.setKeyValueAt(1, QPoint(0, 0))
        animation1.setDuration(5000)
        # animation1.start()

        # 按钮2的动画
        animation2 = QPropertyAnimation(self.btn2, b'pos', self)
        animation2.setKeyValueAt(0, QPoint(50, 50))
        animation2.setKeyValueAt(0.25, QPoint(400, 50))
        animation2.setKeyValueAt(0.5, QPoint(400, 400))
        animation2.setKeyValueAt(0.75, QPoint(50, 400))
        animation2.setKeyValueAt(1, QPoint(50, 50))
        animation2.setDuration(3000)
        # animation2.start()

        animation_group = QSequentialAnimationGroup(self)
        animation_group.addAnimation(animation1)
        animation_group.addAnimation(animation2)
        animation_group.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
