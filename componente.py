from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import (Property, QSize, Qt, Signal)

from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QBrush, QPen
import functools

PALETTES = {
    'paired12':['#0000FF', '#FF0000']
}
def helper_function(widget, color):
        widget.setStyleSheet("background-color: {}".format(color.name()))


def apply_color_animation(widget, start_color, end_color, duration=2):
    anim = QtCore.QVariantAnimation(
        widget,
        duration=duration,
        startValue=start_color,
        endValue=end_color,
    )
    anim.valueChanged.connect(functools.partial(helper_function, widget))
    anim.start()
class _PaletteButton(QtWidgets.QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24, 24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)
class _PaletteBase(QtWidgets.QWidget):

    selected = Signal(object)

    def _emit_color(self, color):
        self.selected.emit(color)
class _PaletteLinearBase(_PaletteBase):
    def __init__(self, colors, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(colors, str):
            if colors in PALETTES:
                colors = PALETTES[colors]

        palette = self.layoutvh()

        for c in colors:
            b = _PaletteButton(c)
            b.pressed.connect(
                lambda c=c: self._emit_color(c)
            )
            palette.addWidget(b)

        self.setLayout(palette)
class PaletteHorizontal(_PaletteLinearBase):
    layoutvh = QtWidgets.QHBoxLayout


class PaletteVertical(_PaletteLinearBase):
    layoutvh = QtWidgets.QVBoxLayout
class PaletteGrid(_PaletteBase):

    def __init__(self, colors, n_columns=5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(colors, str):
            if colors in PALETTES:
                colors = PALETTES[colors]

        palette = QtWidgets.QGridLayout()
        row, col = 0, 0

        for c in colors:
            b = _PaletteButton(c)
            b.pressed.connect(
                lambda c=c: self._emit_color(c)
            )
            palette.addWidget(b, row, col)
            col += 1
            if col == n_columns:
                col = 0
                row += 1

        self.setLayout(palette)
        
class Botton(QPushButton):
    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)
    def __init__(self,
        parent=None,
        bar_color=Qt.gray,
        checked_color="#00B0FF",
        handle_color=Qt.white,
        pulse_unchecked_color="#44999999",
        pulse_checked_color="#4400B0EE"
        ):
        super().__init__(parent)
        self._bar_brush = QBrush(bar_color)
        self.setText("No presiones")
        self.setAutoFillBackground(True)
        self.clicked.connect(self.cambioColor)
        self.contador= 0
        
    def cambioColor(self):
        self.contador=self.contador+1
        if(self.contador==1):
            self.setText("Toca un botón de color")
        elif(self.contador==2):
            self.setText("¡Los botones debajo de este!")
        elif(self.contador==3):
            self.setText("¡Abajo!")
        elif(self.contador==4):
            self.setText("¿Me vas a hacer que te lo repita?")
        elif(self.contador==5):
            self.setText("...")
            self.contador=0
        self.show()

class componente(QtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QtWidgets.QVBoxLayout()
        self.botton = Botton()
        layout.addWidget(self.botton)
        
        palette = PaletteGrid('paired12')
        palette.selected.connect(self.show_selected_color)
        layout.addWidget(palette)
        layout.addWidget(self.botton)
        self.setLayout(layout)
        self.color1= (QtGui.QColor("#E9EBEF"))
        self.color2= (QtGui.QColor("#0000FF"))
    def getBottomColor(self):
        return self.botton.property("background-color")
    def getColor1(self):
        return self.color1
    def getColor2(self):
        return self.color2
    def setColor1(self, color1):
        self.color1 = color1
    def setColor2(self, color2):
        self.color2 = color2
    def sizeHint(self):
        return QSize(100, 124)
    value1 = Property(int, getColor1, setColor1)
    value2 = Property(int, getColor2, setColor2)
    def handle_timeout(self):
                apply_color_animation(
                    self,
                    self.color1,
                    self.color2,
                    duration=2000,
                )
    def show_selected_color(self, c):
        if(format(c)=="#0000FF"):
            self.setColor1(QtGui.QColor("#E9EBEF"))
            self.setColor2(QtGui.QColor("#0000FF"))
            self.handle_timeout()
        if(format(c)=="#FF0000"):
            self.setColor1(QtGui.QColor("pink"))
            self.setColor2(QtGui.QColor("#FF0000"))
            self.handle_timeout()