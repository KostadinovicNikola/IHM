from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Canvas(QWidget) :

    def __init__(self,  fill_color,shape,pen_color,pen_width, topLeft = [], botRight = [], polygons = [],parent = None,
                    current_color=Qt.black, current_pen_color = Qt.red, current_shape = "rect", current_width=1):
        super().__init__(parent)
        self.setMinimumSize(550,450)
        #list of list of QPoints
        self.polygons =polygons
        self.topLeft =topLeft
        self.botRight =botRight
        self.current_color = current_color
        self.current_pen_color = current_pen_color
        self.current_shape = current_shape
        self.current_width = current_width
        self.color = fill_color
        self.pen_color = pen_color
        self.shape = shape
        self.pen_width = pen_width
        self.initial_pos = (0,0)
        self.current_cursor_pos = (0,0)
        self.mod = "draw"
        self.p = parent
        self.selected_existant_shape=None
        self.selected_existant_polygon = None
        self.selected_shapes = []
        self.scaleLevel = 0
        self.scale_levels = {
            -4 : (0.25, 0.25),
            -3 : (0.5,0.5),
            -2 : (2/3, 2/3),
            -1 : (0.75,0.75),
            0 : (1,1),
            1 : (1.25, 1.25),
            2 : (1.5, 1.5),
            3 : (1.75, 1.75),
            4 : (2,2)
        }
        self.black_layer = 0
        self.selection_polygon = None
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.scale(self.scale_levels[self.scaleLevel][0], self.scale_levels[self.scaleLevel][1])
        if(self.topLeft and self.botRight and self.mod == "draw"):
            self.draw_all_shapes(painter)
        elif(self.mod=="move"):
            painter.translate(
                self.current_cursor_pos[0] - self.initial_pos[0],
                self.current_cursor_pos[1] - self.initial_pos[1]
                )
            self.draw_all_shapes(painter)
        elif(self.mod=="select"):
                self.draw_all_shapes(painter)
                if(self.selected_shapes or self.selected_existant_polygon):
                    if(not(self.black_layer)):
                        self.black_layer = 1
                        self.paint_black_layer(painter)
                    if(self.selected_shapes):
                        for i in self.selected_shapes:
                            self.draw_shape(painter, i, 0.5)
                    else:
                        self.draw_polygon(painter, self.selected_existant_polygon, 0.5)
                elif(self.selection_polygon):
                    self.draw_selection_polygon(painter)
        else:
            self.draw_all_shapes(painter)


    def mousePressEvent(self, event):
        if(self.mod=="draw"):
            if(self.current_shape !="polygon"):
                self.topLeft.append([event.pos().x(), event.pos().y()])
            else:
                self.polygons.append((QPolygon([QPoint(event.pos().x(), event.pos().y())]),self.current_color, self.current_pen_color, self.current_width))
        elif(self.mod=="move"):
            self.initial_pos = event.pos().x(), event.pos().y()
        elif(self.mod=="select"):
            shape = None
            in_shape = False
            self.selected_shapes = []
            for i in range(len(self.botRight)-1, 0, -1):
                if(self.shape[i]=="rect"):
                    shape = QRect(self.topLeft[i-1][0], self.topLeft[i-1][1], self.botRight[i-1][0]- self.topLeft[i-1][0], self.botRight[i-1][1]-self.topLeft[i-1][1])
                elif(self.shape[i]=="ellipse"):
                    shape = QRect(self.topLeft[i-1][0], self.topLeft[i-1][1], self.botRight[i-1][0]- self.topLeft[i-1][0], self.botRight[i-1][1]-self.topLeft[i-1][1])
                    shape = QRegion(shape, QRegion.Ellipse)
                if shape.contains(event.pos()):
                    self.selected_shapes = [i-1]
                    in_shape = True
                    break
            if(not(in_shape)):
                self.selected_shapes = []
                for i in range(len(self.polygons)-1, 0, -1):
                    shape = self.polygons[i][0]
                    if shape.contains(event.pos()):
                        self.selected_existant_polygon = i-1
                        in_shape = True
                        break
            if(not(in_shape)):
                self.selected_existant_polygon = None
                self.selection_polygon = QPolygon([QPoint(event.pos().x(), event.pos().y())])
            self.update()

    def mouseMoveEvent(self, event):
        if(self.mod == "draw"):
            if(self.current_shape !='polygon'):
                if(len(self.botRight)):
                    self.botRight[len(self.botRight)-1] = ([event.pos().x(), event.pos().y()])
                    self.color[len(self.color)-1] = self.current_color
                    self.shape[len(self.shape)-1] = self.current_shape
                    self.pen_color[len(self.pen_color)-1] = self.current_pen_color
                    self.pen_width[len(self.pen_width)-1] = self.current_width
                else:
                    self.botRight.append((event.pos().x(), event.pos().y()))
                    self.color.append(self.current_color)
                    self.shape.append(self.current_shape)
                    self.pen_color.append(self.current_pen_color)
                    self.pen_width.append(self.current_width)
            else:
                points = []
                for i in range(self.polygons[len(self.polygons)-1][0].size()):
                    points.append(self.polygons[len(self.polygons)-1][0].point(i))
                points.append(QPoint(event.pos().x(), event.pos().y()))
                self.polygons[len(self.polygons)-1] = (QPolygon(points, ),self.current_color, self.current_pen_color, self.current_width)

        elif(self.mod == "move"):
            self.current_cursor_pos = event.pos().x(), event.pos().y()
        elif(self.mod == "select"):
            points = []
            for i in range(self.selection_polygon.size()):
                points.append(self.selection_polygon.point(i))
            points.append(QPoint(event.pos().x(), event.pos().y()))
            self.selection_polygon = QPolygon(points)

        self.update()


    def mouseReleaseEvent(self, event):
        if(self.mod == "draw"):
            if(self.current_shape != "polygon"):
                self.botRight.append((event.pos().x(), event.pos().y()))
                self.color.append(self.current_color)
                self.shape.append(self.current_shape)
                self.pen_color.append(self.current_pen_color)
                self.pen_width.append(self.current_width)
                self.p.log_action(
                    "added %s with color %s contour with color %s and width %s at position x:%d y:%d with width = %d and length = %d"%(
                        self.current_shape,
                        self.current_color,
                        self.current_pen_color,
                        self.current_width,
                        self.topLeft[len(self.topLeft)-1][0],
                        self.topLeft[len(self.topLeft)-1][1],
                        self.botRight[len(self.botRight)-1][0] - self.topLeft[len(self.topLeft)-1][0],
                        self.botRight[len(self.botRight)-1][0] - self.topLeft[len(self.topLeft)-1][1]
                    )
                )
            self.update()
        elif(self.mod == "move"):
            self.current_cursor_pos = event.pos().x(), event.pos().y()
            for i in range(len(self.topLeft)):
                self.topLeft[i][0] += self.current_cursor_pos[0] - self.initial_pos[0]
                self.botRight[i][0] += self.current_cursor_pos[0] - self.initial_pos[0]
                self.topLeft[i][1] += self.current_cursor_pos[1] - self.initial_pos[1]
                self.botRight[i][1] += self.current_cursor_pos[1] - self.initial_pos[1]
            self.p.log_action("moved canva by x:%d y:%d"%(self.current_cursor_pos[0] - self.initial_pos[0],self.current_cursor_pos[1] - self.initial_pos[1]))
        elif(self.mod == "select" and not(self.selected_shapes)):
            shape = None
            in_shape = False
            for i in range(len(self.botRight)-1, 0, -1):
                if(self.shape[i]=="rect"):
                    shape = QRect(self.topLeft[i-1][0], self.topLeft[i-1][1], self.botRight[i-1][0]- self.topLeft[i-1][0], self.botRight[i-1][1]-self.topLeft[i-1][1])
                elif(self.shape[i]=="ellipse"):
                    shape = QRect(self.topLeft[i-1][0], self.topLeft[i-1][1], self.botRight[i-1][0]- self.topLeft[i-1][0], self.botRight[i-1][1]-self.topLeft[i-1][1])
                    shape = QRegion(shape, QRegion.Ellipse)
                if QRegion(self.selection_polygon).intersects(QRegion(shape)):
                    self.selected_shapes.append(i-1)
                    in_shape = True
            self.selection_polygon = None
            self.update()
    def remove_last_shape(self):
        if(len(self.botRight) and len(self.topLeft)):
            self.topLeft.pop()
            self.botRight.pop()
            self.color.pop()
            self.shape.pop()
            self.pen_color.pop()
            self.pen_width.pop()
            self.update()

    def draw_all_shapes(self, painter):
        for i in range(len(self.topLeft)):
            self.draw_shape(painter, i)
        for i in range(len(self.polygons)):
            self.p.log_action("polygon with %d points drawn"%(self.polygons[i][0].size()))
            self.draw_polygon(painter, i)

    def draw_polygon(self,painter,index,opacity=1):
        painter.setOpacity(opacity)
        painter.setBrush(self.polygons[index][1])
        pen = QPen(self.polygons[index][2]) # instancier un pen
        pen.setWidth(self.polygons[index][3])
        painter.setPen(pen)
        painter.drawPolygon(self.polygons[index][0])

    def paint_black_layer(self,painter):
        painter.setBrush(Qt.black)
        painter.setOpacity(0.7)
        painter.drawRect(0,0, self.width(), self.height())

    def draw_shape(self, painter, index, opacity = 1):
        scale = 1
        painter.setBrush(self.color[index])
        painter.setOpacity(opacity)
        pen = QPen(self.pen_color[index]) # instancier un pen
        pen.setWidth(self.pen_width[index])
        painter.setPen(pen)
        if(self.shape[index]=="rect"):
            shape = QRect(self.topLeft[index][0], self.topLeft[index][1], (self.botRight[index][0]- self.topLeft[index][0])*scale, (self.botRight[index][1]-self.topLeft[index][1])*scale)
            painter.drawRect(shape)
        elif(self.shape[index]=="ellipse"):
            painter.drawEllipse(self.topLeft[index][0], self.topLeft[index][1], (self.botRight[index][0]- self.topLeft[index][0])*scale, (self.botRight[index][1]-self.topLeft[index][1])*scale)

    def draw_selection_polygon(self,painter):
        brush = QBrush()
        brush.setColor(QColor(0,0,0,0))
        painter.setBrush(brush)
        pen = QPen(Qt.black) # instancier un pen
        pen.setWidth(2)
        pen.setStyle(Qt.DashLine);
        painter.setPen(pen)
        painter.drawPolygon(self.selection_polygon)


    def change_shape_color(self, color):
        if(self.selected_shapes):
            for i in self.selected_shapes:
                self.color[i] = color
            self.update()

        elif(self.selected_existant_polygon):
            self.polygons[self.selected_existant_polygon][1] = color
            self.update()

    def change_shape_contour(self, color):
        if(self.selected_shapes):
            for i in self.selected_shapes:
                self.pen_color[i] = color
            self.update()
        elif(self.selected_existant_polygon):
            self.polygons[self.selected_existant_polygon][2] = color
            self.update()

    def increase_shape_pen_width(self):
        if(self.selected_shapes):
            for i in self.selected_shapes:
                self.pen_width[i] += 1
            self.update()
        elif(self.selected_existant_polygon):
            self.polygons[self.selected_existant_polygon][2] += 1
            self.update()

    def decrease_shape_pen_width(self):
        if(self.selected_shapes):
            for i in self.selected_shapes:
                if(self.pen_width[i]>0):
                    self.pen_width[i] -= 1
                self.update()
        elif(self.selected_existant_polygon):
            if(self.polygons[self.selected_existant_polygon][2]>0):
                self.polygons[self.selected_existant_polygon][2] -= 1
                self.update()

    def set_shape_ellipse(self):
        if(self.selected_shapes):
            for i in self.selected_shapes:
                self.shape[i] = "ellipse"
            self.update()

    def set_shape_rect(self):
        if(self.selected_shapes):
            for i in self.selected_shapes:
                self.shape[i] = "rect"
            self.update()
