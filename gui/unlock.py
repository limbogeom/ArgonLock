from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from vault.file import open_vault
from vault.engine import Vault
import traceback

class UnlockWindow(QWidget):
    def __init__(self, vault_path, on_unlocked):
        super().__init__()
        self.vault_path = vault_path
        self.on_unlocked = on_unlocked
        self.setWindowTitle("Unlock Vault")
        self.setFixedSize(400, 100)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Master password"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.returnPressed.connect(self.unlock)

        btn = QPushButton("Unlock")
        btn.clicked.connect(self.unlock)

        layout.addWidget(self.password)
        layout.addWidget(btn)
        self.setLayout(layout)

    def unlock(self):
        password = self.password.text()
        if not password:
            QMessageBox.warning(self, "Error", "Password cannot be empty")
            return
            
        try:
            data = open_vault(self.vault_path, password)
            vault = Vault(password, data)
            self.on_unlocked(vault)
            self.close()
        except Exception as e:
            error_msg = str(e) if str(e) else f"{type(e).__name__}: {traceback.format_exc()}"
            QMessageBox.critical(self, "Error", error_msg)