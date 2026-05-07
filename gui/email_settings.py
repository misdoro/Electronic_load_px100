from PyQt5 import uic
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QGroupBox, QMessageBox
import smtplib
import os
import tempfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime

class EmailSettings(QGroupBox):
    def __init__(self, *args, **kwargs):
        super(EmailSettings, self).__init__(*args, **kwargs)
        uic.loadUi("gui/email_settings.ui", self)

        self.test_email_button.clicked.connect(self.send_test_email)
        self.load_settings()
        self.main_window = None  # Will be set by main window

        # Connect text change signals to auto-save
        self.sender_email.textChanged.connect(self.save_settings)
        self.email_password.textChanged.connect(self.save_settings)
        self.recipient_email.textChanged.connect(self.save_settings)

    def set_main_window(self, main_window):
        """Set reference to main window for accessing test data."""
        self.main_window = main_window

    def send_test_email(self):
        """Send a test email to verify the email settings."""
        try:
            # Email configuration
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = self.sender_email.text()
            password = self.email_password.text()
            recipient = self.recipient_email.text()

            if not all([sender_email, password, recipient]):
                QMessageBox.warning(self, "Missing Information",
                    "Please fill in all email settings before sending a test email.")
                return

            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = "Battery Tester - Test Email"

            body = """This is a test email from your Battery Tester application.

If you're receiving this email, your email settings are configured correctly!"""
            msg.attach(MIMEText(body, 'plain'))

            # Connect to server and send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, password)
                server.send_message(msg)

            QMessageBox.information(self, "Success",
                "Test email sent successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error",
                f"Failed to send test email:\n{str(e)}")

    def load_settings(self):
        settings = QSettings()
        self.sender_email.setText(settings.value("Email/sender", ""))
        self.email_password.setText(settings.value("Email/password", ""))
        self.recipient_email.setText(settings.value("Email/recipient", ""))

        # Load additional email preferences
        self.auto_send_enabled = settings.value("Email/auto_send", True, type=bool)
        self.email_on_completion = settings.value("Email/on_completion", True, type=bool)
        self.email_on_error = settings.value("Email/on_error", False, type=bool)

    def save_settings(self):
        settings = QSettings()
        settings.setValue("Email/sender", self.sender_email.text())
        settings.setValue("Email/password", self.email_password.text())
        settings.setValue("Email/recipient", self.recipient_email.text())

        # Save additional email preferences
        settings.setValue("Email/auto_send", getattr(self, 'auto_send_enabled', True))
        settings.setValue("Email/on_completion", getattr(self, 'email_on_completion', True))
        settings.setValue("Email/on_error", getattr(self, 'email_on_error', False))
        settings.sync()

    def save_email_history(self, subject, recipient, status):
        """Save email sending history for debugging/tracking."""
        settings = QSettings()

        # Get existing history (limit to last 10 entries)
        history = settings.value("Email/history", [], type=list)

        # Add new entry
        new_entry = {
            'timestamp': datetime.now().isoformat(),
            'subject': subject,
            'recipient': recipient,
            'status': status  # 'success' or 'failed'
        }

        history.append(new_entry)

        # Keep only last 10 entries
        if len(history) > 10:
            history = history[-10:]

        settings.setValue("Email/history", history)
        settings.sync()

    def get_email_history(self):
        """Get email sending history."""
        settings = QSettings()
        return settings.value("Email/history", [], type=list)