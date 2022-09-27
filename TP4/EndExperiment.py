from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Chart import *
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



class EndExperiment(QWidget):
	def __init__(self, parent = None):
		QWidget.__init__(self, parent )

		self.resize(1200, 1000)

		self.setFocusPolicy(Qt.StrongFocus)
		layout = QVBoxLayout(self)
		thanks_lab = QLabel()
		thanks_lab.setText("Fin de l'experience. Merci pour votre participation")		
		layout.addWidget(thanks_lab)
		

		self.figure = plt.figure( tight_layout=True )
		self.canvas = FigureCanvas( self.figure )
		self.canvas.setSizePolicy( QSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding ) )
		self.toolbar = NavigationToolbar(self.canvas, self )

		quitButton = QPushButton("QUIT", self)
		quitButton.setGeometry(550, 0, 100, 30)
		quitButton.clicked.connect(self.quit)

		#self.l.addWidget( self.toolbar )
		#self.l.addWidget( self.canvas )


		#######################
		# read csv file
		#######################
		#read your csv file and add the header
		#df = pd.read_csv( ... )
		#print(df)
		#

		##################
		# chart
		##################
		self.chart = Chart()
		self.view = QChartView(self.chart)
		self.chart.set_view(self.view)
		layout.addWidget(self.view)

	def quit():
		msg = QMessageBox()
		msg.setText("Do you want to quit")
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		returnValue = msg.exec()
		if (returnValue == QMessageBox.Yes):
			QApplication.quit()