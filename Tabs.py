import sys
from PyQt6.QtWidgets import (
    QApplication,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QComboBox
)
from FilmView import FilmView
from GrilleFilms import GrilleFilms




class Tabs(QWidget):
    
    def __init__(self, record : dict, listeTitre: list[str]):
        super().__init__()
        self.secondPageWidget = GrilleFilms(listeTitre)
        self.firstPageWidget = FilmView(record)
        

        self.stackedLayout = QStackedLayout()
        self.stackedLayout.addWidget(self.firstPageWidget)
        self.stackedLayout.addWidget(self.secondPageWidget)


        self.mainLayout = QVBoxLayout()
        
        self.setLayout(self.mainLayout)

        self.pageComboBox = QComboBox()
        self.pageComboBox.addItem("Film current")
        self.pageComboBox.addItem("Grille des films")
        self.mainLayout.addWidget(self.pageComboBox)
        self.mainLayout.addLayout(self.stackedLayout)
        self.pageComboBox.activated.connect(self.stackedLayout.setCurrentIndex)
        
        
        
    def update(self, record : dict, genres : list[str], distributors : list[str],licenses : list[str], index: int, taille: int, ListeTitre: list[str]):
        self.firstPageWidget.update(record, genres, distributors, licenses, index, taille)
        self.stackedLayout.setCurrentIndex(0)
        self.secondPageWidget.deleteLater()
        self.secondPageWidget = GrilleFilms(ListeTitre)
        self.stackedLayout.addWidget(self.secondPageWidget)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    from ModeleBDD import ModeleBDD
    m=ModeleBDD()
    print(m.getAllFilms()[0])
    window = Tabs(m.getAllFilms()[80],m.getListTitle()[80:90])
    window.update(m.getAllFilms()[80], m.getAllGenres(),m.getAllDistibutors(),m.getAllLicenses(),80,198,m.getListTitle()[80:90])
    window.show()

    sys.exit(app.exec())