# --- import 
from typing_extensions import Self
from PyQt6.QtWidgets import QWidget, QFrame
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backend_tools import Cursors
import datetime as dt
from wordcloud import WordCloud
# ----------------------------------------------------------------------
# --- class StatsView
# ----------------------------------------------------------------------

class StatsView (QWidget):
    prochain : pyqtSignal = pyqtSignal(int)
    boutonNext1 : pyqtSignal = pyqtSignal(int, int)
    boutonBack1 : pyqtSignal = pyqtSignal(int, int)
    # +---------------------------------------------------------------------+
    # |                                                                     | 
    # |                                                                     | 
    # |                                                                     | 
    # |                                                                     | 
    # |                            GRAPHIQUE                                | 
    # |                                                                     | 
    # |                                                                     |
    # |                                                                     | 
    # |                                                                     | 
    # +---------------------------------------------------------------------+
    
    # constructor
    def __init__(self : Self, films: dict, genre: list, distrib: list) -> None:
        # initialisation des variables
        super().__init__()
        self.films = films
        self.index = 0
        self.figure : Figure = Figure()
        self.genre = genre
        self.distrib = distrib
        self.coordClick = []
        
        # affichage du graphique avec un cadre
        self.canvas = FigureCanvas(self.figure)
        
        # on enleve la figure créée précédement avant de recréer la nouvelle
        self.canvas.figure.clear()
        


        self.idplot = 1
        self.maxidplot = 4
        self.plot(self.idplot)
        
        # création de l'affichage de la partie de droite
        self.mainLayout : QVBoxLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.globalWidget : QFrame = QFrame()
        self.globalWidget.setFrameStyle(QFrame.Shape.StyledPanel)
        self.mainLayout.addWidget(self.globalWidget)

        self.layoutPrincipal : QVBoxLayout = QVBoxLayout()
        self.globalWidget.setLayout(self.layoutPrincipal)




        #ajout du graphique
        self.layoutPrincipal.addWidget(self.canvas) 
        
        
        # ajout des boutons 
        self.widgetBottom : QWidget = QWidget()
        self.layoutPrincipal.addWidget(self.widgetBottom) 

        self.layoutBottom : QHBoxLayout = QHBoxLayout()
        self.widgetBottom.setLayout(self.layoutBottom)
        self.widgetBottom.setFixedHeight(50)

        self.boutonNext : QPushButton = QPushButton("->")
        self.boutonBack : QPushButton = QPushButton("<-")
        
        self.layoutBottom.addWidget(self.boutonBack)
        self.layoutBottom.addStretch(1)
        self.layoutBottom.addWidget(self.boutonNext)
        
        self.setStyleSheet("background-color: white")
        self.setMinimumSize(700, 400)

        #Les signaux
        self.boutonNext.clicked.connect(self.suivant)
        self.boutonBack.clicked.connect(self.precedent)

    def plot(self, valeur: int):
        if (valeur == 1):
            self.test2=self.films[self.index]['releaseDate'][0:4]

            self.x2 = dt.datetime.strptime(self.test2,'%Y').date() #la date
            self.y2 = self.films[self.index]['worldSales'] #le nombre

            dates = []
            for i in range (len(self.films)):
                dates.append(self.films[i]['releaseDate'][0:4])
            
            worldsales = []
            for i in range (len(self.films)):
                worldsales.append(self.films[i]['worldSales'])

            self.x1 = [dt.datetime.strptime(d,'%Y').date() for d in dates]
            self.y1 = worldsales

            self.nuageDePoint(self.x1, self.y1, self.x2, self.y2)
            if len(self.coordClick) == 2:
                self.canvas.figure.mpl_disconnect('pick_event', self.onclick)

            self.figure.canvas.mpl_connect('pick_event', self.onclick)

            self.canvas.draw()
        if (valeur == 2):
            self.canvas.figure.clear()
            self.test2=self.films[self.index]['releaseDate'][0:4]

            x1 = ['1930','1940','1950','1960','1970','1980','1990','2000','2010','2020']
            y1 = self.compteFilmAnnee(x1)
            
            self.histogramme(x1,y1)
        if (valeur == 3):
            lesmots = ""
            for i in range (len(self.films)):
                for y in self.films[i]['genre']:
                    lesmots = lesmots + " " + self.genre[y]
            self.nuageDeMot(lesmots, "Nuage de mots des genres total par genre de films")
        if (valeur == 4):
            lesmots = ""
            for i in range (len(self.films)):
                lesmots = lesmots + " " + self.distrib[self.films[i]['distributor']]
            self.nuageDeMot(lesmots, "Nuage de mots des distributeurs total par distributeur de films")
    
    def nuageDeMot(self, text: str, titre: str):
        self.canvas.figure.clear()
        wordcloud = WordCloud(background_color = 'white').generate(text)
        ax = self.figure.add_subplot(111)
        ax.imshow(wordcloud)
        ax.title.set_text(titre)
        self.canvas.draw()
    
    def nuageDePoint(self, x1: int, y1: int, x2: int, y2: int):
        self.canvas.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.scatter(x1, y1, s=10, c='red', picker=True, pickradius=1, marker="o")
        ax.scatter(x2, y2, s=100, c='black', picker=True, pickradius=1, marker="*")
        ax.set_xlabel("Annee")
        ax.set_ylabel("Nombres de films")
        if len(self.coordClick) == 2:
            self.canvas.figure.mpl_disconnect('pick_event', self.onclick)

        self.figure.canvas.mpl_connect('pick_event', self.onclick)

        self.canvas.draw()
    
    def histogramme(self, x1: str, y1: str):
        self.canvas.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(x1, y1)
        ax.set_xlabel("Annee")
        ax.set_ylabel("Nombres de films")
        self.canvas.draw()



    def compteFilmAnnee(self, x):
        dates = []
        for i in range(len(x)):
            dates.append(0)
        for i in range (len(self.films)):
            for y in range(len(dates)):
                if self.films[i]['releaseDate'][0:3] == x[y][0:3]:
                    dates[y] = dates[y] + 1
        return dates

    def onclick (self, event):
        self.prochain.emit(event.ind[0])

    def precedent (self, max: int):
        self.boutonBack1.emit(self.idplot, self.maxidplot)

    def suivant (self, max: int):
        self.boutonNext1.emit(self.idplot, self.maxidplot)
    
    def updateGraph(self, ind2: int) -> None:
        self.idplot=ind2
        self.plot(self.idplot)
    
    def update(self : Self, index, films: dict) -> None:
        self.index = index
        self.films = films
        self.plot(self.idplot)

    # methods
    #Aucune pour le moment

    #------ TESTS MATPLOTLIB -------
    # Test afin de savoir si matplotlib s'ouvre avec pyqt dans un QWidget
    # Résolution au bout : 15 tests
    # Fonctionnement : Oui (données manuelles)

    #------ TESTS MATPLOTLIB -------
    # Test d'insertion dans la GlobalView
    # Résolution au bout : 15 tests
    # Fonctionnement : Oui (données manuelles)

    #------ TESTS MATPLOTLIB -------
    # Test de compatibilité avec les tries réussis
    # Résolution au bout : 15 tests
    # Fonctionnement : Oui (données manuelles)


    #/!\ Aurélian n'a pas ajouté les debuggers
    # getI
    # getWS

# --- main: kind of unit test
if __name__ == "__main__" :
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    main = StatsView()
    main.show()

    sys.exit(app.exec())