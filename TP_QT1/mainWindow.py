import sys
import pickle 

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        print("constructeur de la class MainWindow")
        super().__init__()
        self.resize(300, 400)
        self.initUI()
        self.saved = False

    def initUI(self):
        bar = self.menuBar()
        self.statusBar()
        bar.setNativeMenuBar(False)
        fileMenu = bar.addMenu("Fichier")

        openAction = QAction(QIcon("./open.png"), '&Open', self)
        openAction.setShortcut(QKeySequence("Ctrl+O"))
        openAction.setToolTip("Open")
        openAction.setStatusTip("Open a file")
        openAction.triggered.connect(self.openFile)

        fileMenu.addAction(openAction)

        newAction = QAction(QIcon("./new.png"), '&New', self)
        newAction.setShortcut(QKeySequence("Ctrl+N"))
        newAction.setToolTip("Create a new file ")
        newAction.setStatusTip("Create a file")
        newAction.triggered.connect(self.newFile)

        cutAction = QAction(QIcon("./cut.png"), '&Cut', self)
        cutAction.setShortcut(QKeySequence("Ctrl+X"))
        cutAction.setToolTip("Cut")
        cutAction.setStatusTip("Cut")
        cutAction.triggered.connect(self.cut)

        copyAction = QAction(QIcon("./copy.png"), '&Copy', self)
        copyAction.setShortcut(QKeySequence("Ctrl+C"))
        copyAction.setToolTip("Copy")
        copyAction.setStatusTip("Copy")
        copyAction.triggered.connect(self.copy)

        pasteAction = QAction(QIcon("./paste.png"), '&Paste', self)
        pasteAction.setShortcut(QKeySequence("Ctrl+V"))
        pasteAction.setToolTip("Paste")
        pasteAction.setStatusTip("Paste")
        pasteAction.triggered.connect(self.paste)

        saveAction = QAction(QIcon("./save.png"), '&Save', self)
        saveAction.setShortcut(QKeySequence("Ctrl+S"))
        saveAction.setToolTip("Save")
        saveAction.setStatusTip("Save as a file")
        saveAction.triggered.connect(self.saveFile)

        fileMenu.addAction(saveAction)

        exitAction = QAction(QIcon("./quit.png"), '&Exit', self)
        exitAction.setShortcut(QKeySequence("Ctrl+Q"))
        exitAction.setToolTip("Exit Application")
        exitAction.setStatusTip("Exit Application")
        exitAction.triggered.connect(self.quitApp)

        fileMenu.addAction(exitAction)

        self.text = QTextEdit(self)
        self.saved = False
        self.setCentralWidget(self.text)

        self.setWindowTitle("PyQt5 test")
        self.show()

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, fileExt = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "Text Files (*.txt);; HTML files (*.html);;Pickle Files (*.pkl) ;; All Files (*)", options=options)
        file = open(filePath, 'r')
        text = file.read()
        if fileExt != "HTML files (*.html)":
            if (fileExt == "Pickle Files (*.pkl)"):
                pickle.load(file)
            self.centralWidget().setPlainText(text)
        else:
            self.centralWidget().setHtml(file.read())
        file.close()
        print(text)
        print(filePath)
        print(fileExt)

    def newFile(self):
        print("This is a new File")

    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, fileExt = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "", "All Files (*);;Text Files (*.txt);;Pickle Files (*.pkl)", options=options)
        file = open(fileName, 'w')
        text = self.centralWidget().toPlainText()
        file.write(text)
        self.saved = True
        if (fileExt == "Pickle Files (*.pkl)"):
                pickle.dump(text, file)
        if fileName:
            print(fileName)

    def cut(self):
        print("cut the text")

    def copy(self):
        print("copy the text")

    def paste(self):
        print("past the text")

    def quitApp(self):
        msg = QMessageBox()
        msg.setText("Do you want to quit")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        msgS = QMessageBox()
        msgS.setText("Do you want to save")
        msgS.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = msg.exec()
        if (returnValue == QMessageBox.Yes):
            if (self.saved == False):
                saveValue = msgS.exec()
                if saveValue == QMessageBox.Yes:
                    self.saveFile()
            QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        msg = QMessageBox()
        msg.setText("Do you want to quit")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        msgS = QMessageBox()
        msgS.setText("Do you want to save")
        msgS.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = msg.exec()
        
        if (returnValue == QMessageBox.Yes):
            if (self.saved == False):
                saveValue = msgS.exec()
                if saveValue == QMessageBox.Yes:
                    self.saveFile()
            
            QApplication.quit()


def main(args):
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)
