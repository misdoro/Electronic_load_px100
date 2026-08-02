# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'swcccv.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDoubleSpinBox, QFormLayout,
    QGroupBox, QLabel, QSizePolicy, QWidget)

class Ui_SwCCCV(object):
    def setupUi(self, SwCCCV):
        if not SwCCCV.objectName():
            SwCCCV.setObjectName(u"SwCCCV")
        SwCCCV.resize(195, 190)
        SwCCCV.setCheckable(True)
        self.formLayout_2 = QFormLayout(SwCCCV)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.baseCurrent = QDoubleSpinBox(SwCCCV)
        self.baseCurrent.setObjectName(u"baseCurrent")
        self.baseCurrent.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.baseCurrent)

        self.label_2 = QLabel(SwCCCV)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.label_5 = QLabel(SwCCCV)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.minCurrent = QDoubleSpinBox(SwCCCV)
        self.minCurrent.setObjectName(u"minCurrent")
        self.minCurrent.setSingleStep(0.100000000000000)
        self.minCurrent.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.minCurrent)

        self.label_3 = QLabel(SwCCCV)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.stepMultiplier = QDoubleSpinBox(SwCCCV)
        self.stepMultiplier.setObjectName(u"stepMultiplier")
        self.stepMultiplier.setMaximum(0.990000000000000)
        self.stepMultiplier.setSingleStep(0.050000000000000)
        self.stepMultiplier.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.stepMultiplier)

        self.label_4 = QLabel(SwCCCV)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.targetVoltage = QDoubleSpinBox(SwCCCV)
        self.targetVoltage.setObjectName(u"targetVoltage")
        self.targetVoltage.setSingleStep(0.100000000000000)
        self.targetVoltage.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.targetVoltage)


        self.retranslateUi(SwCCCV)

        QMetaObject.connectSlotsByName(SwCCCV)
    # setupUi

    def retranslateUi(self, SwCCCV):
        SwCCCV.setTitle(QCoreApplication.translate("SwCCCV", u"Software CC-CV", None))
        self.baseCurrent.setSuffix(QCoreApplication.translate("SwCCCV", u" A", None))
        self.label_2.setText(QCoreApplication.translate("SwCCCV", u"Base current", None))
        self.label_5.setText(QCoreApplication.translate("SwCCCV", u"Min current", None))
        self.minCurrent.setSuffix(QCoreApplication.translate("SwCCCV", u" A", None))
        self.label_3.setText(QCoreApplication.translate("SwCCCV", u"Step multiplier", None))
        self.label_4.setText(QCoreApplication.translate("SwCCCV", u"Target voltage", None))
        self.targetVoltage.setSuffix(QCoreApplication.translate("SwCCCV", u" V", None))
    # retranslateUi

