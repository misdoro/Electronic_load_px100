# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDateTimeEdit, QDoubleSpinBox,
    QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QTabWidget, QTimeEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(985, 700)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabs = QTabWidget(self.centralwidget)
        self.tabs.setObjectName(u"tabs")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabs.sizePolicy().hasHeightForWidth())
        self.tabs.setSizePolicy(sizePolicy)
        self.tab1 = QWidget()
        self.tab1.setObjectName(u"tab1")
        self.horizontalLayout_2 = QHBoxLayout(self.tab1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.plot_placeholder = QWidget(self.tab1)
        self.plot_placeholder.setObjectName(u"plot_placeholder")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(9)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plot_placeholder.sizePolicy().hasHeightForWidth())
        self.plot_placeholder.setSizePolicy(sizePolicy1)
        self.plot_placeholder.setMinimumSize(QSize(600, 400))

        self.horizontalLayout_2.addWidget(self.plot_placeholder)

        self.controlsLayout = QVBoxLayout()
        self.controlsLayout.setObjectName(u"controlsLayout")
        self.ranges = QGroupBox(self.tab1)
        self.ranges.setObjectName(u"ranges")
        self.formLayout = QFormLayout(self.ranges)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label = QLabel(self.ranges)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.label_2 = QLabel(self.ranges)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.set_current = QDoubleSpinBox(self.ranges)
        self.set_current.setObjectName(u"set_current")
        self.set_current.setMinimumSize(QSize(90, 0))
        self.set_current.setBaseSize(QSize(90, 0))
        self.set_current.setSingleStep(0.100000000000000)
        self.set_current.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.set_current)

        self.label_7 = QLabel(self.ranges)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.set_timer = QTimeEdit(self.ranges)
        self.set_timer.setObjectName(u"set_timer")
        self.set_timer.setEnabled(True)
        self.set_timer.setMinimumSize(QSize(90, 0))
        self.set_timer.setBaseSize(QSize(90, 0))
        self.set_timer.setCurrentSection(QDateTimeEdit.HourSection)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.set_timer)

        self.label_8 = QLabel(self.ranges)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.cellLabel = QLineEdit(self.ranges)
        self.cellLabel.setObjectName(u"cellLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cellLabel.sizePolicy().hasHeightForWidth())
        self.cellLabel.setSizePolicy(sizePolicy2)
        self.cellLabel.setMinimumSize(QSize(90, 0))
        self.cellLabel.setBaseSize(QSize(90, 0))
        self.cellLabel.setMaxLength(10)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.cellLabel)

        self.set_voltage = QDoubleSpinBox(self.ranges)
        self.set_voltage.setObjectName(u"set_voltage")
        self.set_voltage.setMinimumSize(QSize(90, 0))
        self.set_voltage.setBaseSize(QSize(90, 0))
        self.set_voltage.setSingleStep(0.100000000000000)
        self.set_voltage.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.set_voltage)


        self.controlsLayout.addWidget(self.ranges)

        self.groupBox = QGroupBox(self.tab1)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout_2 = QFormLayout(self.groupBox)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.readVoltage = QLabel(self.groupBox)
        self.readVoltage.setObjectName(u"readVoltage")
        palette = QPalette()
        brush = QBrush(QColor(0, 85, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(160, 162, 162, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.readVoltage.setPalette(palette)
        font = QFont()
        font.setPointSize(16)
        self.readVoltage.setFont(font)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.readVoltage)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.readCurrent = QLabel(self.groupBox)
        self.readCurrent.setObjectName(u"readCurrent")
        palette1 = QPalette()
        brush2 = QBrush(QColor(170, 0, 0, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.readCurrent.setPalette(palette1)
        self.readCurrent.setFont(font)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.readCurrent)

        self.readCapAH = QLabel(self.groupBox)
        self.readCapAH.setObjectName(u"readCapAH")
        self.readCapAH.setFont(font)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.readCapAH)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.readCapWH = QLabel(self.groupBox)
        self.readCapWH.setObjectName(u"readCapWH")
        self.readCapWH.setFont(font)

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.readCapWH)

        self.readTime = QLabel(self.groupBox)
        self.readTime.setObjectName(u"readTime")
        self.readTime.setFont(font)

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.FieldRole, self.readTime)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_9)


        self.controlsLayout.addWidget(self.groupBox)

        self.resetButton = QPushButton(self.tab1)
        self.resetButton.setObjectName(u"resetButton")

        self.controlsLayout.addWidget(self.resetButton)


        self.horizontalLayout_2.addLayout(self.controlsLayout)

        self.tabs.addTab(self.tab1, "")

        self.gridLayout.addWidget(self.tabs, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Battery tester", None))
        self.ranges.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Voltage", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Current", None))
        self.set_current.setSuffix(QCoreApplication.translate("MainWindow", u" A", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Timer", None))
        self.set_timer.setDisplayFormat(QCoreApplication.translate("MainWindow", u"h:mm:ss", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Label", None))
        self.cellLabel.setText(QCoreApplication.translate("MainWindow", u"B1", None))
        self.set_voltage.setPrefix("")
        self.set_voltage.setSuffix(QCoreApplication.translate("MainWindow", u" V", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Readings", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Voltage", None))
        self.readVoltage.setText(QCoreApplication.translate("MainWindow", u"0.0 V", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Current", None))
        self.readCurrent.setText(QCoreApplication.translate("MainWindow", u"0.0 A", None))
        self.readCapAH.setText(QCoreApplication.translate("MainWindow", u"0.0 AH", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Capacity", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Capacity", None))
        self.readCapWH.setText(QCoreApplication.translate("MainWindow", u"0.0 WH", None))
        self.readTime.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab1), QCoreApplication.translate("MainWindow", u"Main", None))
    # retranslateUi

