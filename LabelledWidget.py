# a Widget with a label above or on the left

from typing import Callable, Any
from typing_extensions import Self
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt

class LabelledWidget (QWidget):
    # signal
    changed : pyqtSignal = pyqtSignal(object)

    # constructor
    def __init__(self : Self, info:str, 
                widget:QWidget, 
                data:Any ,
                orientation : Qt.Orientation,
                set: Callable[[Any],None], 
                get: Callable[[], Any], 
                signal : Callable | None) -> None :

        super().__init__()

        # getter and settter function for the embedded widget
        self.getter : Callable = get
        self.setter : Callable =  set

        # gui
        self.topLayout : QVBoxLayout|QHBoxLayout = QVBoxLayout()  if  orientation == Qt.Orientation.Vertical else  QHBoxLayout()  ; self.setLayout(self.topLayout)
        # label
        self.label : QLabel = QLabel(info) ; self.topLayout.addWidget(self.label)
        # widget
        self.widget : QWidget = widget ; self.topLayout.addWidget(self.widget) ; self.set(data)
        #self.topLayout.addStretch()

        # self.show()

        # callback
        if signal : signal.connect(self.changedCB)
    
    # getter and setter
    def get(self : Self) -> Any : return self.getter()
    def set(self : Self,val: Any): self.setter(val)

    # callback
    def changedCB(self: Self) -> None: self.changed.emit(self.get())

# --- main: kind of unit test
if __name__ == "__main__" :
    import sys
    from PyQt6.QtWidgets import QApplication, QLineEdit, QDial
    # callback function to test emit()
    def gcb(val) :  print(">>", val, type(val))
    
    app = QApplication(sys.argv)

    a = QDial()
    test = LabelledWidget("test:", a, 0, Qt.Orientation.Horizontal, a.setValue, a.value, a.valueChanged)
    test.show()
    test.changed.connect(gcb)
    test.set(25)
    print("testing: get :", test.get())

    sys.exit(app.exec())










