from PySide6 import QtWidgets
from componente import componente

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        mainToggle = componente()
        self.setCentralWidget(mainToggle)

app = QtWidgets.QApplication([])
w = Window()
w.show()
app.exec()