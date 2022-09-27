from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import math


class Canvas(QWidget):
	stopTrial = pyqtSignal()

	def __init__(self, parent = None):
		QWidget.__init__(self, parent )

#		self.setFocusPolicy(Qt.StrongFocus)
#		self.setFocus(True)
		self.mat_size = 2
		self.state = 0 #attention ; 1 #selection


	def setState(self, b):
		self.state = b
		self.update()

	def set_stimulus(self,l):
		self.selected_target = -1
		self.stimulus = l
		self.mat_size = int( math.sqrt( len(self.stimulus) ) )

	def paintEvent(self, e):
		offset = 30
		h = (self.height() - (self.mat_size+1)*offset ) / self.mat_size
		x_offset =  ( self.width() - ( (h+offset) * self.mat_size - offset)) /2
		p = QPainter(self)

		if self.state == 0: # attention
		
			for i in range(0, self.mat_size):
				for j in range(0, self.mat_size):
					s = self.stimulus[i* self.mat_size + j]
					x = j * (h+offset) + x_offset
					y = i*(h+offset) + offset
					#p.drawRect(x, y, h, h)
					#p.drawText(QPoint(x, y), s)
					img = QImage('./ressources/'+ s + '.png') #TODO

					p.drawImage(QPoint(x + (h-img.width()) / 2 ,y + (h-img.height()) / 2), img)

		else:	#selection
			for i in range(0, self.mat_size):
				for j in range(0, self.mat_size):
					s = self.stimulus[i* self.mat_size + j]
					x = i * (h+offset) + x_offset
					y = j*(h+offset) + offset
					#p.drawRect(x, y, h, h)
					#p.drawText(QPoint(x, y), s)
					img = QImage('./ressources/white-square.png') #TODO

					p.drawImage(QPoint(x + (h-img.width()) / 2 ,y + (h-img.height()) / 2), img)


	def mouseReleaseEvent(self, e):
		if self.state ==1:
			found = False

			offset = 30
			h = (self.height() - (self.mat_size+1)*offset ) / self.mat_size
			x_offset =  ( self.width() - ( (h+offset) * self.mat_size - offset)) /2

			for i in range(0, self.mat_size):
				for j in range(0, self.mat_size):
					x = j * (h+offset) + x_offset
					y = i*(h+offset) + offset
					img = QImage('./ressources/white-square.png') # TODO
					rect = QRect(x + (h-img.width()) / 2, y + (h-img.height()) / 2, img.width(), img.height())
					#print(rect, e.pos() )
					if rect.contains(e.pos() ):
						found = True
						self.selected_target = i * self.mat_size + j
						#print(i * self.mat_size + j)
						self.stopTrial.emit()			

			




