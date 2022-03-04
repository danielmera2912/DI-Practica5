from PySide6 import QtWidgets
from trabajo import MainWindow

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        mainToggle = MainWindow()
        self.setCentralWidget(mainToggle)

app = QtWidgets.QApplication([])
w = Window()
w.show()
app.exec()