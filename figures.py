from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt6.QtWidgets import QApplication
from abc import ABC, abstractmethod
from enum import Enum


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
        self.message+=message


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

    def draw_point(self, x, y, color: QColor = (0, 0, 0, 255)):
        real_x = x
        real_y = self.rect_height-y-1
        self.qp.setPen(QPen(QColor(0, 0, 0, 255), 1))
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
                self.last_y += 1
            else:
                self.last_x += 1
            self.e -= 1
        if self.main_axis == Axis.x:
            self.last_x += 1
            self.e = self.e + self.dy/self.dx
        else:
            self.last_y += 1
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

    # первый шаг
    def first_step(self):
        self.last_x = 0
        self.last_y = self.R
        self.d = 2 - 2 * self.R
        self.cur_state.add_message(f"d = {self.d}, sig = {self.sig}, sig1 = {self.sig1}, x = {self.last_x}, y = {self.last_y}, Plot(x, y) = ({self.last_x}, {self.last_y})")
        self.draw_point(int(self.last_x+self.x), int(self.last_y+self.y))

    # промежуточный шаг
    def intermediate_step(self):
        if self.d > 0:
            self.sig1 = 2 * self.d - 2 * self.last_x - 1
            if self.sig1 > 0:
                self.last_y = self.last_y - 1
                self.d = self.d - 2 * self.last_y + 1
            else:
                self.last_x += 1
                self.last_y -= 1
                self.d += 2 * self.last_x - 2 * self.last_y + 2
        elif self.d < 0:
            self.sig = 2 * self.d + 2 * self.last_y - 1
            if self.sig <= 0:
                self.last_x = self.last_x + 1
                self.d = self.d + 2 * self.last_x + 1
            else:
                self.last_x += 1
                self.last_y -= 1
                self.d += 2 * self.last_x - 2 * self.last_y + 2
        else:
            self.last_x += 1
            self.last_y -= 1
            self.d += 2 * self.last_x - 2 * self.last_y + 2

        self.cur_state.add_message(f"d = {self.d}, sig = {self.sig}, sig1 = {self.sig1}, x = {self.last_x}, y = {self.last_y}, Plot(x, y) = ({self.last_x}, {self.last_y})")
        self.draw_point(int(self.last_x+self.x), int(self.last_y+self.y))

    def check_state(self):
        if self.last_y <= self.pred:
            self.status = Status.FINISHED

    def save_state(self):
        self.cur_state.data['last_x'] = self.last_x
        self.cur_state.data['last_y'] = self.last_y
        super().save_state()


if __name__ == "__main__":
    app = QApplication([])
    seg = SegmentCDA(0, 0, 5, 5, 500, 500)
    seg.draw()
    print(1)
    app.exec()



