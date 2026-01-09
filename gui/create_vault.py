from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QLineEdit, QWidget, QMessageBox
from vault.file import create_vault

class CreateVault(QWidget):
    def __init__(self, vault_path, on_created):
        super().__init__()
        self.on_created = on_created
        self.vault_path = vault_path
        self.setWindowTitle("Create vault")
        self.setFixedSize(400, 100)

        self.lbmaster = QLabel("Master password:")
        self.passw_entry = QLineEdit()
        self.passw_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.passw_entry.returnPressed.connect(self.create_vault_handler)

        self.savebtn = QPushButton("Create")
        self.savebtn.clicked.connect(self.create_vault_handler)

        layout = QVBoxLayout()

        layout.addWidget(self.lbmaster)
        layout.addWidget(self.passw_entry)
        layout.addWidget(self.savebtn)
        self.setLayout(layout)

    def create_vault_handler(self):
        password = self.passw_entry.text()

        if not password:
            QMessageBox.warning(self, "Error", "Password cannot be empty")
        create_vault(self.vault_path, password)
        self.close()
        self.on_created()