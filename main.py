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

        N = self.data.shape[1]
        self.A, self.B, self.C = 2, N // 2, N // 2  # sound source location

        self.z_slice = self.A
        self.y_slice = self.B
        self.x_slice = self.C

        self.init_ui()
        self.qt_connections()

    def init_ui(self):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('imageAxisOrder', 'row-major')

        self.z_axis_name = ('Head', 'Feet')
        self.y_axis_name = ('Face', 'Back')
        self.x_axis_name = ('Left Hand', 'Right Hand')


        self.layout = QtGui.QVBoxLayout()

        # self.setGeometry(50, 50, 700, 700)
        self.setWindowTitle('Lungs Model')


        self.z_slice_label = QtGui.QLabel(f'Z axis [{self.z_axis_name[0]} - {self.z_axis_name[1]}] Slice: {self.z_slice + 1}/{self.data.shape[0]}')
        self.y_slice_label = QtGui.QLabel(f'Y axis [{self.y_axis_name[0]} - {self.y_axis_name[1]}] Slice: {self.y_slice + 1}/{self.data.shape[1]}')
        self.x_slice_label = QtGui.QLabel(f'X axis [{self.x_axis_name[0]} - {self.x_axis_name[1]}] Slice: {self.x_slice + 1}/{self.data.shape[2]}')


        # slices plots ----------------------------------------------------------------
        
        self.autolevels = True
        self.levels = (0, 100)
        self.glayout = pg.GraphicsLayoutWidget()
        self.glayout.ci.layout.setContentsMargins(0, 0, 0, 0)
        self.glayout.ci.layout.setSpacing(0)
        self.z_slice_img = pg.ImageItem(self.data[self.z_slice, :, :], autoLevels=self.autolevels, levels=self.levels, border=pg.mkPen(color='r', width=3))
        self.y_slice_img = pg.ImageItem(self.data[:, self.y_slice, :], autoLevels=self.autolevels, levels=self.levels, border=pg.mkPen(color='g', width=3))
        self.x_slice_img = pg.ImageItem(self.data[:, :, self.x_slice], autoLevels=self.autolevels, levels=self.levels, border=pg.mkPen(color='b', width=3))
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
        self.z_slice_plot_y_helper1 = self.z_slice_plot.plot([0               , self.data.shape[2] ], [self.y_slice    , self.y_slice      ], pen='g')
        self.z_slice_plot_y_helper2 = self.z_slice_plot.plot([0               , self.data.shape[2] ], [self.y_slice + 1, self.y_slice + 1  ], pen='g')
        self.z_slice_plot_x_helper1 = self.z_slice_plot.plot([self.x_slice    , self.x_slice       ], [0               , self.data.shape[1]], pen='b')
        self.z_slice_plot_x_helper2 = self.z_slice_plot.plot([self.x_slice + 1, self.x_slice + 1   ], [0               , self.data.shape[1]], pen='b')
        self.y_slice_plot_z_helper1 = self.y_slice_plot.plot([0               , self.data.shape[2] ], [self.z_slice    , self.z_slice      ], pen='r')
        self.y_slice_plot_z_helper2 = self.y_slice_plot.plot([0               , self.data.shape[2] ], [self.z_slice + 1, self.z_slice + 1  ], pen='r')
        self.y_slice_plot_x_helper1 = self.y_slice_plot.plot([self.x_slice    , self.x_slice       ], [0               , self.data.shape[0]], pen='b')
        self.y_slice_plot_x_helper2 = self.y_slice_plot.plot([self.x_slice + 1, self.x_slice + 1   ], [0               , self.data.shape[0]], pen='b')
        self.x_slice_plot_z_helper1 = self.x_slice_plot.plot([0               , self.data.shape[1] ], [self.z_slice    , self.z_slice      ], pen='r')
        self.x_slice_plot_z_helper2 = self.x_slice_plot.plot([0               , self.data.shape[1] ], [self.z_slice + 1, self.z_slice + 1  ], pen='r')
        self.x_slice_plot_y_helper1 = self.x_slice_plot.plot([self.y_slice    , self.y_slice       ], [0               , self.data.shape[0]], pen='g')
        self.x_slice_plot_y_helper2 = self.x_slice_plot.plot([self.y_slice + 1, self.y_slice + 1   ], [0               , self.data.shape[0]], pen='g')
        self.z_slice_plot.invertY(True)
        self.y_slice_plot.invertY(True)
        self.x_slice_plot.invertY(True)
        self.z_slice_plot.setLabel('bottom', f'X axis [{self.x_axis_name[0]} - {self.x_axis_name[1]}]')
        self.z_slice_plot.setLabel('left'  , f'Y axis [{self.y_axis_name[1]} - {self.y_axis_name[0]}]')
        self.y_slice_plot.setLabel('bottom', f'X axis [{self.x_axis_name[0]} - {self.x_axis_name[1]}]')
        self.y_slice_plot.setLabel('left'  , f'Z axis [{self.z_axis_name[1]} - {self.z_axis_name[0]}]')
        self.x_slice_plot.setLabel('bottom', f'Y axis [{self.y_axis_name[0]} - {self.y_axis_name[1]}]')
        self.x_slice_plot.setLabel('left'  , f'Z axis [{self.z_axis_name[1]} - {self.z_axis_name[0]}]')
        self.z_slice_plot.addItem(self.z_slice_img)
        self.y_slice_plot.addItem(self.y_slice_img)
        self.x_slice_plot.addItem(self.x_slice_img)
        self.z_slice_img.setRect(pg.QtCore.QRectF(0, 0, self.data.shape[2], self.data.shape[1]))
        self.y_slice_img.setRect(pg.QtCore.QRectF(0, 0, self.data.shape[2], self.data.shape[0]))
        self.x_slice_img.setRect(pg.QtCore.QRectF(0, 0, self.data.shape[1], self.data.shape[0]))
        self.z_slice_img.setZValue(-1)
        self.y_slice_img.setZValue(-1)
        self.x_slice_img.setZValue(-1)



        self.z_slice_slider = QtGui.QSlider()
        self.z_slice_slider.setStyleSheet('background-color: rgba(255, 0, 0, 0.2)')
        self.z_slice_slider.setOrientation(QtCore.Qt.Horizontal)
        self.z_slice_slider.setRange(0, self.data.shape[0] - 1)
        self.z_slice_slider.setValue(self.z_slice)
        self.z_slice_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.z_slice_slider.setTickInterval(1)
        
        self.y_slice_slider = QtGui.QSlider()
        self.y_slice_slider.setStyleSheet('background-color: rgba(0, 255, 0, 0.2)')
        self.y_slice_slider.setOrientation(QtCore.Qt.Horizontal)
        self.y_slice_slider.setRange(0, self.data.shape[1] - 1)
        self.y_slice_slider.setValue(self.y_slice)
        self.y_slice_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.y_slice_slider.setTickInterval(1)

        self.x_slice_slider = QtGui.QSlider()
        self.x_slice_slider.setStyleSheet('background-color: rgba(0, 0, 255, 0.2)')
        self.x_slice_slider.setOrientation(QtCore.Qt.Horizontal)
        self.x_slice_slider.setRange(0, self.data.shape[2] - 1)
        self.x_slice_slider.setValue(self.x_slice)
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

        self.setGeometry(0, 0, 1440, 900)
        # self.setGeometry(0, 0, 1200, 900)
        self.show()

    def qt_connections(self):
        self.z_slice_slider.valueChanged.connect(self.z_slice_slider_changed)
        self.y_slice_slider.valueChanged.connect(self.y_slice_slider_changed)
        self.x_slice_slider.valueChanged.connect(self.x_slice_slider_changed)
        self.steps_state.connect(self.update_steps_progress_bar)

    # def mouseMoved(self, event):
        # print('mouseMoved event')

    def mouseMoveEvent(self, ev):
        print('pp')

    def l_spin_value_changed(self):
        self.model.l = self.l_spin.value()

    def h_spin_value_changed(self):
        self.model.h = self.h_spin.value()
    
    def f_spin_value_changed(self):
        self.model.f = self.f_spin.value()

    @QtCore.pyqtSlot(int)
    def update_steps_progress_bar(self, current_step):
        self.steps_progress_bar.setValue(current_step / self.steps_spin.value() * 100)
        QApplication.processEvents() 

    def reset_params(self):
        self.z_slice = self.model.A
        self.y_slice = self.model.B
        self.x_slice = self.model.C
        self.z_slice_slider.setValue(self.z_slice)
        self.y_slice_slider.setValue(self.y_slice)
        self.x_slice_slider.setValue(self.x_slice)

        self.arrays_to_vis[0].setChecked(True)
        self.array_to_vis_changed()


    def array_to_vis_changed(self):
        
        mapping = {
            'P' : self.model.P,
            'r' : self.model.r,
            'ro': self.model.ro,
            'c' : self.model.c,
            'K' : self.model.K,
        }

        for r in self.arrays_to_vis:
            if r.isChecked():
                self.data = mapping[r.text()]
                self.z_slice_img.setImage(self.data[self.z_slice      ])
                self.y_slice_img.setImage(self.data[:, self.y_slice, :])
                self.x_slice_img.setImage(self.data[:, :, self.x_slice])

    def print_mean(self):
        # pass
        print(f'slices mean Z, Y, X   {np.mean(self.data[self.z_slice]):8.3e}    {np.mean(self.data[:, self.y_slice, :]):8.3e}    {np.mean(self.data[:, :, self.x_slice]):8.3e}    cube mean: {np.mean(self.data):8.3e}')

    def do_steps(self):
        for i in range(self.steps_spin.value()):
            self.model.step()

            self.z_slice_img.setImage(self.data[self.z_slice      ])
            self.y_slice_img.setImage(self.data[:, self.y_slice, :])
            self.x_slice_img.setImage(self.data[:, :, self.x_slice])
           
            self.source_curve.setData(self.model.source_signal)
            self.observ_curve.setData(self.model.observ_signal)

            self.observ_slice = np.roll(self.observ_slice, -1)
            self.observ_slice[-1] = self.model.P[self.z_slice, self.y_slice, self.x_slice]
            self.observ_slice_curve.setData(self.observ_slice)

            self.steps_state.emit(i + 1)
            self.print_mean()
        self.steps_state.emit(0)       

    def wheelEvent(self, event):
        if self.z_slice_img.sceneBoundingRect().contains(self.glayout.mapFromParent(event.pos())):
            self.z_slice = np.clip(self.z_slice + np.sign(event.angleDelta().y()), 0, self.data.shape[0] - 1) # change bounds 0..N-1 => 1..N
            self.z_slice_slider.setValue(self.z_slice)
        elif self.y_slice_img.sceneBoundingRect().contains(self.glayout.mapFromParent(event.pos())):
            self.y_slice = np.clip(self.y_slice + np.sign(event.angleDelta().y()), 0, self.data.shape[1] - 1) # change bounds 0..N-1 => 1..N
            self.y_slice_slider.setValue(self.y_slice)
        elif self.x_slice_img.sceneBoundingRect().contains(self.glayout.mapFromParent(event.pos())):
            self.x_slice = np.clip(self.x_slice + np.sign(event.angleDelta().y()), 0, self.data.shape[2] - 1) # change bounds 0..N-1 => 1..N
            self.x_slice_slider.setValue(self.x_slice)

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent and event.key() == QtCore.Qt.Key_Up:
            self.do_steps()
            #here accept the event and do something
            # self.record_values_button_clicked()
            event.accept()
        else:
            event.ignore()



    def update_slice_helpers_lines(self):
        # self.z_slice_plot_y_helper.setData([0           , self.data.shape[2] ], [self.y_slice, self.y_slice      ])
        # self.z_slice_plot_x_helper.setData([self.x_slice, self.x_slice       ], [0           , self.data.shape[1]])
        # self.y_slice_plot_z_helper.setData([0           , self.data.shape[2] ], [self.z_slice, self.z_slice      ])
        # self.y_slice_plot_x_helper.setData([self.x_slice, self.x_slice       ], [0           , self.data.shape[0]])
        # self.x_slice_plot_z_helper.setData([0           , self.data.shape[1] ], [self.z_slice, self.z_slice      ])
        # self.x_slice_plot_y_helper.setData([self.y_slice, self.y_slice       ], [0           , self.data.shape[0]])
        self.z_slice_plot_y_helper1.setData([0               , self.data.shape[2] ], [self.y_slice    , self.y_slice      ])
        self.z_slice_plot_y_helper2.setData([0               , self.data.shape[2] ], [self.y_slice + 1, self.y_slice + 1  ])
        self.z_slice_plot_x_helper1.setData([self.x_slice    , self.x_slice       ], [0               , self.data.shape[1]])
        self.z_slice_plot_x_helper2.setData([self.x_slice + 1, self.x_slice + 1   ], [0               , self.data.shape[1]])
        self.y_slice_plot_z_helper1.setData([0               , self.data.shape[2] ], [self.z_slice    , self.z_slice      ])
        self.y_slice_plot_z_helper2.setData([0               , self.data.shape[2] ], [self.z_slice + 1, self.z_slice + 1  ])
        self.y_slice_plot_x_helper1.setData([self.x_slice    , self.x_slice       ], [0               , self.data.shape[0]])
        self.y_slice_plot_x_helper2.setData([self.x_slice + 1, self.x_slice + 1   ], [0               , self.data.shape[0]])
        self.x_slice_plot_z_helper1.setData([0               , self.data.shape[1] ], [self.z_slice    , self.z_slice      ])
        self.x_slice_plot_z_helper2.setData([0               , self.data.shape[1] ], [self.z_slice + 1, self.z_slice + 1  ])
        self.x_slice_plot_y_helper1.setData([self.y_slice    , self.y_slice       ], [0               , self.data.shape[0]])
        self.x_slice_plot_y_helper2.setData([self.y_slice + 1, self.y_slice + 1   ], [0               , self.data.shape[0]])

    def z_slice_slider_changed(self):
        self.z_slice = self.z_slice_slider.value()
        self.z_slice_label.setText(f'Z axis [{self.z_axis_name[0]} - {self.z_axis_name[1]}] Slice: {self.z_slice + 1}/{self.data.shape[0]}')
        self.z_slice_img.setImage(self.data[self.z_slice])
        self.print_mean()
        self.update_slice_helpers_lines()

    def y_slice_slider_changed(self):
        self.y_slice = self.y_slice_slider.value()
        self.y_slice_label.setText(f'Y axis [{self.y_axis_name[0]} - {self.y_axis_name[1]}] Slice: {self.y_slice + 1}/{self.data.shape[1]}')
        self.y_slice_img.setImage(self.data[:, self.y_slice, :])
        self.print_mean()
        self.update_slice_helpers_lines()

    def x_slice_slider_changed(self):
        self.x_slice = self.x_slice_slider.value()
        self.x_slice_label.setText(f'X axis [{self.x_axis_name[0]} - {self.x_axis_name[1]}] Slice: {self.x_slice + 1}/{self.data.shape[2]}')
        self.x_slice_img.setImage(self.data[:, :, self.x_slice])
        self.print_mean()
        self.update_slice_helpers_lines()




app = QtGui.QApplication(sys.argv)
# print(sys.argv[1])
gui = AppGUI()
signal.signal(signal.SIGINT, signal.SIG_DFL)
sys.exit(app.exec())
