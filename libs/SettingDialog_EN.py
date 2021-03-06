from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import socket
import re


class SettingDialog(QtWidgets.QDialog):
    enable_color_map = False
    label_font_size = 10
    task_mode = 0 #0=det, 1=seg, 2=cls
    signal_conn = pyqtSignal(list)

    def __init__(self, parent,config):
        QtWidgets.QDialog.__init__(self, parent)
        self.resize(320, 240)
        self.__class__.task_mode = config['task_mode']
        self.__class__.label_font_size = config['label_font_size']
        self.init_UI()
    def createModeGroup(self):
        '''
        set the trask mode setting group
        :return: mode group
        '''
        self.modegroupBox = QtWidgets.QGroupBox("& Task Mode")
        self.modegroupBox.setCheckable(True)
        self.modegroupBox.setChecked(True)
        self.CLS_mode_rb = QtWidgets.QRadioButton("CLS Mode")
        self.CLS_mode_rb.clicked.connect(self.CLS_model_selected)
        self.DET_mode_rb = QtWidgets.QRadioButton("DET Mode")
        self.DET_mode_rb.clicked.connect(self.DET_model_selected)
        self.SEG_mode_rb = QtWidgets.QRadioButton("SEG Mode")
        self.SEG_mode_rb.clicked.connect(self.SEG_model_selected)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.CLS_mode_rb)
        vbox.addWidget(self.DET_mode_rb)
        vbox.addWidget(self.SEG_mode_rb)
        vbox.addStretch(True)
        self.modegroupBox.setLayout(vbox)
        return self.modegroupBox


    
    def createDEToptGroup(self):
        self.detgroupBox = QtWidgets.QGroupBox("& DET options")
        self.enable_show_label_cb = QtWidgets.QCheckBox('enable show label name')
        self.label_font_size_sl = QtWidgets.QSlider(Qt.Horizontal)
        self.label_font_size_sl.setRange(5,50)
        self.label_font_size_sp = QtWidgets.QSpinBox()
        self.label_font_size_sp.setRange(5,50)
        self.signal_conn.connect(self.font_conn)
        self.label_font_size_sl.valueChanged.connect(self.change_label_font_size)
        self.label_font_size_sl.setValue(self.__class__.label_font_size)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.enable_show_label_cb)
        vbox.addWidget(QtWidgets.QLabel('label font size'))
        vbox.addWidget(self.label_font_size_sl)
        vbox.addWidget(self.label_font_size_sp)
        vbox.addStretch()
        self.detgroupBox.setLayout(vbox)
        return self.detgroupBox


    def font_conn(self):
        self.label_font_size_sl = QtWidgets.QSlider(Qt.Horizontal)
        self.label_font_size_sl.setRange(5,50)
        self.label_font_size_sp = QtWidgets.QSpinBox()
        self.label_font_size_sp.setRange(5,50)



    def createCLSoptGroup(self):
        self.clsgroupBox = QtWidgets.QGroupBox("& CLS options")
        #self.single_label_rb = QtGui.QRadioButton("single label")
        #self.multi_label_rb = QtGui.QRadioButton("multi label")
        vbox = QtWidgets.QVBoxLayout()
        #vbox.addWidget(self.single_label_rb)
        #vbox.addWidget(self.multi_label_rb)
        vbox.addStretch(True)
        self.clsgroupBox.setLayout(vbox)
        return self.clsgroupBox

    def createSEGoptGroup(self):
        self.seggroupBox = QtWidgets.QGroupBox("& SEG options")
        self.enable_color_map_cb = QtWidgets.QCheckBox('enable color map')
        if self.__class__.enable_color_map:
            self.enable_color_map_cb.toggle()
        self.enable_color_map_cb.stateChanged.connect(
            self.change_color_enable_state)
        if self.__class__.enable_color_map:
            self.enable_color_map_cb.setChecked(True)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.enable_color_map_cb)
        vbox.addStretch(True)
        self.seggroupBox.setLayout(vbox)
        return self.seggroupBox


    def init_UI(self):
        main_v_layout = QtWidgets.QVBoxLayout()

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.createModeGroup(),0,0)
        grid.addWidget(self.createDEToptGroup(),1,0)
        grid.addWidget(self.createCLSoptGroup(),2,0)
        grid.addWidget(self.createSEGoptGroup(),3,0)
        if self.__class__.task_mode == 0:
            self.DET_mode_rb.setChecked(True)
            self.DET_model_selected()
        elif self.__class__.task_mode == 1:
            self.SEG_mode_rb.setChecked(True)
            self.SEG_model_selected()
        elif self.__class__.task_mode == 2:
            self.CLS_mode_rb.setChecked(True)
            self.CLS_model_selected()
        buttonBox = QtWidgets.QDialogButtonBox(parent=self)
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        main_v_layout.addLayout(grid)
        spacerItem = QtWidgets.QSpacerItem(
            20, 48, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        main_v_layout.addItem(spacerItem)
        main_v_layout.addWidget(buttonBox)
        self.setLayout(main_v_layout)

    def CLS_model_selected(self):
        self.__class__.task_mode = 2
        self.clsgroupBox.setDisabled(False)
        self.detgroupBox.setDisabled(True)
        self.seggroupBox.setDisabled(True)

    def DET_model_selected(self):
        self.__class__.task_mode = 0
        self.detgroupBox.setDisabled(False)
        self.clsgroupBox.setDisabled(True)
        self.seggroupBox.setDisabled(True)

    def SEG_model_selected(self):
        self.__class__.task_mode = 1
        self.seggroupBox.setDisabled(False)
        self.detgroupBox.setDisabled(True)
        self.clsgroupBox.setDisabled(True)

    def change_color_enable_state(self, state):
        if state == QtWidgets.Qt.Checked:
            self.__class__.enable_color_map = True
        else:
            self.__class__.enable_color_map = False
    def change_label_font_size(self,value):
        self.__class__.label_font_size = value

    def get_color_map_state(self):
        return self.__class__.enable_color_map

    def get_setting_state(self):
        if self.__class__.task_mode == 0:
            return {'mode': 0,'enable_color_map':self.__class__.enable_color_map,'label_font_size': self.__class__.label_font_size}

        elif self.__class__.task_mode == 1:
            return {'mode': 1,'enable_color_map':self.__class__.enable_color_map}

        elif self.__class__.task_mode == 2:
            return {'mode': 2}

