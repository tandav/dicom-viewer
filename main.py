from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtGui import QApplication
import pyqtgraph as pg
import numpy as np
import sys
import signal




class AppGUI(QtGui.QWidget):
    steps_state = QtCore.pyqtSignal([int])

    def __init__(self):
        super().__init__()

        # self.data = self.model.ro
        self.data = np.load('cube.npy')
        self.X = self.data

        N = self.data.shape[1]
        self.A, self.B, self.C = 2, N // 2, N // 2  # sound source location
        self.slice = 2, N // 2, N // 2 # sound source location

        self.z = self.A
        self.y = self.B
        self.x = self.C


        self.init_ui()
        self.qt_connections()

    def init_ui(self):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('imageAxisOrder', 'row-major')

        self.zname = ('Head', 'Feet')
        self.yname = ('Face', 'Back')
        self.xname = ('Left Hand', 'Right Hand')


        self.layout = QtGui.QVBoxLayout()

        self.setGeometry(0, 0, 1440, 900)
        self.setWindowTitle('Lungs Model')


        self.z_slice_label = QtGui.QLabel(f'Z axis [{self.zname[0]} - {self.zname[1]}] Slice: {self.z + 1}/{self.data.shape[0]}')
        self.y_slice_label = QtGui.QLabel(f'Y axis [{self.yname[0]} - {self.yname[1]}] Slice: {self.y + 1}/{self.data.shape[1]}')
        self.x_slice_label = QtGui.QLabel(f'X axis [{self.xname[0]} - {self.xname[1]}] Slice: {self.x + 1}/{self.data.shape[2]}')


        # slices plots ----------------------------------------------------------------
        
        self.autolevels = True
        self.levels = (0, 100)
        self.glayout = pg.GraphicsLayoutWidget()
        self.glayout.ci.layout.setContentsMargins(0, 0, 0, 0)
        self.glayout.ci.layout.setSpacing(0)

        self.zi = pg.ImageItem(self.X[self.slice[0], :            , :            ], autoLevels=self.autolevels, levels=self.levels, border=pg.mkPen(color='r', width=3))
        self.yi = pg.ImageItem(self.X[:            , self.slice[1], :            ], autoLevels=self.autolevels, levels=self.levels, border=pg.mkPen(color='g', width=3))
        self.xi = pg.ImageItem(self.X[:,             :            , self.slice[2]], autoLevels=self.autolevels, levels=self.levels, border=pg.mkPen(color='b', width=3))

        self.z_slice_plot = self.glayout.addPlot()
        self.y_slice_plot = self.glayout.addPlot()
        self.x_slice_plot = self.glayout.addPlot()
        # self.z_slice_plot.setTitle(f'Z axis [{self.z_axis_name[0]} - {self.z_axis_name[1]}]')
        # self.y_slice_plot.setTitle(f'Y axis [{self.y_axis_name[0]} - {self.y_axis_name[1]}]')
        # self.x_slice_plot.setTitle(f'X axis [{self.x_axis_name[0]} - {self.x_axis_name[1]}]')
        self.z_slice_plot.setAspectLocked()
        self.y_slice_plot.setAspectLocked()
        self.x_slice_plot.setAspectLocked()

        self.z_slice_plot.setMouseEnabled(x=False, y=False)
        self.y_slice_plot.setMouseEnabled(x=False, y=False)
        self.x_slice_plot.setMouseEnabled(x=False, y=False)

        self.z_slice_plot_y_helper1 = self.z_slice_plot.plot([0        ,  self.X.shape[2]], [self.y    , self.y         ], pen='g')
        self.z_slice_plot_y_helper2 = self.z_slice_plot.plot([0        ,  self.X.shape[2]], [self.y + 1, self.y + 1     ], pen='g')
        self.z_slice_plot_x_helper1 = self.z_slice_plot.plot([self.x   ,  self.x         ], [0         , self.X.shape[1]], pen='b')
        self.z_slice_plot_x_helper2 = self.z_slice_plot.plot([self.x + 1, self.x + 1     ], [0         , self.X.shape[1]], pen='b')
        self.y_slice_plot_z_helper1 = self.y_slice_plot.plot([0        ,  self.X.shape[2]], [self.z    , self.z         ], pen='r')
        self.y_slice_plot_z_helper2 = self.y_slice_plot.plot([0        ,  self.X.shape[2]], [self.z + 1, self.z + 1     ], pen='r')
        self.y_slice_plot_x_helper1 = self.y_slice_plot.plot([self.x    , self.x         ], [0         , self.X.shape[0]], pen='b')
        self.y_slice_plot_x_helper2 = self.y_slice_plot.plot([self.x + 1, self.x + 1     ], [0         , self.X.shape[0]], pen='b')
        self.x_slice_plot_z_helper1 = self.x_slice_plot.plot([0        ,  self.X.shape[1]], [self.z    , self.z         ], pen='r')
        self.x_slice_plot_z_helper2 = self.x_slice_plot.plot([0        ,  self.X.shape[1]], [self.z + 1, self.z + 1     ], pen='r')
        self.x_slice_plot_y_helper1 = self.x_slice_plot.plot([self.y    , self.y         ], [0         , self.X.shape[0]], pen='g')
        self.x_slice_plot_y_helper2 = self.x_slice_plot.plot([self.y + 1, self.y + 1     ], [0         , self.X.shape[0]], pen='g')

        self.z_slice_plot.invertY(True)
        self.y_slice_plot.invertY(True)
        self.x_slice_plot.invertY(True)

        self.z_slice_plot.setLabel('bottom', f'X axis [{self.xname[0]} - {self.xname[1]}]')
        self.y_slice_plot.setLabel('bottom', f'X axis [{self.xname[0]} - {self.xname[1]}]')
        self.z_slice_plot.setLabel('left'  , f'Y axis [{self.yname[1]} - {self.yname[0]}]')
        self.x_slice_plot.setLabel('bottom', f'Y axis [{self.yname[0]} - {self.yname[1]}]')
        self.y_slice_plot.setLabel('left'  , f'Z axis [{self.zname[1]} - {self.zname[0]}]')
        self.x_slice_plot.setLabel('left'  , f'Z axis [{self.zname[1]} - {self.zname[0]}]')

        self.z_slice_plot.addItem(self.zi)
        self.y_slice_plot.addItem(self.yi)
        self.x_slice_plot.addItem(self.xi)

        self.zi.setRect(pg.QtCore.QRectF(0, 0, self.data.shape[2], self.data.shape[1]))
        self.yi.setRect(pg.QtCore.QRectF(0, 0, self.data.shape[2], self.data.shape[0]))
        self.xi.setRect(pg.QtCore.QRectF(0, 0, self.data.shape[1], self.data.shape[0]))

        self.zi.setZValue(-1)
        self.yi.setZValue(-1)
        self.xi.setZValue(-1)


        self.z_slice_slider = QtGui.QSlider()
        self.z_slice_slider.setStyleSheet('background-color: rgba(255, 0, 0, 0.2)')
        self.z_slice_slider.setOrientation(QtCore.Qt.Horizontal)
        self.z_slice_slider.setRange(0, self.data.shape[0] - 1)
        self.z_slice_slider.setValue(self.z)
        self.z_slice_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.z_slice_slider.setTickInterval(1)
        
        self.y_slice_slider = QtGui.QSlider()
        self.y_slice_slider.setStyleSheet('background-color: rgba(0, 255, 0, 0.2)')
        self.y_slice_slider.setOrientation(QtCore.Qt.Horizontal)
        self.y_slice_slider.setRange(0, self.data.shape[1] - 1)
        self.y_slice_slider.setValue(self.y)
        self.y_slice_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.y_slice_slider.setTickInterval(1)

        self.x_slice_slider = QtGui.QSlider()
        self.x_slice_slider.setStyleSheet('background-color: rgba(0, 0, 255, 0.2)')
        self.x_slice_slider.setOrientation(QtCore.Qt.Horizontal)
        self.x_slice_slider.setRange(0, self.data.shape[2] - 1)
        self.x_slice_slider.setValue(self.x)
        self.x_slice_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.x_slice_slider.setTickInterval(1)

        self.layout.addWidget(self.z_slice_label)
        self.layout.addWidget(self.z_slice_slider)
        self.layout.addWidget(self.y_slice_label)
        self.layout.addWidget(self.y_slice_slider)
        self.layout.addWidget(self.x_slice_label)
        self.layout.addWidget(self.x_slice_slider)
        self.layout.addWidget(self.glayout)

        self.setLayout(self.layout)

        self.show()

    def qt_connections(self):
        self.z_slice_slider.valueChanged.connect(self.z_slice_slider_changed)
        self.y_slice_slider.valueChanged.connect(self.y_slice_slider_changed)
        self.x_slice_slider.valueChanged.connect(self.x_slice_slider_changed)
        self.steps_state.connect(self.update_steps_progress_bar)

    @QtCore.pyqtSlot(int)
    def update_steps_progress_bar(self, current_step):
        self.steps_progress_bar.setValue(current_step / self.steps_spin.value() * 100)
        QApplication.processEvents() 


    def wheelEvent(self, event):
        if self.zi.sceneBoundingRect().contains(self.glayout.mapFromParent(event.pos())):
            self.z = np.clip(self.z + np.sign(event.angleDelta().y()), 0, self.data.shape[0] - 1) # change bounds 0..N-1 => 1..N
            self.z_slice_slider.setValue(self.z)
        elif self.yi.sceneBoundingRect().contains(self.glayout.mapFromParent(event.pos())):
            self.y = np.clip(self.y + np.sign(event.angleDelta().y()), 0, self.data.shape[1] - 1) # change bounds 0..N-1 => 1..N
            self.y_slice_slider.setValue(self.y)
        elif self.xi.sceneBoundingRect().contains(self.glayout.mapFromParent(event.pos())):
            self.x = np.clip(self.x + np.sign(event.angleDelta().y()), 0, self.data.shape[2] - 1) # change bounds 0..N-1 => 1..N
            self.x_slice_slider.setValue(self.x)


    def update_slice_helpers_lines(self):
        # self.z_slice_plot_y_helper.setData([0           , self.data.shape[2] ], [self.y_slice, self.y_slice      ])
        # self.z_slice_plot_x_helper.setData([self.x_slice, self.x_slice       ], [0           , self.data.shape[1]])
        # self.y_slice_plot_z_helper.setData([0           , self.data.shape[2] ], [self.z_slice, self.z_slice      ])
        # self.y_slice_plot_x_helper.setData([self.x_slice, self.x_slice       ], [0           , self.data.shape[0]])
        # self.x_slice_plot_z_helper.setData([0           , self.data.shape[1] ], [self.z_slice, self.z_slice      ])
        # self.x_slice_plot_y_helper.setData([self.y_slice, self.y_slice       ], [0           , self.data.shape[0]])
        self.z_slice_plot_y_helper1.setData([0               , self.X.shape[2]], [self.y    , self.y         ])
        self.z_slice_plot_y_helper2.setData([0               , self.X.shape[2]], [self.y + 1, self.y + 1     ])
        self.z_slice_plot_x_helper1.setData([self.x          , self.x         ], [0         , self.X.shape[1]])
        self.z_slice_plot_x_helper2.setData([self.x + 1      , self.x + 1     ], [0         , self.X.shape[1]])
        self.y_slice_plot_z_helper1.setData([0               , self.X.shape[2]], [self.z    , self.z         ])
        self.y_slice_plot_z_helper2.setData([0               , self.X.shape[2]], [self.z + 1, self.z + 1     ])
        self.y_slice_plot_x_helper1.setData([self.x          , self.x         ], [0         , self.X.shape[0]])
        self.y_slice_plot_x_helper2.setData([self.x + 1      , self.x + 1     ], [0         , self.X.shape[0]])
        self.x_slice_plot_z_helper1.setData([0               , self.X.shape[1]], [self.z    , self.z         ])
        self.x_slice_plot_z_helper2.setData([0               , self.X.shape[1]], [self.z + 1, self.z + 1     ])
        self.x_slice_plot_y_helper1.setData([self.y          , self.y         ], [0         , self.X.shape[0]])
        self.x_slice_plot_y_helper2.setData([self.y + 1      , self.y + 1     ], [0         , self.X.shape[0]])

    def z_slice_slider_changed(self):
        self.z = self.z_slice_slider.value()
        self.z_slice_label.setText(f'Z axis [{self.zname[0]} - {self.zname[1]}] Slice: {self.z + 1}/{self.X.shape[0]}')
        self.zi.setImage(self.X[self.z, :, :])
        self.update_slice_helpers_lines()

    def y_slice_slider_changed(self):
        self.y = self.y_slice_slider.value()
        self.y_slice_label.setText(f'Y axis [{self.yname[0]} - {self.yname[1]}] Slice: {self.y + 1}/{self.X.shape[1]}')
        self.yi.setImage(self.X[:, self.y, :])
        self.update_slice_helpers_lines()

    def x_slice_slider_changed(self):
        self.x = self.x_slice_slider.value()
        self.x_slice_label.setText(f'X axis [{self.xname[0]} - {self.xname[1]}] Slice: {self.x + 1}/{self.X.shape[2]}')
        self.xi.setImage(self.X[:, :, self.x])
        self.update_slice_helpers_lines()




app = QtGui.QApplication(sys.argv)
# print(sys.argv[1])
gui = AppGUI()
signal.signal(signal.SIGINT, signal.SIG_DFL)
sys.exit(app.exec())
