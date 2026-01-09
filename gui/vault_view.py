from PySide6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QPushButton, 
                               QHBoxLayout, QMessageBox, QLineEdit, QLabel)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QGuiApplication
from gui.entry_dialog import EntryDialog
from crypto.totp import generate_totp

class VaultView(QWidget):
    def __init__(self, vault, save_callback):
        super().__init__()
        self.vault = vault
        self.save_callback = save_callback
        self.setWindowTitle("Vault")
        self.clipboard_timer = None

        self.list = QListWidget()
        self.list.itemClicked.connect(self.on_item_selected)
        
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")
        self.search.textChanged.connect(self.refresh)

        self.totp_label = QLabel("")
        self.totp_timer = QTimer()
        self.totp_timer.timeout.connect(self.update_totp)

        btn_add = QPushButton("Add")
        btn_edit = QPushButton("Edit")
        btn_del = QPushButton("Delete")
        btn_copy_pass = QPushButton("Copy Password")
        btn_copy_totp = QPushButton("Copy TOTP")

        btn_add.clicked.connect(self.add)
        btn_edit.clicked.connect(self.edit)
        btn_del.clicked.connect(self.delete)
        btn_copy_pass.clicked.connect(self.copy_password)
        btn_copy_totp.clicked.connect(self.copy_totp)

        buttons = QHBoxLayout()
        for b in (btn_add, btn_edit, btn_del, btn_copy_pass, btn_copy_totp):
            buttons.addWidget(b)

        layout = QVBoxLayout()
        layout.addWidget(self.search)
        layout.addWidget(self.list)
        layout.addWidget(self.totp_label)
        layout.addLayout(buttons)
        self.setLayout(layout)
        
        self.refresh()

    def closeEvent(self, event):
        if self.totp_timer.isActive():
            self.totp_timer.stop()
        if self.clipboard_timer and self.clipboard_timer.isActive():
            self.clipboard_timer.stop()
        event.accept()

    def refresh(self):
        self.list.clear()
        search_term = self.search.text().lower()
        for e in self.vault.list_entries():
            if search_term in e['site'].lower() or search_term in e['username'].lower():
                self.list.addItem(f"{e['site']} - {e['username']}")

    def on_item_selected(self):
        self.update_totp()
        if not self.totp_timer.isActive():
            self.totp_timer.start(1000)

    def update_totp(self):
        try:
            i = self.list.currentRow()
            if i < 0:
                self.totp_label.setText("")
                return
            
            entries = [e for e in self.vault.list_entries() 
                      if self.search.text().lower() in e['site'].lower() 
                      or self.search.text().lower() in e['username'].lower()]
            
            if i >= len(entries):
                return
                
            entry = entries[i]
            if entry.get("totp") and entry["totp"].get("secret"):
                try:
                    code, remaining = generate_totp(entry["totp"])
                    self.totp_label.setText(f"TOTP: {code} ({remaining}s)")
                except Exception as e:
                    self.totp_label.setText(f"TOTP: Error - {str(e)}")
            else:
                self.totp_label.setText("")
        except RuntimeError:
            pass

    def add(self):
        dlg = EntryDialog()
        if dlg.exec():
            data = dlg.get_data()
            self.vault.add_entry(data)
            self.save_callback()
            self.refresh()

    def edit(self):
        i = self.list.currentRow()
        if i < 0:
            return
        
        entries = [e for e in self.vault.list_entries() 
                  if self.search.text().lower() in e['site'].lower() 
                  or self.search.text().lower() in e['username'].lower()]
        
        if i >= len(entries):
            return
            
        all_entries = self.vault.list_entries()
        actual_index = all_entries.index(entries[i])
        
        dlg = EntryDialog(entries[i])
        if dlg.exec():
            data = dlg.get_data()
            self.vault.update_entry(actual_index, data)
            self.save_callback()
            self.refresh()

    def delete(self):
        i = self.list.currentRow()
        if i < 0:
            return
            
        reply = QMessageBox.question(self, "Confirm", 
                                     "Delete this entry?",
                                     QMessageBox.StandardButton.Yes | 
                                     QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            entries = [e for e in self.vault.list_entries() 
                      if self.search.text().lower() in e['site'].lower() 
                      or self.search.text().lower() in e['username'].lower()]
            
            if i >= len(entries):
                return
                
            all_entries = self.vault.list_entries()
            actual_index = all_entries.index(entries[i])
            
            self.vault.delete_entry(actual_index)
            self.save_callback()
            self.refresh()

    def copy_password(self):
        i = self.list.currentRow()
        if i < 0:
            return
        
        entries = [e for e in self.vault.list_entries() 
                  if self.search.text().lower() in e['site'].lower() 
                  or self.search.text().lower() in e['username'].lower()]
        
        if i < len(entries):
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(entries[i]['password'])
            self._clear_clipboard_after(30)

    def copy_totp(self):
        i = self.list.currentRow()
        if i < 0:
            return
        
        entries = [e for e in self.vault.list_entries() 
                  if self.search.text().lower() in e['site'].lower() 
                  or self.search.text().lower() in e['username'].lower()]
        
        if i < len(entries) and entries[i].get("totp") and entries[i]["totp"].get("secret"):
            try:
                code, _ = generate_totp(entries[i]["totp"])
                clipboard = QGuiApplication.clipboard()
                clipboard.setText(code)
                self._clear_clipboard_after(30)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Invalid TOTP secret: {str(e)}")

    def _clear_clipboard_after(self, seconds: int):
        if self.clipboard_timer and self.clipboard_timer.isActive():
            self.clipboard_timer.stop()
        
        self.clipboard_timer = QTimer(self)
        self.clipboard_timer.setSingleShot(True)
        self.clipboard_timer.timeout.connect(lambda: QGuiApplication.clipboard().clear())
        self.clipboard_timer.start(seconds * 1000)