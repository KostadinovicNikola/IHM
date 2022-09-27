from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class InterTrial(QWidget):
	startTrial = pyqtSignal()	
	def __init__(self, parent = None):
		QWidget.__init__(self, parent )
 
		#self.setFocusPolicy(Qt.StrongFocus)
		layout = QVBoxLayout(self)
		instructions_lab = QLabel()
		instructions_lab.setText("Une scene avec plusieurs formes va etre affichee a l'ecran. \n Identifier visuellement la seule forme qui est differente de toutes les autres formes. \n Des que vous avez identifie cette forme, appuyez sur la barre d'espace aussi vite que possible. \n Cliquez ensuite sur la position de cette forme. \n \n Appuyez sur la barre d'espace pour commencer")
		self.progress_lab = QLabel()
		self.practice_lab = QLabel ()
		
		layout.addWidget(self.practice_lab)
		layout.addWidget(instructions_lab)
		layout.addWidget(self.progress_lab)

	
	def set_block_trial(self, block_id, trial_id):
		#self.progress_lab.setText("block: " + block_id + " Trial: " + trial_id)
		self.progress_lab.setText("block: " + block_id + " Trial: " + trial_id)


	###################################
	def set_practice (self, b):
		if b:
			self.practice_lab.setText("Ceci est un entrianement\n")
		else:
			self.practice_lab.setText(" ==== VOUS ETES EN PHASE DE TEST ====")
		
		
