
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QPushButton
import PyQt6.QtCore as Qt
from PyQt6.QtCore import pyqtSignal

from ElementListe import ElementListe


# ----------------------------------------------------------------------
# --- class ListeWidget
# ----------------------------------------------------------------------
class ListeWidget(QWidget):
    selectall :pyqtSignal = pyqtSignal(str)
    deselectall :pyqtSignal = pyqtSignal(str)
    
    def __init__(self, liste: list[str], nom: str) -> None:
        super().__init__()
        self.nom = nom
        
        self.nbWidget : int = len(liste)
        self.listeWidget: list[ElementListe] = []
        
        # défini le widget conteneur
        self.WidgetConteneur : QWidget = QWidget()
        self.VLayout : QVBoxLayout = QVBoxLayout()
        self.WidgetConteneur.setLayout(self.VLayout)
        # ajoute les widget au conteneur
        for i in range(self.nbWidget):
            self.listeWidget.append(ElementListe(i,liste[i]))
            self.VLayout.addWidget(self.listeWidget[-1])
            
        # défini la scrollbar
        self.scroll : QScrollArea = QScrollArea()
        self.coreLayout : QVBoxLayout = QVBoxLayout()
        self.setLayout(self.coreLayout)
        
        self.haut : QPushButton = QPushButton("select all")
        self.bas : QPushButton = QPushButton("deselect all")
        self.coreLayout.addWidget(self.haut)
        self.coreLayout.addWidget(self.bas)

        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.WidgetConteneur)
        self.coreLayout.addWidget(self.scroll)

        
        #signaux bouton clic
        self.haut.clicked.connect(self.select)
        self.bas.clicked.connect(self.deselect)
        
        
        # self.show()

        
    def select(self):
        self.selectall.emit(self.nom)
    
    def deselect(self):
        self.deselectall.emit(self.nom)

        
    def selectAll(self):
        for child in self.listeWidget:
            child.setChecked(True)
    
    def deselectAll(self):
        for child in self.listeWidget:
            child.setChecked(False)
        
    def getListe(self):
        liste=[]
        for child in self.listeWidget:
            if child.isChecked():
                liste.append(child.text())
        return liste

    
            
        
        
        
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = ListeWidget(["ahah","hihi","huuh","ohho"], "bonjour")
    window.show()
    sys.exit(app.exec())