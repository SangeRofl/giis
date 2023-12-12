from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt6.QtWidgets import QApplication
from abc import ABC, abstractmethod
from enum import Enum
import math


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    else:
        return 0


class Status(Enum):
    EMPTY = 0
    UNFINISHED = 1
    FINISHED = 2


class Axis(Enum):
    x = "x"
    y = "y"
    z = "z"


class FigureState:
    def __init__(self):
        self.pixels = []
        self.data = dict()
        self.message = ""

    def add_pixel(self, x: int, y: int, color) -> None:
        self.pixels.append((x, y, color))

    def add_pixels(self, pixels) -> None:
        for pixel in pixels:
            self.add_pixel(pixel[0], pixel[1], pixel[2])

    def get_pixels(self) -> list:
        return self.pixels

    def add_message(self, message: str):
        self.message += message


def multiply(matrix1, matrix2):
    result = [[0 for i in range(len(matrix2[0]))] for i in range(len(matrix1))]
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

    return result

def multiply_by_val(val, matrix):
    result = [[matrix[i][j] for j in range(len(matrix[0]))] for i in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            result[i][j] *= val
    return result


class Figure(ABC):
    def __init__(self, rect_width=821, rect_height=701):
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.pm = QPixmap(rect_width, rect_height)
        self.pm.fill(QColor(0, 0, 0, 0))
        self.qp = QPainter(self.pm)
        self.qp.setPen(QPen(QColor(0, 0, 0, 255), 1))
        self.status = Status.EMPTY
        self.cur_state = FigureState()
        self.states = []

    def __del__(self):
        del self.qp
        del self

    def draw(self):
        self.clear()
        while self.status != Status.FINISHED:
            self.next_draw_step()

    def next_draw_step(self):
        if self.status == Status.EMPTY:
            self.status = Status.UNFINISHED
            self.first_step()
            self.check_state()
            self.save_state()
        elif self.status == Status.UNFINISHED:
            self.intermediate_step()
            self.check_state()
            self.save_state()
        elif self.status == Status.FINISHED:
            print("Figure is finished")


    def prev_draw_step(self):
        state = self.states.pop()
        for pixel in state.get_pixels():
            self.qp.setPen(QPen(QColor(255, 255, 255, 255), 1))
            self.qp.drawPoint(pixel[0], pixel[1])
        self.cur_state = FigureState()
        for name, value in self.states[-1].data.items():
            self.__setattr__(name, value)

    @abstractmethod
    def first_step(self):
        pass

    @abstractmethod
    def intermediate_step(self):
        pass

    @abstractmethod
    def check_state(self):
        pass

    def save_state(self):
        self.cur_state.data['status'] = self.status
        self.states.append(self.cur_state)
        self.cur_state = FigureState()

    def draw_point(self, x, y, color: QColor = QColor(0, 0, 0, 255)):
        real_x = x
        real_y = self.rect_height-y-1
        self.qp.setPen(QPen(color, 1))
        self.qp.drawPoint(real_x, real_y)
        self.cur_state.add_pixel(real_x, real_y, color)

    def clear(self):
        self.pm.fill(QColor(0, 0, 0, 0))
        self.status = Status.EMPTY
        self.states.clear()
        self.cur_state = FigureState()


class SegmentCDA(Figure):
    def __init__(self, x1: int, y1: int, x2: int, y2: int, rect_width, rect_height):
        super().__init__(rect_width, rect_height)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.last_x = None
        self.last_y = None
        self.length = max(abs(self.x2 - self.x1), abs(self.y2 - self.y1))
        self.length = 1 if self.length == 0 else self.length
        self.cur_length = -1
        self.dx = (self.x2 - self.x1) / self.length
        self.dy = (self.y2 - self.y1) / self.length

    def first_step(self):
        self.last_x = self.x1 + 0.5 * sign(self.dx)
        self.last_y = self.y1 + 0.5 * sign(self.dy)
        self.cur_length += 1
        self.cur_state.add_message(f"Шаг {self.cur_length}: x = {self.last_x}, y = {self.last_y}, Plot(x, y) = ({int(self.last_x)}, {int(self.last_y)})")
        self.draw_point(int(self.last_x), int(self.last_y))

    def intermediate_step(self):
        self.last_x += self.dx
        self.last_y += self.dy
        self.cur_length += 1
        self.cur_state.add_message(f"Шаг {self.cur_length}: x = {self.last_x}, y = {self.last_y}, Plot(x, y) = ({int(self.last_x)}, {int(self.last_y)})")
        self.draw_point(int(self.last_x), int(self.last_y))

    def check_state(self):
        if self.cur_length == self.length:
            self.status = Status.FINISHED

    def save_state(self):
        self.cur_state.data['last_x'] = self.last_x
        self.cur_state.data['last_y'] = self.last_y
        self.cur_state.data['cur_length'] = self.cur_length
        super().save_state()


class SegmentWoo(Figure):
    def __init__(self, x1: int, y1: int, x2: int, y2: int, rect_width, rect_height):
        super().__init__(rect_width, rect_height)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.dx = (self.x2 - self.x1)
        self.dy = (self.y2 - self.y1)
        self.last_x = None
        self.last_y = None
        self.main_axis = Axis.x if abs(self.dx) > abs(self.dy) else Axis.y
        self.length = max(abs(self.x2 - self.x1), abs(self.y2 - self.y1))
        self.cur_length = -1


    def first_step(self):
        self.last_x = self.x1
        self.last_y = self.y1
        self.cur_length += 1
        self.cur_state.add_message(f"Шаг {self.cur_length}: {self.main_axis.value} = {self.last_x if self.main_axis == Axis.x else self.last_y}, plot({self.last_x}, {self.last_y});")
        self.draw_point(self.last_x, self.last_y)

    def intermediate_step(self):
        self.cur_length += 1
        if self.main_axis == Axis.x:
            self.last_x += 1 if self.dx > 0 else -1
            real_y = (self.last_x - self.x1) * self.dy / self.dx + self.y1
            if real_y-int(real_y) == 0:
                self.draw_point(self.last_x, int(real_y))
                self.cur_state.add_message(
                    f"Шаг {self.cur_length}: {self.main_axis.value} = {self.last_x if self.main_axis == Axis.x else self.last_y}, plot({self.last_x}, {int(real_y)});")
            else:
                px1_y, px2_y = math.ceil(real_y), math.floor(real_y)
                px1_y_intense, px2_y_intense = abs(real_y - px2_y), abs(real_y - px1_y)
                self.draw_point(self.last_x, px1_y, QColor(0, 0, 0, int(255 * px1_y_intense)))
                self.draw_point(self.last_x, px2_y, QColor(0, 0, 0, int(255 * px2_y_intense)))
                self.cur_state.add_message(
                    f"Шаг {self.cur_length}: {self.main_axis.value} = {self.last_x if self.main_axis == Axis.x else self.last_y}, y1 = {px1_y}, distance1 = {round(1-px1_y_intense, 2)}, y2 = {px2_y}, distance2 = {round(1-px2_y_intense, 2)}, plot({self.last_x}, {int(px1_y)}, {round(px1_y_intense, 2)}), plot({self.last_x}, {int(px2_y)}, {round(px2_y_intense, 2)});")

        else:
            self.last_y += 1 if self.dy > 0 else -1
            real_x = (self.last_y - self.y1) * self.dx / self.dy + self.x1
            if real_x - int(real_x) == 0:
                self.draw_point(int(real_x), self.last_y)
                self.cur_state.add_message(
                    f"Шаг {self.cur_length}: {self.main_axis.value} = {self.last_x if self.main_axis == Axis.x else self.last_y}, plot({int(real_x)}, {self.last_y});")
            else:
                py1_x, py2_x = math.ceil(real_x), math.floor(real_x)
                py1_x_intense, py2_x_intense = real_x - py2_x , py1_x - real_x
                self.draw_point(py1_x, self.last_y, QColor(0, 0, 0, int(255 * py1_x_intense)))
                self.draw_point(py2_x, self.last_y, QColor(0, 0, 0, int(255 * py2_x_intense)))
                self.cur_state.add_message(
                    f"Шаг {self.cur_length}: {self.main_axis.value} = {self.last_x if self.main_axis == Axis.x else self.last_y}, x1 = {py1_x}, distance1 = {round(1 - py1_x_intense, 2)}, x2 = {py2_x}, distance2 = {round(1 - py2_x_intense, 2)}, plot({int(py1_x)}, {self.last_y}, {round(py1_x_intense, 2)}), plot({int(py2_x)}, {self.last_y}, {round(py2_x_intense, 2)});")


    def check_state(self):
        if self.cur_length == self.length:
            self.status = Status.FINISHED

    def save_state(self):
        self.cur_state.data['last_x'] = self.last_x
        self.cur_state.data['last_y'] = self.last_y
        self.cur_state.data['cur_length'] = self.cur_length
        super().save_state()


class SegmentBrez(Figure):
    def __init__(self, x1: int, y1: int, x2: int, y2: int, rect_width, rect_height):
        super().__init__(rect_width, rect_height)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.dx = (self.x2 - self.x1)
        self.dy = (self.y2 - self.y1)
        self.e = None
        self.last_x = None
        self.last_y = None
        self.main_axis = Axis.x if abs(self.dx) > abs(self.dy) else Axis.y
        self.length = max(abs(self.x2 - self.x1), abs(self.y2 - self.y1))
        self.cur_length = -1


    def first_step(self):
        self.last_x = self.x1
        self.last_y = self.y1
        if self.main_axis == Axis.x:
            self.e = self.dy / self.dx - 0.5
        else:
            self.e = self.dx / self.dy - 0.5
        self.cur_length += 1
        self.cur_state.add_message(f"Шаг {self.cur_length}: e = {self.e}, x = {self.last_x}, y = {self.last_y}, Plot(x, y) = ({int(self.last_x)}, {int(self.last_y)})")
        self.draw_point(int(self.last_x), int(self.last_y))

    def intermediate_step(self):
        if self.e >= 0:
            if self.main_axis == Axis.x:
                self.last_y += 1 if self.dy > 0 else -1
            else:
                self.last_x += 1 if self.dx > 0 else -1
            self.e -= 1
        if self.main_axis == Axis.x:
            self.last_x += 1 if self.dx > 0 else -1
            self.e = self.e + self.dy/self.dx
        else:
            self.last_y += 1 if self.dy > 0 else -1
            self.e = self.e + self.dx/self.dy
        self.cur_length += 1
        self.cur_state.add_message(f"Шаг {self.cur_length}: e = {self.e}, x = {self.last_x}, y = {self.last_y}, Plot(x, y) = ({int(self.last_x)}, {int(self.last_y)})")
        self.draw_point(int(self.last_x), int(self.last_y))

    def check_state(self):
        if self.cur_length == self.length:
            self.status = Status.FINISHED

    def save_state(self):
        self.cur_state.data['last_x'] = self.last_x
        self.cur_state.data['last_y'] = self.last_y
        self.cur_state.data['e'] = self.e
        self.cur_state.data['cur_length'] = self.cur_length
        super().save_state()


class Okr(Figure):
    def __init__(self, x: int, y: int, R: int, rect_width, rect_height):
        super().__init__(rect_width, rect_height)
        self.x = x
        self.y = y
        self.R = R
        self.d = None
        self.last_x = None
        self.last_y = None
        self.sig = None
        self.sig1 = None
        self.pred = 0
        self.cur_step = -1

    # первый шаг
    def first_step(self):
        self.cur_step += 1
        self.last_x = 0
        self.last_y = self.R
        self.d = 2 - 2 * self.R
        self.cur_state.add_message(f"Шаг {self.cur_step}: d = , sig = {self.sig}, sig1 = {self.sig1}, pix = , x = {self.last_x}, y = {self.last_y}, d_i+1 = {self.d}, Plot(x, y) = ({self.last_x + self.x}, {self.last_y + self.y})")
        self.draw_point(int(self.last_x+self.x), int(self.last_y+self.y))
        self.draw_point(int(self.last_x + self.x), int(-self.last_y + self.y))

    # промежуточный шаг
    def intermediate_step(self):
        self.cur_step += 1
        last_d = self.d
        pix = "error"
        if self.d > 0:
            self.sig1 = 2 * self.d - 2 * self.last_x - 1
            if self.sig1 > 0:
                self.last_y = self.last_y - 1
                self.d = self.d - 2 * self.last_y + 1
                pix = "V"
            else:
                self.last_x += 1
                self.last_y -= 1
                self.d += 2 * self.last_x - 2 * self.last_y + 2
                pix = "D"
        elif self.d < 0:
            self.sig = 2 * self.d + 2 * self.last_y - 1
            if self.sig <= 0:
                self.last_x = self.last_x + 1
                self.d = self.d + 2 * self.last_x + 1
                pix = "H"
            else:
                self.last_x += 1
                self.last_y -= 1
                self.d += 2 * self.last_x - 2 * self.last_y + 2
                pix = "D"
        else:
            self.last_x += 1
            self.last_y -= 1
            self.d += 2 * self.last_x - 2 * self.last_y + 2
            pix = "D"

        self.cur_state.add_message(f"Шаг {self.cur_step}: d = {last_d}, sig = {self.sig}, sig1 = {self.sig1}, pix = {pix}, x = {self.last_x}, y = {self.last_y}, d_i+1 = {self.d}, Plot(x, y) = ({self.last_x+self.x}, {self.last_y+self.y})")
        self.draw_point(int(self.last_x+self.x), int(self.last_y+self.y))
        self.draw_point(int(-self.last_x + self.x), int(self.last_y + self.y))
        self.draw_point(int(self.last_x + self.x), int(-self.last_y + self.y))
        self.draw_point(int(-self.last_x + self.x), int(-self.last_y + self.y))

    def check_state(self):
        if self.last_y <= self.pred:
            self.status = Status.FINISHED

    def save_state(self):
        self.cur_state.data['last_x'] = self.last_x
        self.cur_state.data['last_y'] = self.last_y
        self.cur_state.data['cur_step'] = self.cur_step
        self.cur_state.data['d'] = self.d
        super().save_state()


class Ellipse(Figure):
    def __init__(self, x: int, y: int, a: int, b: int, rect_width, rect_height):
        super().__init__(rect_width, rect_height)
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.d = None
        self.last_x = None
        self.last_y = None
        self.sig = None
        self.sig1 = None
        self.pred = 0
        self.cur_step = -1

    # первый шаг
    def first_step(self):
        self.cur_step += 1
        self.last_x = 0
        self.last_y = self.b
        self.d = self.a**2 + self.b**2 - 2 * (self.a**2) * self.b
        self.cur_state.add_message(f"Шаг {self.cur_step}: d = , sig = {self.sig}, sig1 = {self.sig1}, pix = , x = {self.last_x}, y = {self.last_y}, d_i+1 = {self.d}, Plot(x, y) = ({self.last_x + self.x}, {self.last_y + self.y})")
        self.draw_point(int(self.last_x+self.x), int(self.last_y+self.y))
        self.draw_point(int(self.last_x + self.x), int(-self.last_y + self.y))

    # промежуточный шаг
    def intermediate_step(self):
        self.cur_step += 1
        last_d = self.d
        pix = "error"
        if self.d > 0:
            self.sig1 = 2 * (self.d - self.b**2 * self.last_x) - 1
            if self.sig1 > 0:
                self.last_y = self.last_y - 1
                self.d = self.d + self.a**2 * (1-self.last_y*2)
                pix = "V"
            else:
                self.last_x += 1
                self.last_y -= 1
                self.d += (self.b**2) * (self.last_x*2 + 1) + (self.a**2) * (1 - self.last_y * 2)
                pix = "D"
        elif self.d < 0:
            self.sig = 2 * (self.d + self.a**2 * self.last_y) - 1
            if self.sig <= 0:
                self.last_x = self.last_x + 1
                self.d = self.d + self.b**2 * (self.last_x*2 + 1)
                pix = "H"
            else:
                self.last_x += 1
                self.last_y -= 1
                self.d += (self.b**2) * (self.last_x*2 + 1) + (self.a**2) * (1 - self.last_y * 2)
                pix = "D"
        else:
            self.last_x += 1
            self.last_y -= 1
            self.d += (self.b**2) * (self.last_x*2 + 1) + (self.a**2) * (1 - self.last_y * 2)
            pix = "D"

        self.cur_state.add_message(f"Шаг {self.cur_step}: d = {last_d}, sig = {self.sig}, sig1 = {self.sig1}, pix = {pix}, x = {self.last_x}, y = {self.last_y}, d_i+1 = {self.d}, Plot(x, y) = ({self.last_x+self.x}, {self.last_y+self.y})")
        self.draw_point(int(self.last_x+self.x), int(self.last_y+self.y))
        self.draw_point(int(-self.last_x + self.x), int(self.last_y + self.y))
        self.draw_point(int(self.last_x + self.x), int(-self.last_y + self.y))
        self.draw_point(int(-self.last_x + self.x), int(-self.last_y + self.y))

    def check_state(self):
        if self.last_y <= self.pred:
            self.status = Status.FINISHED

    def save_state(self):
        self.cur_state.data['last_x'] = self.last_x
        self.cur_state.data['last_y'] = self.last_y
        self.cur_state.data['cur_step'] = self.cur_step
        self.cur_state.data['d'] = self.d
        super().save_state()


class Gip(Figure):
    def __init__(self, x: int, y: int, a: int, b: int, rect_width, rect_height):
        super().__init__(rect_width, rect_height)
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.d = None
        self.last_x = None
        self.last_y = None
        self.sig = None
        self.sig1 = None
        self.pred = 2000
        self.cur_step = -1

    # первый шаг
    def first_step(self):
        self.cur_step += 1
        self.last_x = abs(self.a)
        self.last_y = 0
        self.d = self.b**2 - self.a**2 + 2 * self.a * self.b**2
        self.cur_state.add_message(f"Шаг {self.cur_step}: d = , sig = {self.sig}, sig1 = {self.sig1}, pix = , x = {self.last_x}, y = {self.last_y}, d_i+1 = {self.d}, Plot(x, y) = ({self.last_x + self.x}, {self.last_y + self.y})")
        self.draw_point(int(self.last_x+self.x), int(self.last_y+self.y))
        self.draw_point(int(-self.last_x + self.x), int(self.last_y + self.y))

    # промежуточный шаг
    def intermediate_step(self):
        self.cur_step += 1
        last_d = self.d
        pix = "error"
        if self.d > 0:
            self.sig1 = 2 * (self.d - self.b ** 2 * self.last_x) - self.b ** 2
            if self.sig1 > 0:
                self.last_y = self.last_y + 1
                self.d = self.d - self.a**2 * (1+self.last_y*2)
                pix = "V"
            else:
                self.last_x += 1
                self.last_y += 1
                self.d += (self.b**2) * (self.last_x*2 + 1) - (self.a**2) * (1 + self.last_y * 2)
                pix = "D"
        elif self.d < 0:
            self.sig = 2 * (self.d + self.a**2 * self.last_y) + self.a**2
            if self.sig <= 0:
                self.last_x = self.last_x + 1
                self.d = self.d + self.b**2 * (self.last_x*2 + 1)
                pix = "H"
            else:
                self.last_x += 1
                self.last_y += 1
                self.d += (self.b**2) * (self.last_x*2 + 1) - (self.a**2) * (1 + self.last_y * 2)
                pix = "D"
        else:
            self.last_x += 1
            self.last_y += 1
            self.d += (self.b**2) * (self.last_x*2 + 1) - (self.a**2) * (1 + self.last_y * 2)
            pix = "D"

        self.cur_state.add_message(f"Шаг {self.cur_step}: d = {last_d}, sig = {self.sig}, sig1 = {self.sig1}, pix = {pix}, x = {self.last_x}, y = {self.last_y}, d_i+1 = {self.d}, Plot(x, y) = ({self.last_x+self.x}, {self.last_y+self.y})")
        self.draw_point(int(self.last_x+self.x), int(self.last_y+self.y))
        self.draw_point(int(-self.last_x + self.x), int(self.last_y + self.y))
        self.draw_point(int(self.last_x + self.x), int(-self.last_y + self.y))
        self.draw_point(int(-self.last_x + self.x), int(-self.last_y + self.y))

    def check_state(self):
        if self.last_x >= self.pred:
            self.status = Status.FINISHED

    def save_state(self):
        self.cur_state.data['last_x'] = self.last_x
        self.cur_state.data['last_y'] = self.last_y
        self.cur_state.data['cur_step'] = self.cur_step
        self.cur_state.data['d'] = self.d
        super().save_state()

class Par(Figure):
    def __init__(self, x: int, y: int, p: int, rect_width, rect_height):
        super().__init__(rect_width, rect_height)
        self.x = x
        self.y = y
        self.p = p
        self.d = None
        self.last_x = None
        self.last_y = None
        self.sig = None
        self.sig1 = None
        self.pred = 2000
        self.cur_step = -1

    # первый шаг
    def first_step(self):
        self.cur_step += 1
        self.last_x = 0
        self.last_y = 0
        self.d = 1 - self.p*2
        self.cur_state.add_message(f"Шаг {self.cur_step}: d = , sig = {self.sig}, sig1 = {self.sig1}, pix = , x = {self.last_x}, y = {self.last_y}, d_i+1 = {self.d}, Plot(x, y) = ({self.last_x + self.x}, {self.last_y + self.y})")
        self.draw_point(int(self.last_x+self.x), int(self.last_y+self.y))

    # промежуточный шаг
    def intermediate_step(self):
        self.cur_step += 1
        last_d = self.d
        pix = "error"
        if self.d < 0:
            self.sig1 = 2 * self.d + self.p * 2
            if self.sig1 <= 0:
                self.last_y = self.last_y + 1
                self.d = self.d + 2 * self.last_y + 1
                pix = "V"
            else:
                self.last_x += 1
                self.last_y += 1
                self.d += 2 * (self.last_y - self.p) + 1
                pix = "D"
        elif self.d > 0:
            self.sig = self.d * 2 - 2 * self.last_y - 1
            if self.sig > 0:
                self.last_x = self.last_x + 1
                self.d = self.d - 2 * self.p
                pix = "H"
            else:
                self.last_x += 1
                self.last_y += 1
                self.d += 2 * (self.last_y - self.p) + 1
                pix = "D"
        else:
            self.last_x += 1
            self.last_y += 1
            self.d += 2 * (self.last_y - self.p) + 1
            pix = "D"

        self.cur_state.add_message(f"Шаг {self.cur_step}: d = {last_d}, sig = {self.sig}, sig1 = {self.sig1}, pix = {pix}, x = {self.last_x}, y = {self.last_y}, d_i+1 = {self.d}, Plot(x, y) = ({self.last_x+self.x}, {self.last_y+self.y})")
        self.draw_point(int(self.last_x+self.x), int(self.last_y+self.y))
        self.draw_point(int(self.last_x + self.x), int(-self.last_y + self.y))

    def check_state(self):
        if self.last_x >= self.pred:
            self.status = Status.FINISHED

    def save_state(self):
        self.cur_state.data['last_x'] = self.last_x
        self.cur_state.data['last_y'] = self.last_y
        self.cur_state.data['cur_step'] = self.cur_step
        self.cur_state.data['d'] = self.d
        super().save_state()


class ErmitInterpol(Figure):
    def __init__(self, p1x: int, p1y: int, p4x: int, p4y: int, r1x: float, r1y: float, r4x: float, r4y: float, rect_width, rect_height):
        super().__init__(rect_width, rect_height)
        self.p1x = p1x
        self.p1y = p1y
        self.p4x = p4x
        self.p4y = p4y
        self.r1x = r1x
        self.r1y = r1y
        self.r4x = r4x
        self.r4y = r4y
        self.dt = 1/rect_width/10# 1 / max(abs(p1x - p4x), abs(p1y - p4y)) / 100
        self.t = None
        self.last_x = None
        self.last_y = None
        self.ermit_form = [
            [2, -2, 1, 1],
            [-3, 3, -2, -1],
            [0, 0, 1, 0],
            [1, 0, 0, 0]
        ]
        self.var_form = [
            [p1x, p1y],
            [p4x, p4y],
            [r1x, r1y],
            [r4x, r4y]
        ]
        self.res_var_form = multiply(self.ermit_form, self.var_form)
        self.cur_step = -1

    # первый шаг
    def first_step(self):
        self.cur_step += 1
        self.t = 0
        res_matrix = multiply([[self.t**3, self.t**2, self.t, 1]], self.res_var_form)
        self.last_x, self.last_y = res_matrix[0][0], res_matrix[0][1]
        self.cur_state.add_message(
            f"Шаг {self.cur_step}: t = {self.t}, y = {self.last_y}, Plot(x, y) = ({round(self.last_x)}, {round(self.last_y)}")
        self.draw_point(round(self.last_x), round(self.last_y))

    # промежуточный шаг
    def intermediate_step(self):
        self.cur_step += 1
        self.t += self.dt
        res_matrix = multiply([[self.t ** 3, self.t ** 2, self.t, 1]], self.res_var_form)
        self.last_x, self.last_y = res_matrix[0][0], res_matrix[0][1]
        self.cur_state.add_message(
            f"Шаг {self.cur_step}: t = {self.t}, y = {self.last_y}, Plot(x, y) = ({round(self.last_x)}, {round(self.last_y)}")
        self.draw_point(round(self.last_x), round(self.last_y))

    def check_state(self):
        if self.t >= 1:
            self.status = Status.FINISHED

    def save_state(self):
        self.cur_state.data['last_x'] = self.last_x
        self.cur_state.data['last_y'] = self.last_y
        self.cur_state.data['cur_step'] = self.cur_step
        self.cur_state.data['t'] = self.t
        super().save_state()


class BezInterpol(Figure):
    def __init__(self, p1x: int, p1y: int, p2x: int, p2y: int, p3x: int, p3y: int, p4x: int, p4y: int, rect_width, rect_height):
        super().__init__(rect_width, rect_height)
        self.p1x = p1x
        self.p1y = p1y
        self.p4x = p4x
        self.p4y = p4y
        self.p2x = p2x
        self.p2y = p2y
        self.p3x = p3x
        self.p3y = p3y
        self.dt = 1/rect_width/10
        self.t = None
        self.last_x = None
        self.last_y = None
        self.ermit_form = [
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ]
        self.var_form = [
            [p1x, p1y],
            [p2x, p2y],
            [p3x, p3y],
            [p4x, p4y]
        ]
        self.res_var_form = multiply(self.ermit_form, self.var_form)
        self.cur_step = -1

    # первый шаг
    def first_step(self):
        self.cur_step += 1
        self.t = 0
        res_matrix = multiply([[self.t**3, self.t**2, self.t, 1]], self.res_var_form)
        self.last_x, self.last_y = res_matrix[0][0], res_matrix[0][1]
        self.cur_state.add_message(
            f"Шаг {self.cur_step}: t = {self.t}, y = {self.last_y}, Plot(x, y) = ({round(self.last_x)}, {round(self.last_y)}")
        self.draw_point(round(self.last_x), round(self.last_y))

    # промежуточный шаг
    def intermediate_step(self):
        self.cur_step += 1
        self.t += self.dt
        res_matrix = multiply([[self.t ** 3, self.t ** 2, self.t, 1]], self.res_var_form)
        self.last_x, self.last_y = res_matrix[0][0], res_matrix[0][1]
        self.cur_state.add_message(
            f"Шаг {self.cur_step}: t = {self.t}, y = {self.last_y}, Plot(x, y) = ({round(self.last_x)}, {round(self.last_y)}")
        self.draw_point(round(self.last_x), round(self.last_y))

    def check_state(self):
        if self.t >= 1:
            self.status = Status.FINISHED

    def save_state(self):
        self.cur_state.data['last_x'] = self.last_x
        self.cur_state.data['last_y'] = self.last_y
        self.cur_state.data['cur_step'] = self.cur_step
        self.cur_state.data['t'] = self.t
        super().save_state()


class SplineInterpol(Figure):
    def __init__(self, points: list[tuple[int, int]], closed: bool, rect_width, rect_height):
        super().__init__(rect_width, rect_height)
        self.points = points
        if closed:
            self.points.append(points[0])
            self.points.append(points[1])
            self.points.append(points[2])
        self.dt = 1/rect_width/10
        self.t = None
        self.spline_form = [
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 0, 3, 0],
            [1, 4, 1, 0]
        ]
        self.var_form = None
        self.res_var_form = None
        self.cur_n = None
        self.cur_step = -1

    # первый шаг
    def first_step(self):
        self.cur_step += 1
        self.t = 0
        self.cur_n = 1
        self.var_form = [
            [self.points[self.cur_n-1][0], self.points[self.cur_n-1][1]],
            [self.points[self.cur_n][0], self.points[self.cur_n][1]],
            [self.points[self.cur_n + 1][0], self.points[self.cur_n + 1][1]],
            [self.points[self.cur_n + 2][0], self.points[self.cur_n + 2][1]]
        ]
        self.res_var_form = multiply(self.spline_form, self.var_form)
        res_matrix = multiply_by_val(1/6, multiply([[self.t**3, self.t**2, self.t, 1]], self.res_var_form))
        x, y = res_matrix[0][0], res_matrix[0][1]
        self.cur_state.add_message(
            f"Шаг {self.cur_step}: segment = {self.cur_n}, t = {self.t}, x = {x}, y = {y}, Plot(x, y) = ({round(x)}, {round(y)}")
        self.draw_point(round(x), round(y))

    # промежуточный шаг
    def intermediate_step(self):
        if self.t >= 1:
            self.cur_step += 1
            self.t = 0
            self.cur_n += 1
            self.var_form = [
                [self.points[self.cur_n - 1][0], self.points[self.cur_n - 1][1]],
                [self.points[self.cur_n][0], self.points[self.cur_n][1]],
                [self.points[self.cur_n + 1][0], self.points[self.cur_n + 1][1]],
                [self.points[self.cur_n + 2][0], self.points[self.cur_n + 2][1]]
            ]
            self.res_var_form = multiply(self.spline_form, self.var_form)
            res_matrix = multiply_by_val(1/6, multiply([[self.t**3, self.t**2, self.t, 1]], self.res_var_form))
            x, y = res_matrix[0][0], res_matrix[0][1]
            self.cur_state.add_message(
                f"Шаг {self.cur_step}: segment = {self.cur_n}, t = {self.t}, x = {x}, y = {y}, Plot(x, y) = ({round(x)}, {round(y)}")
            self.draw_point(round(x), round(y))
        else:
            self.cur_step += 1
            self.t += self.dt
            res_matrix = multiply_by_val(1/6, multiply([[self.t**3, self.t**2, self.t, 1]], self.res_var_form))
            x, y = res_matrix[0][0], res_matrix[0][1]
            self.cur_state.add_message(
                f"Шаг {self.cur_step}: segment = {self.cur_n}, t = {self.t}, x = {x}, y = {y}, Plot(x, y) = ({round(x)}, {round(y)}")
            self.draw_point(round(x), round(y))

    def check_state(self):
        if self.cur_n >= len(self.points) - 3 and self.t >= 1:
            self.status = Status.FINISHED

    def save_state(self):
        self.cur_state.data['cur_step'] = self.cur_step
        self.cur_state.data['t'] = self.t
        self.cur_state.data['var_form'] = self.var_form
        self.cur_state.data['res_var_form'] = self.res_var_form
        self.cur_state.data['cur_n'] = self.cur_n
        super().save_state()


if __name__ == "__main__":
    app = QApplication([])
    seg = SegmentCDA(0, 0, 5, 5, 500, 500)
    seg.draw()
    print(1)
    app.exec()



