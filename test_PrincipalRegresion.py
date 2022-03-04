import unittest, pytest
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QWidget
from trabajoIntegrado import MainWindow
class test(unittest.TestCase):
    def test_texto1(self):
        app=QApplication.instance()
        if app==None:
            app= QApplication([])

        app = MainWindow()
        self.assertEqual(app.button1.text(), 'Jugar')
    def test_texto2(self):
        app=QApplication.instance()
        if app==None:
            app= QApplication([])

        app = MainWindow()
        self.assertEqual(app.button2.text(), 'Estadísticas')
    def test_texto3(self):
        app=QApplication.instance()
        if app==None:
            app= QApplication([])

        app = MainWindow()
        self.assertEqual(app.button3.text(), 'Salir')
if __name__ == '__main__':
    unittest.main()