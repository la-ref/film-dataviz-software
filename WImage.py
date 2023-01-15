from http.client import responses
from typing_extensions import Self
import requests
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QResizeEvent
from PyQt6.QtCore import Qt,pyqtSignal

class WImage (QLabel):
    indImage : pyqtSignal = pyqtSignal(int,QPixmap)

    def __init__(self : Self) -> None:
        super().__init__()

        self.minSize = 400

        self.pixmax = QPixmap(self.minSize,self.minSize)
        self.setPixmap(self.pixmax)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # self.show() # ne sert que dans les tests

    def query(self : Self, image : str) -> None:
        try:
            r = requests.get("https://api.qwant.com/v3/search/images",timeout=2,
                params={
                    'count': 3,
                    'q': image,
                    't': 'images',
                    'safesearch': 1,
                    'locale': 'en_US',
                    'offset': 0,
                    'device': 'desktop'
                },
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                }
            )
            
            response = r.json().get('data').get('result').get('items')
            urls = [r.get('media') for r in response]
            
            pixmap = QPixmap()

            for i in range(len(responses)):
                response = requests.get(urls[i])

                pixmap.loadFromData(response.content)

                if not pixmap.isNull() : break

        
            
        except (requests.ConnectionError, requests.Timeout) as exception:
            pixmap = QPixmap("./image/no_connection.jpg")
        
        

        w = min(pixmap.width(), self.minSize)
        h = min(pixmap.height(), self.minSize)
        self.pixmax = pixmap.scaled(w,h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
        self.setPixmap(self.pixmax.scaled(self.width(),self.height(),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation ))
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    def resizeEvent(self : Self, a0: QResizeEvent) -> None:
        pixmap = self.pixmax
        pixmap = pixmap.scaled(a0.size(),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
        self.setPixmap(pixmap)

# --- main: kind of unit test        
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    test = WImage()
    test.query("Remi Cozot")
    test.show()
    sys.exit(app.exec())