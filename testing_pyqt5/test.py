import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, 
                             QWidget, QVBoxLayout, QHBoxLayout, QGridLayout)
from PyQt5.QtGui import QFont, QPixmap, QIcon 
from PyQt5.QtCore import Qt 


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("My cool first GUI")
        self.setGeometry(0,0,500,500)
        self.setWindowIcon(QIcon("kalego.jpg"))
        
        label = QLabel("Hello", self)
        label.setFont(QFont("Ariel",40))
        label.setGeometry(0,0,500,100)
        label.setStyleSheet("color: plum;"
                            "background-color: indigo;"
                            "font-weight: bold;"
                            "font-style: italic;"
                            "text-decoration: underline;")
        
        #label.setAlignment(Qt.AlignTop) #VERTICALLY top
        #label.setAlignment(Qt.AlignBottom) #VERTICALLY bottom
        # label.setAlignment(Qt.AlignVCenter) #VERTICALLY center
        # label.setAlignment(Qt.AlignRight) #HORIZONTALLY right
        #label.setAlignment(Qt.AlignLeft) #HORIZONTALLY Left
        # label.setAlignment(Qt.AlignHCenter) #HORIZONTALLY center
        label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        
        label2 = QLabel(self)
        label2.setGeometry(50,100,400,400)
        
        pixmap = QPixmap("kalego.jpg")
        label2.setPixmap(pixmap)
        label2.setScaledContents(True)
        
        label2.setGeometry((self.width()-label2.width())//2,
                           self.height()-label2.height(),
                           label2.width(),label2.height())
        
    def initUI(self):
        # central_widget = QWidget()
        # self.setCentralWidget(central_widget)
        
        # label1 = QLabel('#1', self)
        # label2 = QLabel('#2', self)
        # label3 = QLabel('#3', self)
        # label4 = QLabel('#4', self)
        # label5 = QLabel('#5', self)
        
        # label1.setStyleSheet("background-color: pink;")
        # label2.setStyleSheet("background-color: plum;")
        # label3.setStyleSheet("background-color: violet;")
        # label4.setStyleSheet("background-color: indigo;"
        #                      "color:white;")
        # label5.setStyleSheet("background-color: black;"
        #                      "color:white;")
        
        #vert
        # vbox = QVBoxLayout()
        
        # vbox.addWidget(label1)
        # vbox.addWidget(label2)
        # vbox.addWidget(label3)
        # vbox.addWidget(label4)
        # vbox.addWidget(label5)
        
        #horiz
        # hbox = QHBoxLayout()
        
        # hbox.addWidget(label1)
        # hbox.addWidget(label2)
        # hbox.addWidget(label3)
        # hbox.addWidget(label4)
        # hbox.addWidget(label5)
        
        #grid
        # grid = QGridLayout()
        
        # grid.addWidget(label1,0,0)
        # grid.addWidget(label2,0,1)
        # grid.addWidget(label3,1,0)
        # grid.addWidget(label4,1,1)
        # grid.addWidget(label5,2,2)
        
        # central_widget.setLayout(vbox)
        pass
        
        
        
        
    
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()