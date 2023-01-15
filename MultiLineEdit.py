from typing_extensions import Self
from PyQt6.QtWidgets import QWidget, QLineEdit, QLabel
from PyQt6.QtWidgets import QVBoxLayout

class MultiLineEdit (QWidget):
    # constructor
    def __init__(self : Self,info:str| None= None) -> None:
        super().__init__()

        # attributes
        self.lineEdits : list[QLineEdit]=  []

        # gui
        self.topLayout : QVBoxLayout = QVBoxLayout() ; self.setLayout(self.topLayout)
        if info: self.topLayout.addWidget(QLabel(info))
        # show()
        # self.show()

    def addItem(self : Self, item : str) -> None: 
        iLE = QLineEdit() 
        iLE.setText(item)
        self.lineEdits.append(iLE)
        self.topLayout.addWidget(iLE)
    
    def removeLast(self : Self, key : str| None=None) -> None:
        if not key:
            if len(self.lineEdits)>0 :
                self.lineEdits[-1].deleteLater()
                self.lineEdits.pop()
        else:
            for idx, i in enumerate(self.lineEdits):
                if i.text() == key:
                    i.deleteLater() 
                    self.lineEdits.pop(idx)
                    break 

    def clear(self : Self) -> None:
        for idx, i in enumerate(self.lineEdits):
            i.deleteLater() 
        self.lineEdits.clear()

# -- main: test
if __name__ == "__main__" :
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)

    test = MultiLineEdit()
    test.show()
    test.addItem('A 0') ; input('go') 
    test.addItem('B 0') ; input('go')
    test.addItem('C 0') ; input('go')
    test.addItem('D 0') ; input('go')
    test.removeLast('B 0') ; input('go')
    test.removeLast() ; input('go')
    test.addItem('A 1') ; input('go')
    test.addItem('B 1') ; input('go')
    test.addItem('C 1') ; input('go')
    test.addItem('D 1') ; input('go -> clear')
    test.clear() ; input('go -> end clear')
    test.addItem('A 2') ; input('go')
    test.addItem('B 2') ; input('go')    

    sys.exit(app.exec())
    



