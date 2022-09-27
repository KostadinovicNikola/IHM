import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Canvas import *
import resources
import pickle


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        print("init mainwindow")
        self.resize(600, 500)

        self.sure_to_close = False

        self.brushColor = Qt.black
        self.penColor = Qt.red
        self.selectedShape = "rect"
        self.penWidth = 2

        bar = self.menuBar()

        fileMenu = bar.addMenu("File")

        quit_icon = QIcon(":/icons/quit.png")
        quit_action = QAction(quit_icon, "Fermer", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.quit)

        open_icon = QIcon(":/icons/open.png")
        open_action = QAction(open_icon, "Ouvrir", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open)

        save_icon = QIcon(":/icons/save.png")
        save_action = QAction(save_icon, "Sauvegarder", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save)

        fileMenu.addAction(open_action)
        fileMenu.addAction(save_action)
        fileMenu.addAction(quit_action)

        fileToolBar = QToolBar("File")
        fileToolBar.addAction(open_action)
        fileToolBar.addAction(save_action)
        fileToolBar.addAction(quit_action)

        brushMenu = bar.addMenu("Brush")

        colorMenu = bar.addMenu("Color")
        actPen = brushMenu.addAction(QIcon(":/icons/pen.png"), "&Pen color")
        actPen.setShortcut("Ctrl+P")
        actPen.triggered.connect(self.change_color)

        actBrush = brushMenu.addAction(
            QIcon(":/icons/brush.png"), "&Brush color")
        actBrush.setShortcut("Ctrl+B")
        actBrush.triggered.connect(self.change_color)

        actPlus = brushMenu.addAction(
            QIcon(":/icons/plus.png"), "&Increase pen width")
        actPlus.triggered.connect(self.change_width)
        actMinus = brushMenu.addAction(
            QIcon(":/icons/minus.png"), "&Decrease pen width")
        actMinus.triggered.connect(self.change_width)

        colorToolBar = QToolBar("Color")
        self.addToolBar(colorToolBar)
        colorToolBar.addAction(actPen)
        colorToolBar.addAction(actBrush)
        colorToolBar.addAction(actPlus)
        colorToolBar.addAction(actMinus)

        shapeMenu = bar.addMenu("Shape")
        actRectangle = brushMenu.addAction(
            QIcon(":/icons/rectangle.png"), "&Rectangle")
        actRectangle.triggered.connect(self.change_shape)
        actEllipse = brushMenu.addAction(
            QIcon(":/icons/ellipse.png"), "&Ellipse")
        actEllipse.triggered.connect(self.change_shape)
        actFree = brushMenu.addAction(
            QIcon(":/icons/free.png"), "&Free drawing")
        actFree.triggered.connect(self.change_shape)
        actUndo = brushMenu.addAction(QIcon(":/icons/undo.png"), "&Undo")
        actUndo.setShortcut("Ctrl+Z")
        actUndo.triggered.connect(self.undo)

        shapeToolBar = QToolBar("Shape")
        self.addToolBar(shapeToolBar)
        shapeToolBar.addAction(actRectangle)
        shapeToolBar.addAction(actEllipse)
        shapeToolBar.addAction(actFree)
        shapeToolBar.addAction(actUndo)

        modeMenu = bar.addMenu("Mode")
        actMove = modeMenu.addAction(
            QIcon(":/icons/move.png"), "&Move", self.change_mode)
        actDraw = modeMenu.addAction(
            QIcon(":/icons/draw.png"), "&Draw", self.change_mode)
        actSelect = modeMenu.addAction(
            QIcon(":/icons/select.png"), "&Select", self.change_mode)
        actZoomIn = modeMenu.addAction(
            QIcon(":/icons/zoom-in.png"), "&Zoom-in", self.change_mode)
        actZoomOut = modeMenu.addAction(
            QIcon(":/icons/zoom-out.png"), "&Zoom-out", self.change_mode)

        modeToolBar = QToolBar("Navigation")
        self.addToolBar(modeToolBar)
        modeToolBar.addAction(actMove)
        modeToolBar.addAction(actDraw)
        modeToolBar.addAction(actSelect)
        modeToolBar.addAction(actZoomIn)
        modeToolBar.addAction(actZoomOut)

        self.addToolBar(fileToolBar)

        self.colorDialog = QColorDialog(self)

        self.canva = Canvas([], [], [], [], parent=self)
        self.textEdit = QTextEdit(self)

        self.change_container()

        self.dialog_fichier = QFileDialog()
        # file dialog
        self.dialog_fichier.setFileMode(QFileDialog.AnyFile)

        #warning_icon = QIcon("warning.png")
        self.quit_warning = QMessageBox(
            QMessageBox.Warning, "Attention", "Voulez vous vraiment quitter?")
        self.quit_warning.setStandardButtons(
            QMessageBox.Ok | QMessageBox.Cancel)

    def change_container(self):
        v_layout = QVBoxLayout()
        self.canva.current_color = self.brushColor
        self.canva.current_pen_color = self.penColor
        self.canva.current_width = self.penWidth
        self.canva.current_shape = self.selectedShape
        v_layout.addWidget(self.canva)
        v_layout.addWidget(self.textEdit)
        container = QWidget()
        container.setLayout(v_layout)
        self.setCentralWidget(container)

    ##############
    ### SLOTS ###

    def change_color(self):
        if(self.sender().text() == "&Brush color"):
            color = self.colorDialog.getColor()
            if(self.canva.mod != "select"):
                self.brushColor = color
                self.change_container()
            else:
                self.canva.change_shape_color(color)
        if(self.sender().text() == "&Pen color"):
            color = self.colorDialog.getColor()
            if(self.canva.mod != "select"):
                self.penColor = color
                self.change_container()
            else:
                self.canva.change_shape_contour(color)

    def change_width(self):
        if(self.sender().text() == "&Increase pen width"):
            if(self.canva.mod != "select"):
                self.penWidth += 1
                self.change_container()
            else:
                self.canva.decrease_shape_pen_width()
        elif(self.sender().text() == "&Decrease pen width"):
            if(self.canva.mod != "select"):
                if(self.penWidth > 0):
                    self.penWidth -= 1
                    self.change_container()
            else:
                self.canva.increase_shape_pen_width()

    def change_shape(self):
        if(self.sender().text() == "&Ellipse"):
            if(self.canva.mod != "select"):
                self.canva.mod = "draw"
                self.selectedShape = "ellipse"
                self.change_container()
            else:
                self.canva.set_shape_ellipse()
        elif(self.sender().text() == "&Rectangle"):
            if(self.canva.mod != "select"):
                self.canva.mod = "draw"
                self.selectedShape = "rect"
                self.change_container()
            else:
                self.canva.set_shape_rect()
        elif(self.sender().text() == "&Free drawing"):
            self.canva.mod = "draw"
            self.selectedShape = "polygon"
            self.change_container()

    def undo(self):
        self.canva.remove_last_shape()

    def change_mode(self):
        if(self.sender().text() == "&Move"):
            self.log_action("Mode: move")
            self.canva.mod = "move"
            self.canva.black_layer = 0

        elif(self.sender().text() == "&Draw"):
            self.log_action("Mode: draw")
            self.canva.mod = "draw"
            self.canva.black_layer = 0

        elif(self.sender().text() == "&Select"):
            self.log_action("Mode: select")
            self.canva.mod = "select"
        elif(self.sender().text() == "&Zoom-in"):
            self.log_action("Mode: zoom in")
            self.canva.mod = "zoom-in"
            self.canva.black_layer = 0
            if(self.canva.scaleLevel != 4):
                self.canva.scaleLevel += 1
            self.canva.update()
        elif(self.sender().text() == "&Zoom-out"):
            self.log_action("Mode: zoom out")
            if(self.canva.scaleLevel != -4):
                self.canva.scaleLevel -= 1
            self.canva.update()

    def select(self):
        self.log_action("Mode: select")

    def log_action(self, str):
        content = self.textEdit.toPlainText()
        self.textEdit.setPlainText(content + "\n" + str)

    def open(self, e):
        file = self.dialog_fichier.getOpenFileName(
            self, "Open File", "./", "Images (*.png *.xpm *.jpg);;Text files (*.txt *.py);;XML files (*.xml *.qrc);;HTML files (*.html);;All files (*.*)")
        if(file[0]):
            with open(file[0], "rb") as f:
                if(file[1] == "HTML files (*.html)"):
                    self.text_edit.setHtml(f.read())
                elif(file[1] == "Text files (*.txt *.py)"):
                    self.text_edit.setPlainText(f.read())
                else:
                    data = pickle.load(f)
                    self.canva = Canvas(data["color"], data["shape"], data["pen_color"],
                                        data["pen_width"], data["topLeft"], data["botRight"], data["polygons"], self)
                    self.canva.update()

    def save(self, e):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "", "All Files (*);;Text Files (*.txt);;Pickle Files (*.pkl)", options=options)
        if(fileName):
            try:
                file = open(fileName, 'wb')
            except FileNotFoundError:
                self.close()
            if(file):
                pickle.dump({
                    "polygons": self.canva.polygons,
                    "topLeft": self.canva.topLeft,
                    "botRight": self.canva.botRight,
                    "color": self.canva.color,
                    "shape": self.canva.shape,
                    "pen_color": self.canva.pen_color,
                    "pen_width": self.canva.pen_width
                }, file)

    def quit(self):
        msg = QMessageBox()
        msg.setText("Do you want to quit")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        msgS = QMessageBox()
        msgS.setText("Do you want to save")
        msgS.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = msg.exec()
        if (returnValue == QMessageBox.Yes):
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
            saveValue = msgS.exec()
            if (saveValue == QMessageBox.Yes):
                self.saveFile()

            QApplication.quit()

    # def quit(self, e):
    #     btn = self.quit_warning.exec()
    #     if(btn == QMessageBox.Ok):
    #         self.save(e)
    #         self.sure_to_close = True
    #         self.close()
    #     else:
    #         e.ignore()

    # def closeEvent(self, event):
    #     if(self.sure_to_close):
    #         event.accept()
    #     else:
    #         self.quit(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()
