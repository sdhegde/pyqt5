import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

fpath = "new.png"

class rect(QWidget):
	def __init__(self):
		super().__init__()
		#self.setGeometry(30, 30, 700, 500)
		global fpath
		self.path = fpath
		self.begin = QPoint()
		self.end = QPoint()
	
	def paintEvent(self, event):
		painter = QPainter(self)		
		pen = QPen(Qt.red, 3)
		painter.setPen(pen)
		painter.drawRect(12,21,76,19)
		
		br = QBrush(QColor(100, 10, 10, 40))  
		painter.setBrush(br)   
		painter.drawRect(QRect(self.begin, self.end)) 

	def mousePressEvent(self, event):
		self.begin = event.pos()
		self.end = event.pos()
		self.update()

	def mouseMoveEvent(self, event):
		self.end = event.pos()
		self.update()

	def mouseReleaseEvent(self, event):
		#self.begin = event.pos()
		self.end = event.pos()
		self.update()

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QStackedLayout()


        #Background area test
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("new.png"))
        self.background.show()
        #self.background.setAutoFillBackground(True)

        #Setup text area for clock
        newfont = QFont("Consolas",120, QFont.Bold)
        self.lbl1 = QLabel()
        self.lbl1.setAlignment(Qt.AlignCenter)
        self.lbl1.setFont(newfont)
        self.lbl1.setWindowFlags(Qt.FramelessWindowHint)
        self.lbl1.setAttribute(Qt.WA_TranslucentBackground)

        #Timer to refresh clock
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()

        #layout area for widgets

        layout.addWidget(self.background)
        layout.addWidget(self.lbl1)
        layout.setCurrentIndex(1)
        layout.setStackingMode(QStackedLayout.StackAll)
        self.setLayout(layout)
        self.setGeometry(300,300,250,150)
        self.show()

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]
        self.lbl1.setText(text)

class Example1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        layout = QStackedLayout()

        #Background area test
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("new.png"))
        #self.background.show()
        #self.background.setAutoFillBackground(True)
        
        r = rect()
        
        #layout area for widgets
        layout.addWidget(self.background)
        layout.addWidget(r)
        layout.setCurrentIndex(1)
        layout.setStackingMode(QStackedLayout.StackAll)
        self.setLayout(layout)
        #self.setGeometry(300,300,250,150)
        #self.show()

    def showTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]
        self.lbl1.setText(text)

class sdh(QMainWindow):
		def __init__(self):
				super().__init__()
				ex1=Example1()
				scrollArea = QScrollArea()
				scrollArea.setWidget(ex1)
				self.setCentralWidget(scrollArea)
		
		
		
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #ex = Example1()
    #ex.show()
    sdh = sdh()
    sdh.show()
    sys.exit(app.exec_())
