import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
from datetime import time as tm


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=7, height=4, dpi=100)
        self.setWindowTitle("Battery tester")

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def plot(self, data):
        self.ax = self.canvas.axes
        self.twinax = self.ax.twinx()
        self.update_plot()

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
        print("update_plot")
        data = self.backend.datastore.data
        if len(data) > 0:
            lastrow = data.tail(1)
            set_voltage = lastrow['set_voltage'].to_list()[0]
            time = lastrow['time'].to_list()[0]

            if time != tm(0):
                self.ax.cla()
                self.twinax.cla()
                data.plot(ax=self.ax, x='time', y=['voltage'])
                self.ax.legend(loc='center left')
                self.ax.set_ylabel('Voltage, V')
                self.ax.set_ylim(bottom=set_voltage)
                data.plot(ax=self.twinax, x='time', y=['current'], style='r')
                self.twinax.legend(loc='center right')
                self.twinax.set_ylabel('Current, A')
                self.twinax.set_ylim(0, 10)
                self.canvas.draw()

    def set_backend(self, backend):
        self.backend = backend

    def closeEvent(self, event):
        self.backend.at_exit()
        event.accept()


class GUI:
    def __init__(self, backend):
        app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow()
        self.window.set_backend(backend)
        self.window.plot(backend.datastore.data)
        app.exec_()
