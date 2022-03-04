import unittest, pytest
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from PySide6 import QtWidgets
from trabajoIntegrado import AnotherWindow
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalTableModel
db = QSqlDatabase("QSQLITE")
db.setDatabaseName("chinook.sqlite")
db.open()
class introducirDatos (QMainWindow):
    def add(self):
        app=QApplication.instance()
        if app==None:
            app= QApplication([])
        
        window=AnotherWindow()
        nuevaFila = window.modelo.rowCount()
        while(nuevaFila<=550):
            window.modelo.insertRow(nuevaFila)
            window.tabla.selectRow(nuevaFila)
            window.modelo.setData(window.modelo.index(nuevaFila, 0), "José")
            window.modelo.setData(window.modelo.index(nuevaFila, 1), "Fácil")
            window.modelo.setData(window.modelo.index(nuevaFila, 2), "2")
            window.modelo.setData(window.modelo.index(nuevaFila, 3), "2:10:20")
            window.modelo.setData(window.modelo.index(nuevaFila, 4), "21")
            nuevaFila= nuevaFila+1
            print(window.fila)
            window.modelo.submit()

    
class QMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        introducirDatos(self).add()
app = QtWidgets.QApplication([])
w = QMainWindow()
w.show()
app.exec()