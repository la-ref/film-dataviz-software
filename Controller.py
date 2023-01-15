# --- import 
from typing_extensions import Self
from PyQt6.QtCore import pyqtSignal

import ModeleBDD as MB
import GlobalView as GV
# ----------------------------------------------------------------------
# --- class Controller
# ----------------------------------------------------------------------
class Controller:
    # +--------------+-------------------+-----------------+
    # |              |                   |                 |
    # |              |                   |                 |
    # |              |                   |                 |
    # |  Listes      |      FilmVie      |    Stats        |
    # |              |                   |                 |
    # |              |                   |                 |
    # |              |                   |                 |
    # +--------------+-------------------+-----------------+
    
    # constructor
    def __init__(self : Self) -> None:
        super().__init__()
        
        # drawGUI
        self.MB = MB.ModeleBDD()
        self.index = 0
        self.idplot = 1
        self.view = GV.GlobalView(self.MB.getFilms(),self.MB.getAllGenres(), self.MB.getAllDistibutors(), self.MB.getAllLicenses(), self.index, len(self.MB.getFilms()),self.MB.getListTitle())
        
        # Les signaux
        self.view.suivant.connect(self.up)
        self.view.precedent.connect(self.down)
        self.view.liste.connect(self.updategeneral)
        self.view.prochain.connect(self.updatescatter_and_grid)

        self.view.boutonNext2.connect(self.suivant)
        self.view.boutonBack2.connect(self.precedent)

        self.view.selectall.connect(self.selectAll)
        self.view.deselectall.connect(self.deselectAll)
        

    def getIndex(self) -> None : 
        return self.view.getIndex()

    def up(self):
        currentIndex = self.getIndex()
        if currentIndex == len(self.MB.getFilms())-1:
            currentIndex = 0
        else:
            currentIndex = currentIndex + 1
        self.view.update(self.MB.getFilms()[currentIndex],self.MB.getAllGenres(), self.MB.getAllDistibutors(), self.MB.getAllLicenses(), currentIndex, len(self.MB.getFilms()), self.MB.getFilms(),self.MB.getListTitle())

    def down(self):
        currentIndex = self.getIndex()
        if currentIndex == 0:
            currentIndex = len(self.MB.getFilms())-1
        else:
            currentIndex = currentIndex - 1
        self.view.update(self.MB.getFilms()[currentIndex],self.MB.getAllGenres(), self.MB.getAllDistibutors(), self.MB.getAllLicenses(), currentIndex, len(self.MB.getFilms()), self.MB.getFilms(),self.MB.getListTitle())
    
    def updategeneral(self, distrib : list[str], genre: list[str], lic: list[str]):
        self.MB.filtrer(distrib, genre, lic)
        self.view.update(self.MB.getFilms()[0], self.MB.getAllGenres(), self.MB.getAllDistibutors(), self.MB.getAllLicenses(), 0, len(self.MB.getFilms()), self.MB.getFilms(),self.MB.getListTitle())

    def updatescatter_and_grid(self, ind: int):
        self.view.update(self.MB.getFilms()[ind],self.MB.getAllGenres(), self.MB.getAllDistibutors(), self.MB.getAllLicenses(), ind, len(self.MB.getFilms()), self.MB.getFilms(),self.MB.getListTitle())

    def precedent (self,nombre: int, maxoff: int):
        if nombre-1 < 1:
            nombre = maxoff
        else:
            nombre=nombre-1
        self.view.updateGraph(nombre)

    def suivant (self,nombre: int, maxoff: int):
        if nombre+1 > maxoff:
            nombre = 1
        else:
            nombre=nombre+1
        self.view.updateGraph(nombre)
    
    def selectAll(self, nom : str):
        self.view.updateListeSelect(nom)
    
    def deselectAll(self, nom : str):
        self.view.updateListeDeSelect(nom)
        
# --- main: kind of unit test
if __name__ == "__main__" :
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    fv = Controller()

    sys.exit(app.exec())
