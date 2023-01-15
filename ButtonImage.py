from time import sleep
import WImage
from PyQt6.QtWidgets import QPushButton, QHBoxLayout

class ButtonImage(QPushButton):
    
    def __init__(self, requete:str):
        super().__init__()
        
        self.coreLayout : QHBoxLayout = QHBoxLayout()
        self.setLayout(self.coreLayout)
        self.widget = WImage.WImage()
        self.setMaximumHeight(200)
        self.setMaximumWidth(200)
        self.widget.query(requete)
        self.coreLayout.addWidget(self.widget)
        

        
        
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    test = ButtonImage("Remi Cozot")
    test.show()
    sys.exit(app.exec())