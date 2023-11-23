from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen
from figures import Figure, SegmentCDA, FigureState


class Model:
    def __init__(self, rect_width, rect_height):
        self.figures = []
        self.cur_figure = None
        self.fig_cls = None
        self.rw = rect_width
        self.rh = rect_height
        self.pm = QPixmap(self.rw, self.rh)
        self.pm.fill(QColor(255, 255, 255, 255))
        self.qp = QPainter(self.pm)
        self.messages = []

    def add_figure(self, fig_cls, debug, **kwargs):
        self.set_figure_class(fig_cls)
        self.cur_figure = self.fig_cls(**kwargs, rect_height=self.rh, rect_width=self.rw)
        self.figures.append(self.cur_figure)
        if debug == False:
            self.cur_figure.draw()
            self.update()

    def clear(self):
        self.figures.clear()
        self.update()
        # del self.cur_figure # ??


    def set_figure_class(self, cls):
        self.fig_cls = cls

    def debug_next(self):
        self.cur_figure.next_draw_step()
        self.messages.append(self.cur_figure.states[-1].message)
        self.update()

    def debug_prev(self):
        if len(self.cur_figure.states)>=2:
            self.cur_figure.prev_draw_step()
            self.update()

    def update(self):
        self.pm.fill(QColor(255, 255, 255, 255))
        for figure in self.figures:
            self.qp.drawPixmap(0, 0, figure.pm)
