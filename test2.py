import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, 
                             QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton)
from PyQt5.QtGui import QFont, QPixmap, QIcon 
from PyQt5.QtCore import Qt 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("My Book List!")
        self.setGeometry(100,100,1000,625)
        self.setWindowIcon(QIcon("kalego.jpg"))
        
        title = QLabel("My Book List!", self)
        title.setFont(QFont("Ariel",40))
        title.setGeometry(0,0,self.width(),100)
        title.setStyleSheet("color: plum;"
                            "background-color: indigo;"
                            "font-weight: bold;")
        title.hide()
        tst = QLabel('testing',self)
        
        #title.setAlignment(Qt.AlignTop) #VERTICALLY top
        #title.setAlignment(Qt.AlignBottom) #VERTICALLY bottom
        # title.setAlignment(Qt.AlignVCenter) #VERTICALLY center
        # title.setAlignment(Qt.AlignRight) #HORIZONTALLY right
        #title.setAlignment(Qt.AlignLeft) #HORIZONTALLY Left
        # title.setAlignment(Qt.AlignHCenter) #HORIZONTALLY center
        title.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        
        label2 = QLabel(self)
        label2.setGeometry(50,100,400,400)
        
        pixmap = QPixmap("kalego.jpg")
        label2.setPixmap(pixmap)
        label2.setScaledContents(True)
        
        label2.setGeometry((self.width()-label2.width())//2,
                           self.height()-label2.height(),
                           label2.width(),label2.height())
        
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        label1 = QLabel('#1', self)
        label2 = QLabel('#2', self)
        label3 = QLabel('#3', self)
        label4 = QLabel('#4', self)
        label5 = QLabel('#5', self)
        
        label1.setStyleSheet("background-color: pink;")
        label2.setStyleSheet("background-color: plum;")
        label3.setStyleSheet("background-color: violet;")
        label4.setStyleSheet("background-color: indigo;"
                             "color:white;")
        label5.setStyleSheet("background-color: black;"
                             "color:white;")
        
        #vert
        vbox = QVBoxLayout()
        
        vbox.addWidget(label1)
        label1.hide()
        vbox.addWidget(label2)
        vbox.addWidget(label3)
        vbox.addWidget(label4)
        vbox.addWidget(label5)
        
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
        
        central_widget.setLayout(vbox)
        pass
class data_proccessing():
    def __init__(self, title):
        self.title = title 
        self.tbr = []
        self.current = []
        self.finished = []
    def get_input(self):
        x = input("book name: ")
        y = input("author name: ")
        z = input("excitement level (1-5): ")
        if z.isdigit() and 1<=int(z)<=5:
            z = int(z)
        self.tbr.append({"name":x,"aut":y,"exc":z})
        

    
        
        
    
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()