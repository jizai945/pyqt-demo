import sys
from PyQt5.Qt import *


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('使用插值')
        self.resize(500, 500)
        self.move(400, 200)
        self.btn = QPushButton(self)
        self.init_ui()

    def init_ui(self):
        self.btn.resize(50, 50)
        self.btn.move(0, 0)
        self.btn.setStyleSheet('QPushButton{border: none; background: pink;}')
        
        # 1.创建动画
        animation = QPropertyAnimation(self.btn, b'pos', self)
        
        # 2.定义动画插值
        animation.setKeyValueAt(0, QPoint(0, 0))
        animation.setKeyValueAt(0.25, QPoint(450, 0))
        animation.setKeyValueAt(0.5, QPoint(450, 450))
        animation.setKeyValueAt(0.75, QPoint(0, 450))
        animation.setKeyValueAt(1, QPoint(0, 0))
        # 3.动画时长
        animation.setDuration(5000)
        # 4.启动动画
        animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
