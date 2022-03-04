import unittest, pytest
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QWidget
from componente import componente
class TestComponente(unittest.TestCase):
    def test_sizeHint(self):
        app = QApplication([])
        result = componente().sizeHint()
        self.assertEqual(result, QSize(100, 124))


@pytest.fixture
def app(qtbot):
    test_componente = componente()
    qtbot.addWidget(test_componente)

    return test_componente


def test_color1(app):
    assert app.getColor1() == QtGui.QColor("#E9EBEF")
def test_color2(app):
    assert app.getColor2() == QtGui.QColor("#0000FF")
def test_color_after_click(app, qtbot):
    qtbot.mouseClick(app, QtCore.Qt.LeftButton)
    assert app.getBottomColor() == "#E9EBEF" or "#0000FF"
if __name__ == '__main__':
    unittest.main()