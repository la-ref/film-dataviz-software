
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QRadioButton,QHBoxLayout, QWidget


class ElementListe(QRadioButton):
    
    def __init__(self, indice:int, label:str) -> None:
        super().__init__(label)
        self.indice=indice
        self.setAutoExclusive(False)
        self.setChecked(True)
        
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = ElementListe(1,"label")
    window.show()
    sys.exit(app.exec())