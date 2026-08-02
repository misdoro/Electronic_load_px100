# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'internal_r.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFormLayout, QGroupBox,
    QHeaderView, QLabel, QSizePolicy, QTableView,
    QVBoxLayout, QWidget)

class Ui_is_enabled(object):
    def setupUi(self, is_enabled):
        if not is_enabled.objectName():
            is_enabled.setObjectName(u"is_enabled")
        is_enabled.resize(171, 250)
        is_enabled.setCheckable(True)
        self.verticalLayout_2 = QVBoxLayout(is_enabled)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(is_enabled)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.stateLabel = QLabel(is_enabled)
        self.stateLabel.setObjectName(u"stateLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.stateLabel)

        self.label = QLabel(is_enabled)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.measurePeriod = QDoubleSpinBox(is_enabled)
        self.measurePeriod.setObjectName(u"measurePeriod")
        self.measurePeriod.setDecimals(2)
        self.measurePeriod.setMinimum(0.010000000000000)
        self.measurePeriod.setSingleStep(0.100000000000000)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.measurePeriod)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.resultsTable = QTableView(is_enabled)
        self.resultsTable.setObjectName(u"resultsTable")
        self.resultsTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.resultsTable.horizontalHeader().setMinimumSectionSize(30)
        self.resultsTable.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.resultsTable)


        self.retranslateUi(is_enabled)

        QMetaObject.connectSlotsByName(is_enabled)
    # setupUi

    def retranslateUi(self, is_enabled):
        is_enabled.setTitle(QCoreApplication.translate("is_enabled", u"Internal resistance", None))
        self.label_2.setText(QCoreApplication.translate("is_enabled", u"State", None))
        self.stateLabel.setText(QCoreApplication.translate("is_enabled", u"Idle", None))
        self.label.setText(QCoreApplication.translate("is_enabled", u"Periodicity", None))
        self.measurePeriod.setSuffix(QCoreApplication.translate("is_enabled", u" V", None))
    # retranslateUi

