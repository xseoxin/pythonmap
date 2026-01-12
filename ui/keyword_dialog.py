from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QLineEdit, QMessageBox, QLabel,
    QTextEdit, QGroupBox
)
from PyQt5.QtCore import Qt

from models import Database, Keyword


class KeywordDialog(QDialog):
    """Dialog for managing keywords."""

    def __init__(self, parent, db: Database, project_id: int):
        super().__init__(parent)
        self.db = db
        self.project_id = project_id
        self.keyword_model = Keyword(db)

        self.init_ui()
        self.load_keywords()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Zarządzanie Frazami")
        self.setModal(True)
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout()

        # Current keywords group
        current_group = QGroupBox("Obecne frazy")
        current_layout = QVBoxLayout()

        self.keywords_list = QListWidget()
        current_layout.addWidget(self.keywords_list)

        btn_delete = QPushButton("Usuń zaznaczoną frazę")
        btn_delete.clicked.connect(self.delete_keyword)
        current_layout.addWidget(btn_delete)

        current_group.setLayout(current_layout)
        layout.addWidget(current_group)

        # Add single keyword group
        single_group = QGroupBox("Dodaj pojedynczą frazę")
        single_layout = QHBoxLayout()

        self.txt_keyword = QLineEdit()
        self.txt_keyword.setPlaceholderText("Wpisz frazę...")
        self.txt_keyword.returnPressed.connect(self.add_single_keyword)

        btn_add_single = QPushButton("Dodaj")
        btn_add_single.clicked.connect(self.add_single_keyword)

        single_layout.addWidget(self.txt_keyword)
        single_layout.addWidget(btn_add_single)

        single_group.setLayout(single_layout)
        layout.addWidget(single_group)

        # Add multiple keywords group
        multiple_group = QGroupBox("Dodaj wiele fraz (jedna fraza na linię)")
        multiple_layout = QVBoxLayout()

        self.txt_keywords_bulk = QTextEdit()
        self.txt_keywords_bulk.setPlaceholderText(
            "Wpisz frazy, każdą w nowej linii:\n"
            "pizza\n"
            "restauracja włoska\n"
            "najlepsza pizza w mieście"
        )
        self.txt_keywords_bulk.setMaximumHeight(150)

        btn_add_bulk = QPushButton("Dodaj wszystkie")
        btn_add_bulk.clicked.connect(self.add_bulk_keywords)

        multiple_layout.addWidget(self.txt_keywords_bulk)
        multiple_layout.addWidget(btn_add_bulk)

        multiple_group.setLayout(multiple_layout)
        layout.addWidget(multiple_group)

        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        btn_close = QPushButton("Zamknij")
        btn_close.clicked.connect(self.accept)

        button_layout.addWidget(btn_close)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_keywords(self):
        """Load keywords for the project."""
        self.keywords_list.clear()
        keywords = self.keyword_model.get_by_project(self.project_id)

        for keyword in keywords:
            item_text = f"{keyword['phrase']} (ID: {keyword['id']})"
            item = self.keywords_list.addItem(item_text)
            # Store keyword ID in item data
            self.keywords_list.item(self.keywords_list.count() - 1).setData(Qt.UserRole, keyword['id'])

    def add_single_keyword(self):
        """Add a single keyword."""
        phrase = self.txt_keyword.text().strip()

        if not phrase:
            QMessageBox.warning(self, "Uwaga", "Wpisz frazę")
            return

        try:
            self.keyword_model.create(self.project_id, phrase)
            self.txt_keyword.clear()
            self.load_keywords()
            QMessageBox.information(self, "Sukces", "Fraza została dodana")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się dodać frazy:\n{str(e)}")

    def add_bulk_keywords(self):
        """Add multiple keywords."""
        text = self.txt_keywords_bulk.toPlainText().strip()

        if not text:
            QMessageBox.warning(self, "Uwaga", "Wpisz frazy")
            return

        # Split by lines and filter empty
        phrases = [line.strip() for line in text.split('\n') if line.strip()]

        if not phrases:
            QMessageBox.warning(self, "Uwaga", "Brak poprawnych fraz")
            return

        try:
            self.keyword_model.bulk_create(self.project_id, phrases)
            self.txt_keywords_bulk.clear()
            self.load_keywords()
            QMessageBox.information(
                self,
                "Sukces",
                f"Dodano {len(phrases)} fraz"
            )
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się dodać fraz:\n{str(e)}")

    def delete_keyword(self):
        """Delete the selected keyword."""
        current_item = self.keywords_list.currentItem()

        if not current_item:
            QMessageBox.warning(self, "Uwaga", "Wybierz frazę do usunięcia")
            return

        keyword_id = current_item.data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno chcesz usunąć tę frazę?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.keyword_model.delete(keyword_id)
                self.load_keywords()
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się usunąć frazy:\n{str(e)}")
