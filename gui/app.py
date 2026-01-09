import sys
from PySide6.QtWidgets import QApplication
from gui.unlock import UnlockWindow
from gui.vault_view import VaultView
from gui.create_vault import CreateVault
from pathlib import Path

VAULT_FILE = Path("safe.vault")

def main():
    app = QApplication(sys.argv)
    
    vault_view = None
    unlock = None

    def on_unlocked(vault):
        nonlocal vault_view, unlock
        
        def save():
            with open(VAULT_FILE, "wb") as f:
                f.write(vault.serialize())

        vault_view = VaultView(vault, save)
        vault_view.show()

        if unlock:
            unlock.close()

    unlock = UnlockWindow(VAULT_FILE, on_unlocked)

    if not Path.exists(VAULT_FILE):
        create = CreateVault(VAULT_FILE, unlock.show)
        create.show()
    else:
        unlock.show()
        

    sys.exit(app.exec())

if __name__ == "__main__":
    main()