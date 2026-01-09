from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, 
                               QLabel, QFormLayout, QHBoxLayout)
import base64

class EntryDialog(QDialog):
    def __init__(self, entry=None):
        super().__init__()
        self.setWindowTitle("Entry")
        self.setFixedSize(400, 200)

        self.site = QLineEdit()
        self.user = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.totp = QLineEdit()
        self.totp.setPlaceholderText("Base32 secret (optional)")

        if entry:
            self.site.setText(entry["site"])
            self.user.setText(entry['username'])
            self.password.setText(entry['password'])
            try:
                self.totp.setText(entry.get("totp", {}).get("secret", ""))
            except:
                self.totp.setText("")

        self.show_password_btn = QPushButton("⚆")
        self.show_password_btn.setFixedWidth(40)
        self.show_password_btn.setCheckable(True)
        self.show_password_btn.toggled.connect(self.toggle_password_visibility)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password)
        password_layout.addWidget(self.show_password_btn)

        btn = QPushButton("Save")
        btn.clicked.connect(self.validate_and_accept)

        form = QFormLayout()
        form.addRow(QLabel("Site:"), self.site)
        form.addRow(QLabel("Username:"), self.user)
        form.addRow(QLabel("Password:"), password_layout)
        form.addRow(QLabel("TOTP Secret:"), self.totp)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(btn)
        self.setLayout(layout)

    def toggle_password_visibility(self, checked):
        if checked:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)

    def validate_and_accept(self):
        try:
            site = self.site.text().strip()
            username = self.user.text().strip()
            password = self.password.text()
            totp_secret = self.totp.text().strip().upper().replace(" ", "")
            
            if not site or not password:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Error", "Site and password are required")
                return
            
            if totp_secret and not self._is_valid_base32(totp_secret):
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Error", "Invalid TOTP secret format (must be base32)")
                return
            
            self._cached_data = {
                "site": site,
                "username": username,
                "password": password,
                "totp": {"secret": totp_secret, "digits": 6, "period": 30} if totp_secret else None
            }
            
            self.accept()
        except RuntimeError:
            pass

    def get_data(self):
        return self._cached_data
    
    def _is_valid_base32(self, s: str) -> bool:
        try:
            base64.b32decode(s + "=" * (-len(s) % 8))
            return True
        except:
            return False