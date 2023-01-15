####################################################
import numpy as np
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QScrollArea, QPushButton, QGridLayout, QLabel
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt
import PyQt6.QtGui as Qg
from ButtonImage import ButtonImage


class GrilleFilms(QWidget):
    CaseClicked : pyqtSignal = pyqtSignal(int)
    
    def __init__(self, listeFilm: list[str]) -> None:
        super().__init__()
        self.tailleImage=120
        self.filmParLigne=4
        self.liste = listeFilm
        self.index=0
        
        # CoreLayout
        self.CoreLayout : QVBoxLayout = QVBoxLayout()
        self.setLayout(self.CoreLayout)

        
        # conteneurWidget avec grid 
        self.contLayout : QGridLayout = QGridLayout()
        self.widgetConteneur : QWidget = QWidget()
        self.widgetConteneur.setLayout(self.contLayout)
        
        self.tab=np.full([len(listeFilm)//self.filmParLigne+1,self.filmParLigne],None,dtype=ButtonImage)

        
            
        
        # défini la scrollbar
        self.scroll : QScrollArea = QScrollArea()

        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widgetConteneur)
        self.CoreLayout.addWidget(self.scroll)
        
        # load more
        if self.index<len(listeFilm):
            self.loadButton : QPushButton = QPushButton("Charger plus d'images")
            self.loadButton.clicked.connect(self.load)
            self.CoreLayout.addWidget(self.loadButton)
        
        self.show()
        
    def caseClick(self):
        b=self.sender()
        for i in range(0,self.index):
            if b == self.contLayout.itemAt(i).widget():
                self.CaseClicked.emit(i)
                return

    def load(self):
        
        if self.index+self.filmParLigne*2<len(self.liste): 
            max = self.filmParLigne*2 
        else : 
            max = len(self.liste)-self.index
            self.loadButton.setHidden(True)
        for i in range(self.index,self.index+max):
            self.tab[i//self.filmParLigne,i%self.filmParLigne]=ButtonImage(self.liste[i])
            self.contLayout.addWidget(self.tab[i//self.filmParLigne,i%self.filmParLigne],i//self.filmParLigne,i%self.filmParLigne)
            self.tab[i//self.filmParLigne,i%self.filmParLigne].setFixedWidth(self.tailleImage)
            self.tab[i//self.filmParLigne,i%self.filmParLigne].setFixedHeight(self.tailleImage)
            self.tab[i//self.filmParLigne,i%self.filmParLigne].clicked.connect(self.caseClick)
            print("image n°",i,"chargée")
        
        self.index+=max
        
        
if __name__=="__main__":
    import sys
    app = QApplication(sys.argv)
    screen = app.screens()[0]

    
    # windows list
    firstWindows = GrilleFilms(["1","2","3","4","5","6","7","8","9","10","1","2","3","4","5","6","7","8","9","10"])
    
    #start Qt engine
    sys.exit(app.exec()) # fin boucle d'intéraction