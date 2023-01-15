# --- import 
from typing_extensions import Self
from PyQt6.QtWidgets import QWidget, QFrame
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QLabel, QLineEdit, QDateEdit, QTextEdit, QPushButton, QRadioButton
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from Tabs import Tabs
import StatsView
import ListeWidget
# ----------------------------------------------------------------------
# --- class FilmVue
# ----------------------------------------------------------------------
class GlobalView (QWidget):
    # +--------------+-------------------+-----------------+
    # |              |                   |                 |
    # |              |                   |                 |
    # |              |                   |                 |
    # |  Listes*3    |      FilmVie      |    Stats        |
    # |              |                   |                 |
    # |              |                   |                 |
    # |              |                   |                 |
    # +--------------+-------------------+-----------------+
    
    # Signaux
    suivant : pyqtSignal = pyqtSignal()
    precedent : pyqtSignal = pyqtSignal()
    prochain : pyqtSignal = pyqtSignal(int)
    liste : pyqtSignal = pyqtSignal(list, list, list) 
    selectall : pyqtSignal = pyqtSignal(str)
    deselectall : pyqtSignal = pyqtSignal(str)

    boutonNext2 : pyqtSignal = pyqtSignal(int, int)
    boutonBack2 : pyqtSignal = pyqtSignal(int, int)
    # constructor
    def __init__(self : Self, films: list[dict], listeGenre: list[str], listeDistrib: list[str], listeLicenses: list[str], index: int, taille: int, listeTitre:list[str]) -> None:
        super().__init__()
        
        # drawGUI
        self.setWindowTitle("Notre superbe projet de SAE")
        self.globalLayout : QHBoxLayout = QHBoxLayout()
        self.setLayout(self.globalLayout)



        #---------- Gauche ------------------
        # Les 3 listes
        self.soussousgaucheLayout : QHBoxLayout = QHBoxLayout()
        self.soussousgaucheWidget : QFrame() = QFrame()

        self.distrib=ListeWidget.ListeWidget(listeDistrib, "distrib")
        self.genre=ListeWidget.ListeWidget(listeGenre, "genre")
        self.licenses=ListeWidget.ListeWidget(listeLicenses, "licenses")



        self.soussousgaucheLayout.addWidget(self.distrib)
        self.soussousgaucheLayout.addWidget(self.genre)
        self.soussousgaucheLayout.addWidget(self.licenses)



        self.soussousgaucheLayout.itemAt(0).widget().setFixedWidth(175)
        self.soussousgaucheLayout.itemAt(1).widget().setFixedWidth(125)
        self.soussousgaucheLayout.itemAt(2).widget().setFixedWidth(100)
        self.soussousgaucheWidget.setLayout(self.soussousgaucheLayout)

        # Layout global gauche
        self.gaucheLayout : QVBoxLayout = QVBoxLayout()

        self.gaucheWidget : QFrame() = QFrame()
        self.gaucheWidget.setFrameStyle(QFrame.Shape.StyledPanel) 
        self.gaucheLayout.addWidget(self.soussousgaucheWidget)
        self.filtrerButton : QPushButton = QPushButton('Filtrer')
        self.gaucheLayout.addWidget(self.filtrerButton)
        
        self.gaucheWidget.setLayout(self.gaucheLayout)

        self.globalLayout.addWidget(self.gaucheWidget)


         #---------- Centre ------------------
        self.centre=Tabs(films[index],listeTitre)
        self.centre.update(films[index], listeGenre, listeDistrib, listeLicenses, index, taille,listeTitre)
        self.globalLayout.addWidget(self.centre)

         #---------- Droite ------------------
        self.droite=StatsView.StatsView(films, listeGenre, listeDistrib) 
        self.droite.update(0, films)
        self.globalLayout.addWidget(self.droite)


        self.globalLayout.setStretch(0, 1)
        self.globalLayout.setStretch(3, 6)

        # Les signaux
        self.centre.firstPageWidget.next.connect(self.cbNext)
        self.centre.firstPageWidget.previous.connect(self.cbPrevious)

        self.droite.prochain.connect(self.cbProchain)
        self.centre.secondPageWidget.CaseClicked.connect(self.cbProchain)

        
        self.filtrerButton.clicked.connect(self.cbList)


        self.droite.boutonNext1.connect(self.cbSuivant)
        self.droite.boutonBack1.connect(self.cbPrecedent)

        self.distrib.selectall.connect(self.select)
        self.genre.selectall.connect(self.select)
        self.licenses.selectall.connect(self.select)

        self.distrib.deselectall.connect(self.deselect)
        self.genre.deselectall.connect(self.deselect)
        self.licenses.deselectall.connect(self.deselect)

        # show() !
        self.show()

    def select(self, nom):
        self.selectall.emit(nom)
    
    def deselect(self, nom):
        self.deselectall.emit(nom)

    def updateListeSelect(self, nom : str):
        if nom == "distrib":
            self.distrib.selectAll()
        if nom == "genre":
            self.genre.selectAll()
        if nom == "licenses":
            self.licenses.selectAll()

    def updateListeDeSelect(self, nom : str):
        if nom == "distrib":
            self.distrib.deselectAll()
        if nom == "genre":
           self.genre.deselectAll()
        if nom == "licenses":
            self.licenses.deselectAll()

    def cbNext(self: Self) -> None:     self.suivant.emit()
    def cbPrevious(self: Self) -> None: self.precedent.emit()
    def cbProchain(self: Self, ind: int) -> None: self.prochain.emit(ind)
    def cbList(self) -> None: 
        self.liste.emit(self.distrib.getListe(), self.genre.getListe(), self.licenses.getListe())

    def getIndex(self) -> None : return self.centre.firstPageWidget.getIndex()

    def getListDistrib(self) -> None : return self.distrib.getListe()
    def getListGenre(self) -> None : return self.genre.getListe()
    def getListLicenses(self) -> None : return self.licenses.getListe()

    def cbSuivant(self, ind: int, maxoff: int) -> None: 
        self.boutonNext2.emit(ind, maxoff)

    def cbPrecedent(self, ind: int, maxoff: int) -> None: 
        self.boutonBack2.emit(ind, maxoff)
    
    def update(self, record : dict, genres : list[str], distributors : list[str],licenses : list[str], index: int, taille: int, films: list[dict],listeFilms:list[str]) -> None:
        self.centre.update(record, genres, distributors, licenses, index, taille,listeFilms)
        self.droite.update(index, films)
        self.centre.secondPageWidget.CaseClicked.connect(self.cbProchain)
    
    def updateGraph(self, ind: int) -> None:
        self.droite.updateGraph(ind)
# --- main: kind of unit test
if __name__ == "__main__" :
    import sys
    from PyQt6.QtWidgets import QApplication
    import ModeleBDD as MB
    db=MB.ModeleBDD()
    app = QApplication(sys.argv)
    fv = GlobalView(db.getAllFilms(),db.getAllGenres(), db.getAllDistibutors(), db.getAllLicenses(),10,918,db.getListTitle())
    fv.show()

    sys.exit(app.exec())
