# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_settingsTab(object):
    def setupUi(self, settingsTab):
        if not settingsTab.objectName():
            settingsTab.setObjectName(u"settingsTab")
        settingsTab.resize(517, 572)
        self.gridLayout_3 = QGridLayout(settingsTab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_2 = QFrame(settingsTab)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 1)

        self.frame = QFrame(settingsTab)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 1, 1, 1, 1)


        self.retranslateUi(settingsTab)

        QMetaObject.connectSlotsByName(settingsTab)
    # setupUi

    def retranslateUi(self, settingsTab):
        settingsTab.setWindowTitle(QCoreApplication.translate("settingsTab", u"Form", None))
    # retranslateUi

