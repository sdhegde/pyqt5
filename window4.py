import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import csv

class ImageViewer(QWidget):
	def __init__(self, tableObj, rowIndx, parent=None):
		super(ImageViewer, self).__init__(parent)
		#self.setGeometry(30, 30, 700, 500)
		self.tableObj = tableObj
		self.rowIndx = rowIndx
		self.begin = QPoint()
		self.end = QPoint()		
	
	def paintEvent(self, event):		
		painter = QPainter(self)
		br = QBrush(QColor(100, 0, 0, 40))  
		painter.setBrush(br)   
		painter.drawRect(QRect(self.begin, self.end)) 
				
		rowList = [i for i in range(self.tableObj.rowCount()) if i != self.rowIndx]
		if(self.rowIndx >= 0):
			pen = QPen(Qt.green, 2)
			painter.setPen(pen)
			x1 = int(self.tableObj.data(self.tableObj.index(self.rowIndx, 0)))
			y1 = int(self.tableObj.data(self.tableObj.index(self.rowIndx, 1)))
			x2 = int(self.tableObj.data(self.tableObj.index(self.rowIndx, 2)))
			y2 = int(self.tableObj.data(self.tableObj.index(self.rowIndx, 3)))
			x3 = int(self.tableObj.data(self.tableObj.index(self.rowIndx, 4)))
			y3 = int(self.tableObj.data(self.tableObj.index(self.rowIndx, 5)))
			x4 = int(self.tableObj.data(self.tableObj.index(self.rowIndx, 6)))
			y4 = int(self.tableObj.data(self.tableObj.index(self.rowIndx, 7)))
			painter.drawRect(x1,y1,x2-x1,y4-y1)
			
		for rowNumber in rowList:
			pen = QPen(Qt.red, 2)
			painter.setPen(pen)
			x1 = int(self.tableObj.data(self.tableObj.index(rowNumber, 0)))
			y1 = int(self.tableObj.data(self.tableObj.index(rowNumber, 1)))
			x2 = int(self.tableObj.data(self.tableObj.index(rowNumber, 2)))
			y2 = int(self.tableObj.data(self.tableObj.index(rowNumber, 3)))
			x3 = int(self.tableObj.data(self.tableObj.index(rowNumber, 4)))
			y3 = int(self.tableObj.data(self.tableObj.index(rowNumber, 5)))
			x4 = int(self.tableObj.data(self.tableObj.index(rowNumber, 6)))
			y4 = int(self.tableObj.data(self.tableObj.index(rowNumber, 7)))
			painter.drawRect(x1,y1,x2-x1,y4-y1)
	
	def mousePressEvent(self, event):
		self.begin = event.pos()
		self.end = event.pos()
		self.update()

	def mouseMoveEvent(self, event):
		self.end = event.pos()
		self.update()

	def mouseReleaseEvent(self, event):
		self.end = event.pos()		
		x1 = QStandardItem((str(self.begin.x())))
		y1 = QStandardItem((str(self.begin.y())))
		x2 = QStandardItem((str(self.end.x())))
		y2 = QStandardItem((str(self.begin.y())))
		x3 = QStandardItem((str(self.end.x())))
		y3 = QStandardItem((str(self.end.y())))
		x4 = QStandardItem((str(self.begin.x())))
		y4 = QStandardItem((str(self.end.y())))		
		newRow = [x1,y1,x2,y2,x3,y3,x4,y4]
		self.tableObj.appendRow(newRow)
		self.update()

	
class MainWindow(QMainWindow, QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		loadUi('window.ui', self)		
		
		self.openAct.triggered.connect(self.openCsv)
		self.saveAct.triggered.connect(self.saveCsv)
		self.exitAct.triggered.connect(self.close) 
		self.pushButton1.clicked.connect(self.delete)
		
		self.model = QStandardItemModel(self)
		self.tableView = QTableView(self)
		self.tableView.setModel(self.model)
		self.tableView.horizontalHeader().setStretchLastSection(True)
		self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows);
		#self.tableView.clicked.connect(self.onSelection)
		self.tableView.selectionModel().selectionChanged.connect(self.onSelection1) #alternate way
		
		#self.layoutVertical = QVBoxLayout(self)
		#self.layoutVertical.addWidget(self.tableView)		
		self.scrollArea1.setWidget(self.tableView)							
		
	def delete(self, index):
		indexes = self.tableView.selectionModel().selectedRows()
		for index in sorted(indexes):
			print('Row %d is selected' % index.row())
			self.model.removeRows(index.row(),1)    
			
			pre, ext = os.path.splitext(self.fileName)	
			"""imageViewer = ImageViewer(pre+".png", self.model, -1)
			self.scrollArea2.setWidget(imageViewer)
			self.update()"""
			self.drawAllRect(self.imgPath, -1)
	
	def drawAllRect(self, path, indx):
		"""imageViewer = ImageViewer(pre+".png", self.model, -1)
		self.scrollArea2.setWidget(imageViewer)
		self.update()"""
		self.qw = QWidget()
		layout = QStackedLayout()
		#Background area test
		self.background = QLabel(self)
		self.background.setPixmap(QPixmap(path))
		#self.background.show()
		#self.background.setAutoFillBackground(True)
		
		r = ImageViewer(self.model, indx)
		
		#layout area for widgets
		layout.addWidget(self.background)
		layout.addWidget(r)
		layout.setCurrentIndex(1)
		layout.setStackingMode(QStackedLayout.StackAll)
		self.qw.setLayout(layout)
		self.scrollArea2.setWidget(self.qw)
		#self.setCentralWidget(self.scrollArea2)
		self.model.setHorizontalHeaderLabels(["x1","y1","x2","y2","x3","y3","x4","y4","word"])

	def openCsv(self):
		self.fileName, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())		
		self.model.clear()
		with open(self.fileName, "r") as fileInput:
			for row in csv.reader(fileInput):		 
				items = [
						QStandardItem(field)
						for field in row
				]
				self.model.appendRow(items)
				
		pre, ext = os.path.splitext(self.fileName)
		self.imgPath = pre+".jpg"
		self.drawAllRect(self.imgPath, -1)				
		
	
	def saveCsv(self):
		with open(self.fileName, "w") as fileOutput:
			writer = csv.writer(fileOutput)
			for rowNumber in range(self.model.rowCount()):
				fields = [
						self.model.data(
								self.model.index(rowNumber, columnNumber),
								Qt.DisplayRole
						)
						for columnNumber in range(self.model.columnCount())
				]
				writer.writerow(fields)
	
	"""def onSelection(self, index):
		indexes = self.tableView.selectionModel().selectedRows()
		for index in sorted(indexes):
			print('Row %d is selected' % index.row())
			pre, ext = os.path.splitext(self.fileName)
			print(pre+".png")				
			imageViewer = ImageViewer(pre+".png", self.model, index.row())
			self.scrollArea2.setWidget(imageViewer)
			self.update()"""
			
	#alternate way to onSelection()
	def onSelection1(self):
		indexes = self.tableView.selectionModel().selectedRows()
		for index in sorted(indexes):
			pre, ext = os.path.splitext(self.fileName)
			"""imageViewer = ImageViewer(pre+".png", self.model, index.row())
			self.scrollArea2.setWidget(imageViewer)
			self.update()"""
			self.drawAllRect(self.imgPath, index.row())
	


if __name__ == '__main__':	
	app = QApplication(sys.argv)
	mainWindow = MainWindow()
	mainWindow.show()
	#mainWindow.showMaximized() 
	sys.exit(app.exec_())
