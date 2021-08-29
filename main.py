import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainGUI import Ui_MainWindow


# 创建一个窗体函数
def GUISHOW():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # 使用多线程
    t1 = threading.Thread(target=GUISHOW)
    t1.start()
    # 如果不使用多线程，则主程序会卡住，而且textBrower会等下载函数执行完后才会显示文本
