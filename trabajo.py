from datetime import datetime
from pathlib import Path
import random
import sys, os
import textwrap
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QComboBox, QMainWindow, QPushButton, QWizard, QWizardPage, QLineEdit, QHBoxLayout, QLabel, QWidget, QAbstractItemView, QVBoxLayout, QMessageBox, QFormLayout, QTextEdit, QSpinBox
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelation, QSqlRelationalTableModel
from design import Ui_MainWindow
import pyqtgraph as pg
import pyqtgraph.exporters

# La aplicación consistiría en pulsar a jugar y se elige el juego que se desea jugar,
#  saltaría la pantalla del juego y al acabar, salta el asistente para registrar tu puntuación en un informe
# en estadísticas se guarda las estadísticas locales en una base de datos, y el botón salir sale

db = QSqlDatabase("QSQLITE")
db.setDatabaseName("chinook.sqlite")

db.open()
class AnotherWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setupUi(self)
        self.modelo = QSqlRelationalTableModel(db=db)
        self.modelo.setTable("estadisticas")
        self.modelo.select()
        self.modelo.setHeaderData(0, Qt.Horizontal, "nombre")
        self.modelo.setHeaderData(1, Qt.Horizontal, "dificultad")
        self.modelo.setHeaderData(2, Qt.Horizontal, "score")
        self.modelo.setHeaderData(3, Qt.Horizontal, "tiempo")
        self.modelo.setHeaderData(4, Qt.Horizontal, "juego")
        self.tabla.setModel(self.modelo)
        self.tabla.resizeColumnsToContents()
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.selectionModel().selectionChanged.connect(self.seleccion)
        self.actionModificar.triggered.connect(self.modificar)
        self.actionInsertar.triggered.connect(self.nueva)
        self.actionEliminar.triggered.connect(self.borrar)
        self.fila = -1




        self.setLayout(layout)
    def seleccion(self, seleccion):
    # Recuerda que indexes almacena los índices de la selección
        if seleccion.indexes():
            # Nos quedamos con la fila del primer índice (solo se puede seleccionar una fila)
            self.fila = seleccion.indexes()[0].row()
            # Obtenemos los valores del modelo en esa fila
            nombre = self.modelo.index(self.fila, 0).data()
            dificultad = self.modelo.index(self.fila, 1).data()
            score = self.modelo.index(self.fila, 2).data()
            tiempo = self.modelo.index(self.fila, 3).data()
            juego = self.modelo.index(self.fila, 4).data()
            # Modificamos los campos del formulario para establecer esos valores
            self.nombreText.setText(str(nombre))
            self.dificultadText.setText(str(dificultad))
            self.scoreText.setText(str(score))
            self.tiempoText.setText(str(tiempo))
            self.juegoText.setText(str(juego))
        else:
            # Si no hay selección,  ponemos la fila inicial a un valor que indica que no está seleccionada ninguna fila
            self.fila = -1

    def modificar(self):
        # Si es una fila válida la seleccionada
        if self.fila >= 0:
            # Obtenemos los valores de los campos del formulario
            nombre = self.nombreText.text()
            dificultad = self.dificultadText.text()
            score = self.scoreText.text()
            tiempo = self.tiempoText.text()
            juego = self.juegoText.text()
            # Actualizamos los campos en el modelo
            self.modelo.setData(self.modelo.index(self.fila, 0), nombre)
            self.modelo.setData(self.modelo.index(self.fila, 1), dificultad)
            self.modelo.setData(self.modelo.index(self.fila, 2), score)
            self.modelo.setData(self.modelo.index(self.fila, 3), tiempo)
            self.modelo.setData(self.modelo.index(self.fila, 4), juego)
            # Ejecutamos los cambios en el modelo
            self.modelo.submit()

    def nueva(self):
        # Guardamos en la variable nuevaFila el número de filas del modelo
        nuevaFila = self.modelo.rowCount()
        # Insertamos una nueva fila en el modelo en la posición de ese valor
        self.modelo.insertRow(nuevaFila)
        # Seleccionamos la fila nueva
        self.tabla.selectRow(nuevaFila)
        # Ponemos en blanco el texto la dificultad en el formulario
        self.dificultadText.setText("")

        # Establecemos en blanco los valores de esa nueva fila
        self.modelo.setData(self.modelo.index(nuevaFila, 1), "")
        self.modelo.setData(self.modelo.index(nuevaFila, 2), 0)
        # Ejecutamos los cambios en el modelo
        self.modelo.submit()

    def borrar(self):
        # Si es una fila válida la seleccionada
        if self.fila >= 0:
            # Borramos la fila en el modelo
            self.modelo.removeRow(self.fila)
            # Actualizamos la tabla
            self.modelo.select()
            # Y ponemos la fila actual a -1
            self.fila = -1
            # Reseteamos los valores en los campos del formulario
            self.nombreText.setText("")
            self.dificultadText.setText("")
            self.scoreText.setText("")
            self.tiempoText.setText("")
            self.juegoText.setText("")
class AnotherWindow2(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Informe")
        self.web = QWebEngineView()
        self.web.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        ruta = Path("result.pdf")
        ruta.absolute().as_uri()
        self.web.load(QUrl(ruta.absolute().as_uri()))
        self.setCentralWidget(self.web)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("App SimpGam")
        self.contenedor= QWidget()
        self.layout = QVBoxLayout()
        self.button1 = QPushButton("Jugar")
        self.button2 = QPushButton("Estadísticas")
        self.button3 = QPushButton("Salir")
        self.button1.setStyleSheet("border:7px solid #ff0000")
        self.button2.setStyleSheet("border:7px solid #ff0000")
        self.button3.setStyleSheet("border:7px solid #ff0000")
        self.button1.setMinimumSize(50,50)
        self.button2.setMinimumSize(50,50)
        self.button3.setMinimumSize(50,50)
        self.button1.clicked.connect(self.button_clicked)
        self.button2.clicked.connect(self.button2_clicked)
        self.button3.clicked.connect(self.button3_clicked)
        self.w = AnotherWindow()
        self.w2 = AnotherWindow2()
        self.button4 = QPushButton()
        self.button4.setText("Salir")
        self.button4.clicked.connect(self.button4_clicked)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.contenedor.setLayout(self.layout)
        self.setCentralWidget(self.contenedor)

        
        self.wizard = QWizard()

        self.wizard.setWizardStyle(QWizard.ModernStyle)

        self.wizard.setPixmap(QWizard.WatermarkPixmap,QPixmap('Watermark.png'))
        self.wizard.setPixmap(QWizard.LogoPixmap,QPixmap('Logo.png'))
        self.wizard.setPixmap(QWizard.BannerPixmap,QPixmap('Banner.png'))

        page1 = QWizardPage()
        page1.setTitle('Introduzca tu nombre y el juego jugado')
        self.nombre = QLineEdit()
        self.juegoB= QComboBox()
        query = QSqlQuery("SELECT DISTINCT juego FROM estadisticas",db=db)
        while query.next():
            self.juegoB.addItem(query.value(0))
        hLayout1 = QHBoxLayout(page1)
        hLayout1.addWidget(self.nombre)
        hLayout1.addWidget(self.juegoB)
        page1.registerField('miCampo1*', self.nombre,self.nombre.text(),'textChanged')
        page1.registerField('miCampo1.2', self.juegoB,self.juegoB.currentText())
        self.wizard.addPage(page1)

        page2 = QWizardPage()
        page2.setTitle('Nivel de dificultad elegido')
        dificultadN = random.randint(1, 3)
        if(dificultadN==1):
            self.dificultad = QLabel("Fácil")
        elif(dificultadN==2):
            self.dificultad = QLabel("Normal")
        else:
            self.dificultad = QLabel("Difícil")
        hLayout2 = QHBoxLayout(page2)
        hLayout2.addWidget(self.dificultad)

        self.wizard.addPage(page2)

        page3 = QWizardPage()
        page3.setTitle('Puntuación obtenida')
        self.score = str(random.randint(0, 300))
        self.puntuacion = QLabel(self.score)
        hLayout3 = QHBoxLayout(page3)
        hLayout3.addWidget(self.puntuacion)
        
        self.wizard.addPage(page3)

        page4 = QWizardPage()
        page4.setTitle('Tiemplo empleado en la partida')
        tiempoH = str(random.randint(0, 3))
        tiempoM= str(random.randint(0, 59))
        tiempoS= str(random.randint(0, 59))
        self.tiempoTotal= (tiempoH*60)+tiempoM
        formato= tiempoH+":"+tiempoM+":"+tiempoS
        self.tiempo = QLabel(formato)
        hLayout4 = QHBoxLayout(page4)
        hLayout4.addWidget(self.tiempo)
        page4.setFinalPage(True)

        next = self.wizard.button(QWizard.NextButton)

        finish = self.wizard.button(QWizard.FinishButton)
        finish.clicked.connect(self.generate)

        self.wizard.addPage(page4)
        
    def generate(self):
        self.puntMax = QSqlQuery("SELECT MAX(score) FROM estadisticas WHERE juego='"+self.juegoB.currentText()+"'",db=db)
        self.puntMax.next()
        self.data = {
            'nombre': self.nombre.text(),
            'dificultad': self.dificultad.text(),
            'puntuacion': self.puntuacion.text(),
            'tiempo': self.tiempo.text(),
            'juego': self.juegoB.currentText(),
            'puntuación máxima del juego': str(self.puntMax.value(0))
        }
        query = QSqlQuery("SELECT score FROM estadisticas",db=db)
        
        query.next()
        scor1= query.value(0)
        query.next()
        scor2= query.value(0)
        query.next()
        scor3= query.value(0)
        if(scor1 is None):
            scor1=0
        if(scor2 is None):
            scor2=0
        if(scor3 is None):
            scor3=0
        plt = pg.plot([scor1,scor2,scor3,int(self.score)])

        # Creamos una instancia de exportación con el ítem que queremos exportar
        exporter = pg.exporters.ImageExporter(plt.plotItem)

        # Establecemos los parámetros de la exportación (anchura)
        exporter.parameters()['width'] = 100   # (afecta a la altura de forma proporcional)

        # Elegimos el nombre del archivo en el que exportamos la gráfica como imagen
        exporter.export('graphic.png')

        outfile = "result.pdf"

        template = PdfReader("template.pdf", decompress=False).pages[0]
        template_obj = pagexobj(template)

        canvas = Canvas(outfile)

        xobj_name = makerl(canvas, template_obj)
        canvas.doForm(xobj_name)

        ystart = 820
        today = datetime.today()
        canvas.drawString(510, ystart, today.strftime('%F'))

        canvas.drawString(165, ystart-57, self.data['nombre'])
        canvas.drawString(165, ystart-97, self.data['dificultad'])
        canvas.drawString(165, ystart-137, self.data['puntuacion'])
        canvas.drawString(165, ystart-177, self.data['tiempo'])
        canvas.drawString(165, ystart-220, self.data['juego'])
        canvas.drawString(300, ystart-265, self.data['puntuación máxima del juego'])
        canvas.drawImage("graphic.png", 50, ystart-350, width=None,height=None,mask=None)






        canvas.save()
        layout2 = QVBoxLayout()
        
        self.web = QWebEngineView()
        
        plt.hide()
        self.web.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        
        #rutaConPDF = Path("template.pdf")
        #self.web.load(QUrl(rutaConPDF.absolute().as_uri()))
        #layout2.addWidget(self.web)
        #layout2.addWidget(self.button4)
        #contenedor2= QWidget()
        #contenedor2.setLayout(layout2)
        #self.setCentralWidget(contenedor2)
        
        QMessageBox.information(self, "Finalizado", "Se ha generado el PDF")
        self.w2.show()
        
    def button_clicked(self, s):
        self.wizard.show()
    def button2_clicked(self, checked):
        
        if self.w.isVisible():
            self.w.hide()

        else:
            self.w.show()
    def button3_clicked(self, s):
        self.close()
    def button4_clicked(self,s):
        self.setCentralWidget(self.contenedor)
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()