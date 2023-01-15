# --- import 
import json
from typing_extensions import Self
from PyQt6.QtWidgets import QWidget, QFrame
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QLabel, QLineEdit, QDateEdit, QTextEdit, QPushButton
from PyQt6.QtCore import Qt, QDate, pyqtSignal

from LabelledWidget import LabelledWidget
from MultiLineEdit import MultiLineEdit
from WImage import WImage
# ----------------------------------------------------------------------
# --- class FilmView
# ----------------------------------------------------------------------
class FilmView (QWidget):
    # +---------------------------------------------------------------------+
    # | title                                                               | 
    # +-------------------+--------------------------+----------------------+
    # |  Distributor      |      Release Date        | license              |
    # +-------------------+--------------------------+----------------------+
    # |      genre        |         run time         |                      |
    # +-------------------+--------------------------+----------------------+
    # |   revenu Domestic |   revenu international   | revenu worlds sales  |
    # +-------------------+--------------------------+----------------------+
    # |              descriptif                      |        image         |    
    # +-------------------+--------------------------+----------------------+
    # | previous | -------------------- message -------------------- | next |
    # +-------------------+--------------------------+----------------------+
    
    # signaux
    next : pyqtSignal = pyqtSignal()
    previous : pyqtSignal = pyqtSignal()

    # constructor
    def __init__(self : Self, record : dict) -> None:
        super().__init__()
        self.__record : dict = record
        self.index = 0
        # drawGUI
        self.topLayouyt : QVBoxLayout = QVBoxLayout() ; self.setLayout(self.topLayouyt)

        # info1 Widget
        self.info1Widget : QFrame = QFrame() ; self.info1Layout : QHBoxLayout = QHBoxLayout() ; self.info1Widget.setLayout(self.info1Layout)   
        self.info1Widget.setFrameStyle(QFrame.Shape.StyledPanel) 

        # info2 Widget
        self.info2Widget : QFrame = QFrame() ; self.info2Layout : QHBoxLayout = QHBoxLayout() ; self.info2Widget.setLayout(self.info2Layout)   
        self.info2Widget.setFrameStyle(QFrame.Shape.StyledPanel) 

        # revenu Widget
        self.revenuWidget : QFrame = QFrame() ; self.revenuLayout : QHBoxLayout = QHBoxLayout() ; self.revenuWidget.setLayout(self.revenuLayout)
        self.revenuWidget.setFrameStyle(QFrame.Shape.StyledPanel) 
        
        # dataWidget
        self.dataWidget : QFrame = QFrame() ; self.dataLayout : QHBoxLayout = QHBoxLayout() ; self.dataWidget.setLayout(self.dataLayout)
        self.revenuWidget.setFrameStyle(QFrame.Shape.StyledPanel) 

        # navMsgWidget
        self.navMsgWidget : QFrame = QFrame() ; self.navMsgLayout : QHBoxLayout = QHBoxLayout() ; self.navMsgWidget.setLayout(self.navMsgLayout)
        self.navMsgWidget.setFrameStyle(QFrame.Shape.StyledPanel) 

        # row 1: titre
        self.title = QLabel("Title") ; self.topLayouyt.addWidget(self.title)

        # row 2: Distributor, Date, license
        self.distributorLE = QLineEdit() 
        self.distributor = LabelledWidget("Distributor:", self.distributorLE,"distributor name", Qt.Orientation.Vertical, self.distributorLE.setText, self.distributorLE.text, None)
        self.info1Layout.addWidget(self.distributor)
        self.releaseDateLE = QDateEdit()
        self.releaseDate = LabelledWidget("Release date:", self.releaseDateLE,QDate(2000,1,2),Qt.Orientation.Vertical, self.releaseDateLE.setDate, self.releaseDateLE.date, None)
        self.info1Layout.addWidget(self.releaseDate)
        self.licenseLE = QLineEdit() 
        self.license = LabelledWidget("license:", self.licenseLE,"license", Qt.Orientation.Vertical, self.licenseLE.setText, self.licenseLE.text, None)
        self.info1Layout.addWidget(self.license)

        # row 3: genre, run-time
        self.genre = MultiLineEdit("Genre(s):") 
        self.genre.addItem("genre O")
        self.genre.addItem("genre 1")
        self.info2Layout.addWidget(self.genre)
        self.runtimeLE = QLineEdit() 
        self.runtime = LabelledWidget("Run-time (min):", self.runtimeLE,"120:00", Qt.Orientation.Horizontal,  self.runtimeLE.setText, self.runtimeLE.text, None)
        self.info2Layout.addWidget(self.runtime)


        # row 4 : revenue
        self.revenueDomesticLE = QLineEdit() 
        self.revenuDomestic = LabelledWidget("Domestic Sales (in $):", self.revenueDomesticLE,"1 000 000", Qt.Orientation.Horizontal,  self.revenueDomesticLE.setText, self.revenueDomesticLE.text, None)
        self.revenuInterLE = QLineEdit() 
        self.revenuInter = LabelledWidget("International Sales (in $):", self.revenuInterLE,"1 000 000", Qt.Orientation.Horizontal,  self.revenuInterLE.setText, self.revenuInterLE.text, None)
        self.revenuWorldLE = QLineEdit() 
        self.revenuWorld = LabelledWidget("World Sales (in $):", self.revenuWorldLE,"1 000 000", Qt.Orientation.Horizontal,  self.revenuWorldLE.setText, self.revenuWorldLE.text, None)        
        
        self.revenuLayout.addWidget(self.revenuDomestic)
        self.revenuLayout.addWidget(self.revenuInter)
        self.revenuLayout.addWidget(self.revenuWorld)

        # row 5: descriptif, (image)
        self.descriptif = QTextEdit("descriptif.")
        self.image = WImage()
        self.dataLayout.addWidget(self.descriptif,50)
        self.dataLayout.addWidget(self.image,50)

        # row 6: navigation + message
        self.previousButton : QPushButton = QPushButton('<<')
        self.msg : QLabel = QLabel(f'Film : {self.index+1} sur {len(self.__record)}')
        self.nextButton : QPushButton = QPushButton('>>')
        self.navMsgLayout.addWidget(self.previousButton)
        self.navMsgLayout.addStretch()
        self.navMsgLayout.addWidget(self.msg)
        self.navMsgLayout.addStretch()
        self.navMsgLayout.addWidget(self.nextButton)

        # all widgets to top Layout
        self.topLayouyt.addWidget(self.info1Widget)
        self.topLayouyt.addWidget(self.info2Widget)
        self.topLayouyt.addWidget(self.revenuWidget)
        self.topLayouyt.addWidget(self.dataWidget)
        self.topLayouyt.addWidget(self.navMsgWidget)

        # connections
        self.nextButton.clicked.connect(self.cbNext)
        self.previousButton.clicked.connect(self.cbPrevious)

        # show() !
        # self.show()


    # methods
    def update(self : Self, record : dict, genres : list[str], distributors : list[str],licenses : list[str], index: int, taille: int) -> None:
        # record = {"title" , "info" , "distributor" , "releaseDate" , "domesticSales" , "internationalSales" , "worldSales" , "genre" , "runtime" , "license" }
        self.title.setText(record["title"])
        self.distributor.set(distributors[record["distributor"]])
        self.releaseDate.set(QDate(int(record["releaseDate"].split('-')[0]),int(record["releaseDate"].split('-')[1]),int(record["releaseDate"].split('-')[2])))
        self.license.set(licenses[record["license"]])
        self.runtime.set(str(record["runtime"]))
        self.descriptif.setText(record["info"])
        self.revenuDomestic.set(str(record["domesticSales"]))
        self.revenuInter.set(str(record["internationalSales"]))
        self.revenuWorld.set(str(record["worldSales"]))
        self.image.query(record["title"])

        self.index = index
        self.taille = taille
        self.msg.setText(f'Film : {self.index+1} sur {self.taille}')

        self.genre.clear()
        for g in record["genre"]:
            self.genre.addItem(genres[g])

    def message(self : Self, msg : str) -> None: self.msg.setText(msg)

    # callbacks
    def cbNext(self: Self) -> None:     self.next.emit()
    def cbPrevious(self: Self) -> None: self.previous.emit()
    def getIndex(self: Self) -> None: return self.index

# --- main: kind of unit test
if __name__ == "__main__" :
    import sys
    from PyQt6.QtWidgets import QApplication
    import hhgm
    
    app = QApplication(sys.argv)
    try:
        f=open("./data/Highest_Holywood_Grossing_Movies.js")
        db = json.load(f)
    except OSError:
        csv = hhgm.HHGM()
        csv.loadCSV()
        csv.exportJSON()
        f=open("./data/Highest_Holywood_Grossing_Movies.json")
        db = json.load(f)
        
    fv = FilmView({})
    fv.update(db['films'][10],db['genres'], db['distributors'], db['licenses'],10,918)
    fv.show()
    sys.exit(app.exec())




