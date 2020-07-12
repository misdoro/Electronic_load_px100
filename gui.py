import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def plot(self, data, callback):

        self.callback = callback
        # plot the pandas DataFrame, passing in the
        # matplotlib Canvas axes.
        plt = data.plot(ax=self.canvas.axes,
                        x='time',
                        y='voltage',
                        secondary_y='current')

        toolbar = NavigationToolbar(self.canvas, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

    def update_plot(self):
        print("update")
        data = self.callback()

        self.canvas.axes.cla()
        data.plot(ax=self.canvas.axes,
                  x='time',
                  y='voltage',
                  secondary_y='current')
        self.canvas.draw()


class GUI:
    def __init__(self, data, callback):
        app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow()
        self.window.plot(data, callback)
        app.exec_()
