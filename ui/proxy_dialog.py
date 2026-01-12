from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QTextEdit, QGroupBox, QLabel,
    QCheckBox
)
from PyQt5.QtCore import Qt

from models import Database, Proxy


class ProxyDialog(QDialog):
    """Dialog for managing proxy servers."""

    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self.proxy_model = Proxy(db)

        self.init_ui()
        self.load_proxies()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Zarządzanie Proxy")
        self.setModal(True)
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout()

        # Current proxies group
        current_group = QGroupBox("Dostępne serwery proxy")
        current_layout = QVBoxLayout()

        self.proxies_table = QTableWidget()
        self.proxies_table.setColumnCount(5)
        self.proxies_table.setHorizontalHeaderLabels([
            'Host', 'Port', 'Protokół', 'Status', 'Ostatnie użycie'
        ])
        self.proxies_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.proxies_table.setSelectionBehavior(QTableWidget.SelectRows)

        current_layout.addWidget(self.proxies_table)

        btn_layout = QHBoxLayout()

        btn_delete = QPushButton("Usuń zaznaczone")
        btn_delete.clicked.connect(self.delete_proxy)

        btn_test = QPushButton("Testuj zaznaczone")
        btn_test.clicked.connect(self.test_proxy)

        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_test)
        btn_layout.addStretch()

        current_layout.addLayout(btn_layout)

        current_group.setLayout(current_layout)
        layout.addWidget(current_group)

        # Add proxies group
        add_group = QGroupBox("Dodaj serwery proxy")
        add_layout = QVBoxLayout()

        info_label = QLabel(
            "Wpisz serwery proxy w jednym z następujących formatów (jeden na linię):\n"
            "• host:port\n"
            "• protocol://host:port\n"
            "• protocol://username:password@host:port"
        )
        info_label.setWordWrap(True)
        add_layout.addWidget(info_label)

        self.txt_proxies = QTextEdit()
        self.txt_proxies.setPlaceholderText(
            "Przykłady:\n"
            "123.45.67.89:8080\n"
            "http://proxy.example.com:3128\n"
            "http://user:pass@proxy.example.com:3128"
        )
        self.txt_proxies.setMaximumHeight(120)
        add_layout.addWidget(self.txt_proxies)

        btn_add = QPushButton("Dodaj wszystkie")
        btn_add.clicked.connect(self.add_proxies)
        add_layout.addWidget(btn_add)

        add_group.setLayout(add_layout)
        layout.addWidget(add_group)

        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        btn_close = QPushButton("Zamknij")
        btn_close.clicked.connect(self.accept)

        button_layout.addWidget(btn_close)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_proxies(self):
        """Load proxies into the table."""
        self.proxies_table.setRowCount(0)
        proxies = self.proxy_model.get_all(active_only=False)

        for proxy in proxies:
            row = self.proxies_table.rowCount()
            self.proxies_table.insertRow(row)

            self.proxies_table.setItem(row, 0, QTableWidgetItem(proxy['host']))
            self.proxies_table.setItem(row, 1, QTableWidgetItem(str(proxy['port'])))
            self.proxies_table.setItem(row, 2, QTableWidgetItem(proxy['protocol']))

            status = "✓ Aktywny" if proxy['is_active'] else "✗ Nieaktywny"
            self.proxies_table.setItem(row, 3, QTableWidgetItem(status))

            last_used = proxy.get('last_used', 'Nigdy')
            self.proxies_table.setItem(row, 4, QTableWidgetItem(str(last_used)))

            # Store proxy ID
            self.proxies_table.item(row, 0).setData(Qt.UserRole, proxy['id'])

    def add_proxies(self):
        """Add proxies from text input."""
        text = self.txt_proxies.toPlainText().strip()

        if not text:
            QMessageBox.warning(self, "Uwaga", "Wpisz serwery proxy")
            return

        # Split by lines
        proxy_strings = [line.strip() for line in text.split('\n') if line.strip()]

        if not proxy_strings:
            QMessageBox.warning(self, "Uwaga", "Brak poprawnych serwerów proxy")
            return

        try:
            from services import ProxyManager
            proxy_manager = ProxyManager(self.db)
            results = proxy_manager.bulk_add_proxies(proxy_strings)

            self.txt_proxies.clear()
            self.load_proxies()

            msg = f"Dodano: {results['added']}"
            if results['failed'] > 0:
                msg += f"\nNie udało się dodać: {results['failed']}"

            QMessageBox.information(self, "Wynik", msg)

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się dodać proxy:\n{str(e)}")

    def delete_proxy(self):
        """Delete the selected proxy."""
        selected = self.proxies_table.selectedItems()

        if not selected:
            QMessageBox.warning(self, "Uwaga", "Wybierz proxy do usunięcia")
            return

        row = selected[0].row()
        proxy_id = self.proxies_table.item(row, 0).data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno chcesz usunąć ten serwer proxy?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.proxy_model.delete(proxy_id, soft_delete=False)
                self.load_proxies()
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się usunąć proxy:\n{str(e)}")

    def test_proxy(self):
        """Test the selected proxy."""
        selected = self.proxies_table.selectedItems()

        if not selected:
            QMessageBox.warning(self, "Uwaga", "Wybierz proxy do testowania")
            return

        row = selected[0].row()
        proxy_id = self.proxies_table.item(row, 0).data(Qt.UserRole)

        try:
            from services import ProxyManager
            proxy_manager = ProxyManager(self.db)

            QMessageBox.information(self, "Info", "Testowanie proxy... To może potrwać kilka sekund.")

            success = proxy_manager.test_proxy(proxy_id)

            if success:
                QMessageBox.information(self, "Sukces", "Proxy działa poprawnie!")
            else:
                QMessageBox.warning(self, "Błąd", "Proxy nie działa lub przekroczono limit czasu")

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się przetestować proxy:\n{str(e)}")
