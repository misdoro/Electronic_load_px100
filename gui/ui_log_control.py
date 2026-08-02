# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log_control.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QWidget)

class Ui_LogControl(object):
    def setupUi(self, LogControl):
        if not LogControl.objectName():
            LogControl.setObjectName(u"LogControl")
        LogControl.resize(400, 113)
        LogControl.setCheckable(True)
        self.formLayout = QFormLayout(LogControl)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(LogControl)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.logPath = QLineEdit(LogControl)
        self.logPath.setObjectName(u"logPath")

        self.horizontalLayout.addWidget(self.logPath)

        self.pathExists = QLabel(LogControl)
        self.pathExists.setObjectName(u"pathExists")

        self.horizontalLayout.addWidget(self.pathExists)

        self.selectLogPath = QPushButton(LogControl)
        self.selectLogPath.setObjectName(u"selectLogPath")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectLogPath.sizePolicy().hasHeightForWidth())
        self.selectLogPath.setSizePolicy(sizePolicy)
        self.selectLogPath.setMinimumSize(QSize(32, 32))
        self.selectLogPath.setMaximumSize(QSize(32, 32))
        self.selectLogPath.setFlat(False)

        self.horizontalLayout.addWidget(self.selectLogPath)


        self.formLayout.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.labelAutosave = QLabel(LogControl)
        self.labelAutosave.setObjectName(u"labelAutosave")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelAutosave)

        self.autosaveIntervalMin = QSpinBox(LogControl)
        self.autosaveIntervalMin.setObjectName(u"autosaveIntervalMin")
        self.autosaveIntervalMin.setMaximum(1440)
        self.autosaveIntervalMin.setValue(5)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.autosaveIntervalMin)


        self.retranslateUi(LogControl)

        QMetaObject.connectSlotsByName(LogControl)
    # setupUi

    def retranslateUi(self, LogControl):
        LogControl.setWindowTitle(QCoreApplication.translate("LogControl", u"GroupBox", None))
        LogControl.setTitle(QCoreApplication.translate("LogControl", u"Log to file", None))
        self.label.setText(QCoreApplication.translate("LogControl", u"Log path", None))
        self.pathExists.setText("")
        self.selectLogPath.setText(QCoreApplication.translate("LogControl", u"...", None))
        self.labelAutosave.setText(QCoreApplication.translate("LogControl", u"Autosave interval", None))
        self.autosaveIntervalMin.setSpecialValueText(QCoreApplication.translate("LogControl", u"Disabled", None))
        self.autosaveIntervalMin.setSuffix(QCoreApplication.translate("LogControl", u" min", None))
    # retranslateUi

