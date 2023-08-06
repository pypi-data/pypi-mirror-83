import guidata
from guiqwt.plot import CurveDialog
from guiqwt.curve import CurveItem
from guiqwt.styles import CurveParam
from guiqwt.builder import make

from guidata.qt.QtCore import Qt, QSize
from guidata.qt.QtGui import QMainWindow, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QSplitter, QToolBar

from guiqwt.image import ImagePlot
from guiqwt.curve import PlotItemList
from guiqwt.histogram import ContrastAdjustment
from guiqwt.plot import PlotManager
from guiqwt.builder import make
from guiqwt.curve import PolygonMapItem

import numpy as np

from gfafunctionality.raws import RawImageFile


class WaveForm(object):
    def __init__(self, row, data_limit=None, last=True):
        self._limit = data_limit
        self._last = last
        self.meta = row.meta
        self.id = row.meta['ccd_row_num']
        self.row = row

        self.data = None
        self.max_y = 0
        self.min_y = 0
        self.reference_edges = None
        self.signal_edges = None
        self.debug_edges = None

    @property
    def x(self):
        return self.data[:, 0]

    @property
    def y(self):
        return self.data[:, 1]

    def process(self):
        if self._limit and self._last:
            self.data = np.array([[ix, el & 0xffff, ((el & 0x10000) >> 16), ((el & 0x20000) >> 17),
                                   ((el & 0x40000) >> 18)] for ix, el in enumerate(self.row.data[-self._limit:])])
        elif self._limit:
            self.data = np.array([[ix, el & 0xffff, ((el & 0x10000) >> 16), ((el & 0x20000) >> 17),
                                   ((el & 0x40000) >> 18)] for ix, el in enumerate(self.row.data[:self._limit])])
        else:
            self.data = np.array([[ix, el & 0xffff, ((el & 0x10000) >> 16), ((el & 0x20000) >> 17),
                                   ((el & 0x40000) >> 18)] for ix, el in enumerate(self.row.data)])

        # x = values[:, 0]
        # y = values[:, 1]
        # ref_values = values[:, 2]
        # signal_values = values[:, 3]
        # debug_values = values[:, 4]

        self.max_y = max(self.data[:, 1])
        self.min_y = min(self.data[:, 1])

        # print(self.data[:, 2])
        # print(self.data[:, 3])
        self.reference_edges = np.where(self.data[:, 2][:-1] != self.data[:, 2][1:])[0]
        # print(len(self.reference_edges))
        # print("reference edges: {}".format(self.reference_edges))
        self.signal_edges = np.where(self.data[:, 3][:-1] != self.data[:, 3][1:])[0]
        self.debug_edges = np.where(self.data[:, 4][:-1] != self.data[:, 4][1:])[0]
        # print(len(self.signal_edges))
        # print("signal_edges: {}".format(self.signal_edges))
        # To make sure first index is a rise up edge
        if self.data[:, 2][0] == 1:
            self.reference_edges = np.insert(self.reference_edges, 0, [0])
            # print("reference inserting: {}".format(self.reference_edges))
        if self.data[:, 3][0] == 1:
            self.signal_edges = np.insert(self.signal_edges, 0, [0])
            # print("signal inserting: {}".format(self.signal_edges))
        if self.data[:, 4][0] == 1:
            self.debug_edges = np.insert(self.debug_edges, 0, [0])

        if self.data[:, 2][-1] == 1:
            self.reference_edges = np.append(self.reference_edges, [len(self.data[:, 2])])
            # print("reference append: {}".format(self.reference_edges))
        if self.data[:, 3][-1] == 1:
            self.signal_edges = np.append(self.signal_edges, [len(self.data[:, 3])])
            # print("signal append: {}".format(self.signal_edges))
        if self.data[:, 4][-1] == 1:
            self.debug_edges = np.append(self.debug_edges, [len(self.data[:, 4])])

        # convert array into 2-D array:
        self.reference_edges = self.reference_edges.reshape(-1, 2)
        self.signal_edges = self.signal_edges.reshape(-1, 2)
        self.debug_edges = self.debug_edges.reshape(-1, 2)
        # print("reference edges: {}".format(self.reference_edges))
        # print("signal_edges: {}".format(self.signal_edges))

        # Delete data
        self.row = None


def create_square(x0, x1, y0, y1):
    PTS = np.empty((4, 2), float)
    PTS[:, 0] = (x0, x1, x1, x0)
    PTS[:, 1] = (y0, y0, y1, y1)
    return PTS


class GUIQWTPlotter(object):
    def __init__(self, image, e2v_ccd230_42_im=None):
        self.image = image
        self.e2vccd230_42 = e2v_ccd230_42_im

    def show_as_waveform(self, maxWidth=None, last=True, max_lines=None):
        from guidata import install_translator
        from guidata.qt.QtGui import QApplication
        exec = False
        app = QApplication.instance()
        if not app:
            exec = True
            app = QApplication([])
            install_translator(app)
        win = CurveDialog(edit=False, toolbar=True, wintitle="Waveform",
                          options=dict(title="GFA Waveform output", ylabel="ADUs"))
        plot = win.get_plot()
        colors = [u'#aa00aa', u'#aaaa00', u'#00aaaa', u'#0000aa', u'#aa0000']
        waveforms = []
        num_of_rects = 0
        for amp in self.image.amplifiers:
            if max_lines is None:
                max_lines = -1
            for row in amp.rows[:max_lines]:
                wf = WaveForm(row, data_limit=maxWidth, last=last)
                wf.process()
                waveforms.append(wf)

                row_num = row.meta['ccd_row_num']
                # if maxWidth:
                #     if last:
                #         data = wf.data[-maxWidth:]
                #     else:
                #         data = wf.data[:min(len(row.data), maxWidth)]
                # else:
                #     data = wf.data

                curve = make.curve(wf.x, wf.y, color=colors[amp.amp_id], linewidth=2.0)
                num_of_rects += len(wf.reference_edges) + len(wf.signal_edges) + len(wf.debug_edges)
                curve.setTitle("Amp {0} row {1}".format(amp.amp_id, row_num))
                plot.add_item(curve)
        points = []
        offsets = np.zeros((num_of_rects+1, 2), np.int32)
        colors = np.zeros((num_of_rects+1, 2), np.uint32)
        # print("Num of rects: {}".format(num_of_rects))
        npts = 0
        k = 0
        for wf in waveforms:
            for ix, pulse in enumerate(wf.reference_edges):
                k += 1
                pts = create_square(x0=pulse[0], x1=pulse[1], y0=wf.min_y, y1=wf.max_y)
                offsets[k, 0] = k
                offsets[k, 1] = npts
                npts += pts.shape[0]
                points.append(pts)
                colors[k, 0] = 0xaaaaffff
                colors[k, 1] = 0xaaaaffff
            for ix, pulse in enumerate(wf.signal_edges):
                k += 1
                pts = create_square(x0=pulse[0], x1=pulse[1], y0=wf.min_y, y1=wf.max_y)
                offsets[k, 0] = k
                offsets[k, 1] = npts
                npts += pts.shape[0]
                points.append(pts)
                colors[k, 0] = 0xaaffaaff
                colors[k, 1] = 0xaaffaaff
            for ix, pulse in enumerate(wf.debug_edges):
                k += 1
                pts = create_square(x0=pulse[0], x1=pulse[1], y0=wf.min_y, y1=wf.max_y)
                offsets[k, 0] = k
                offsets[k, 1] = npts
                npts += pts.shape[0]
                points.append(pts)
                colors[k, 0] = 0xffaaaaff
                colors[k, 1] = 0xffaaaaff
        if points:
            points = np.concatenate(points)
            # print("rects points: {}".format(points))
            crv = PolygonMapItem()
            crv.set_data(points, offsets, colors)
            plot.add_item(crv, z=0)

        win.get_itemlist_panel().show()
        win.show()
        win.exec_()

    def show_image(self):
        # def create_window():
        #     win = ImageDialog(edit=False, toolbar=True, wintitle="Amplifier {0}".format(amplifier_num),
        #                       options=dict(show_xsection=True, show_ysection=True,
        #                                    show_itemlist=True))
        #     win.resize(800, 600)
        #     return win
        #
        # _app = guidata.qapplication()
        # # --
        # filename = osp.join(osp.dirname(__file__), "brain.png")
        # win = create_window()
        # image = make.image(filename=filename, colormap="bone")
        # data2 = np.array(image.data.T[200:], copy=True)
        # image2 = make.image(data2, title="Modified", alpha_mask=True)
        # plot = win.get_plot()
        # plot.add_item(image)
        # plot.add_item(image2, z=1)
        # win.exec_()
        app = guidata.qapplication()
        win = AmpWindow()

        win.load_amplifier('all', self.e2vccd230_42.get_matrix())
        # win.load_amplifier(0, self.image.amplifiers[0].matrix)
        # win.load_amplifier(1, self.image.amplifiers[1].matrix)
        # win.load_amplifier(2, self.image.amplifiers[2].matrix)
        # win.load_amplifier(3, self.image.amplifiers[3].matrix)

        win.show()
        app.exec_()
        # pass


    def show_amplifiers(self):
        # def create_window():
        #     win = ImageDialog(edit=False, toolbar=True, wintitle="Amplifier {0}".format(amplifier_num),
        #                       options=dict(show_xsection=True, show_ysection=True,
        #                                    show_itemlist=True))
        #     win.resize(800, 600)
        #     return win
        #
        # _app = guidata.qapplication()
        # # --
        # filename = osp.join(osp.dirname(__file__), "brain.png")
        # win = create_window()
        # image = make.image(filename=filename, colormap="bone")
        # data2 = np.array(image.data.T[200:], copy=True)
        # image2 = make.image(data2, title="Modified", alpha_mask=True)
        # plot = win.get_plot()
        # plot.add_item(image)
        # plot.add_item(image2, z=1)
        # win.exec_()
        app = guidata.qapplication()
        win = AmpWindow()

        # win.load_amplifier('all', self.e2vccd230_42.get_as_matrix())
        win.load_amplifier(0, self.image.amplifiers[0].matrix)
        win.load_amplifier(1, self.image.amplifiers[1].matrix)
        win.load_amplifier(2, self.image.amplifiers[2].matrix)
        win.load_amplifier(3, self.image.amplifiers[3].matrix)

        win.show()
        win.exec()
        # pass


class PlotterWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.amplifiers = ImagePlot(self)
        self.itemlist = PlotItemList(self)
        self.contrast = ContrastAdjustment(self)
        self.manager = PlotManager(self)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.itemlist)

        gridLayout = QGridLayout()
        gridLayout.setObjectName("gridLayout")
        self.setLayout(gridLayout)

        # horizontalLayout = QHBoxLayout()
        # horizontalLayout.setObjectName("horizontalLayout")

        # items_widget = QWidget(self)
        # items_widget.setObjectName("items_widget")

        # horizontalLayout.addWidget(self.itemlist)
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(self.contrast)

        splitter2.addWidget(self.amplifiers)

        splitter1.addWidget(splitter2)
        gridLayout.addWidget(splitter1, 0, 0, 1, 1)

        self.manager.add_plot(self.amplifiers)
        for panel in (self.itemlist, self.contrast):
            self.manager.add_panel(panel)


    def register_tools(self):
        self.manager.register_all_image_tools()


class CentralWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        # layout = QGridLayout()
        # self.setLayout(layout)
        #
        # self.amplifiers = ImagePlot(self)
        #
        # layout.addWidget(self.amplifiers, 0, 0, 2, 2)
        #
        # self.contrast = ContrastAdjustment(self)
        # layout.addWidget(self.contrast, 2, 0, 1, 1)
        # self.itemlist = PlotItemList(self)
        # layout.addWidget(self.itemlist, 2, 1, 1, 1)
        #
        # self.manager = PlotManager(self)
        # self.manager.add_plot(self.amplifiers)
        # for panel in (self.itemlist, self.contrast):
        #     self.manager.add_panel(panel)
        self.parent = parent
        self.verticalLayout = QVBoxLayout()
        self.toolbar = QToolBar(self.parent)
        self.plotter = PlotterWidget(self.parent)

        self.setLayout(self.verticalLayout)

    def addPlotter(self):
        self.verticalLayout.addWidget(self.plotter)

    def addToolBar(self):
        self.plotter.manager.add_toolbar(self.toolbar, id(self.toolbar))
        self.plotter.manager.set_default_toolbar(self.toolbar)
        self.plotter.register_tools()

        self.verticalLayout.addWidget(self.toolbar)



class AmpWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # filename = osp.join(osp.dirname(__file__), "brain.png")
        # image1 = make.image(filename=filename, title="Original", colormap='gray')
        #
        # from guiqwt.tests.image import compute_image
        # image2 = make.image(compute_image())

        self.widget = CentralWidget(self)
        self.widget.addToolBar()
        self.widget.addPlotter()
        self.setCentralWidget(self.widget)

        # widget.plot1.add_item(image1)
        # widget.plot2.add_item(image2)

    def load_amplifier(self, amp_num, data, x=None, y=None):
        if None not in (x, y):
            im = make.xyimage(x, y, data)
        else:
            im = make.image(data)
        self.widget.plotter.amplifiers.add_item(im)


def test():
    """Test"""
    # -- Create QApplication
    import guidata
    app = guidata.qapplication()
    # --
    win = AmpWindow()
    win.show()
    app.exec_()
