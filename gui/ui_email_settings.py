# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'email_settings.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_EmailSettings(object):
    def setupUi(self, EmailSettings):
        if not EmailSettings.objectName():
            EmailSettings.setObjectName(u"EmailSettings")
        EmailSettings.resize(400, 180)
        self.formLayout = QFormLayout(EmailSettings)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(EmailSettings)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.sender_email = QLineEdit(EmailSettings)
        self.sender_email.setObjectName(u"sender_email")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.sender_email)

        self.label_2 = QLabel(EmailSettings)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.email_password = QLineEdit(EmailSettings)
        self.email_password.setObjectName(u"email_password")
        self.email_password.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.email_password)

        self.label_3 = QLabel(EmailSettings)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.recipient_email = QLineEdit(EmailSettings)
        self.recipient_email.setObjectName(u"recipient_email")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.recipient_email)

        self.test_email_button = QPushButton(EmailSettings)
        self.test_email_button.setObjectName(u"test_email_button")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.test_email_button)


        self.retranslateUi(EmailSettings)

        QMetaObject.connectSlotsByName(EmailSettings)
    # setupUi

    def retranslateUi(self, EmailSettings):
        EmailSettings.setTitle(QCoreApplication.translate("EmailSettings", u"Email Settings", None))
        self.label.setText(QCoreApplication.translate("EmailSettings", u"Sender Email:", None))
        self.label_2.setText(QCoreApplication.translate("EmailSettings", u"App Password:", None))
        self.label_3.setText(QCoreApplication.translate("EmailSettings", u"Recipient Email:", None))
        self.test_email_button.setText(QCoreApplication.translate("EmailSettings", u"Send Test Email", None))
    # retranslateUi

