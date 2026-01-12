from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QComboBox, QPushButton,
    QMessageBox, QLabel, QDoubleSpinBox
)
from PyQt5.QtCore import Qt
from typing import Optional

from models import Database, Project
from config import Settings


class ProjectDialog(QDialog):
    """Dialog for adding/editing projects."""

    def __init__(self, parent, db: Database, project_id: Optional[int] = None):
        super().__init__(parent)
        self.db = db
        self.project_model = Project(db)
        self.project_id = project_id

        self.init_ui()

        if project_id:
            self.load_project()

    def init_ui(self):
        """Initialize the user interface."""
        title = "Edytuj Projekt" if self.project_id else "Nowy Projekt"
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        # Form
        form = QFormLayout()

        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("Nazwa projektu")
        form.addRow("Nazwa projektu:", self.txt_name)

        self.txt_business_name = QLineEdit()
        self.txt_business_name.setPlaceholderText("Nazwa firmy w Google Maps")
        form.addRow("Nazwa firmy:", self.txt_business_name)

        self.txt_address = QLineEdit()
        self.txt_address.setPlaceholderText("Adres firmy (opcjonalne)")
        form.addRow("Adres:", self.txt_address)

        self.txt_latitude = QDoubleSpinBox()
        self.txt_latitude.setRange(-90.0, 90.0)
        self.txt_latitude.setDecimals(6)
        self.txt_latitude.setSingleStep(0.000001)
        self.txt_latitude.setValue(52.229676)  # Default: Warsaw
        form.addRow("Szerokość geograficzna:", self.txt_latitude)

        self.txt_longitude = QDoubleSpinBox()
        self.txt_longitude.setRange(-180.0, 180.0)
        self.txt_longitude.setDecimals(6)
        self.txt_longitude.setSingleStep(0.000001)
        self.txt_longitude.setValue(21.012229)  # Default: Warsaw
        form.addRow("Długość geograficzna:", self.txt_longitude)

        # Help label for coordinates
        coord_help = QLabel(
            '<small>Tip: Znajdź współrzędne w Google Maps → Kliknij prawym → "Co tu jest?"</small>'
        )
        coord_help.setWordWrap(True)
        form.addRow("", coord_help)

        self.spin_radius = QSpinBox()
        self.spin_radius.setRange(Settings.MIN_RADIUS_KM, Settings.MAX_RADIUS_KM)
        self.spin_radius.setValue(Settings.DEFAULT_RADIUS_KM)
        self.spin_radius.setSuffix(" km")
        form.addRow("Promień sprawdzania:", self.spin_radius)

        self.combo_grid = QComboBox()
        self.combo_grid.addItems(Settings.GRID_SIZES)
        self.combo_grid.setCurrentText(Settings.DEFAULT_GRID_SIZE)
        form.addRow("Rozmiar siatki:", self.combo_grid)

        # Grid explanation
        grid_help = QLabel(
            '<small>Siatka 5x5 = 25 punktów, 7x7 = 49 punktów, 9x9 = 81 punktów, 12x12 = 144 punkty</small>'
        )
        grid_help.setWordWrap(True)
        form.addRow("", grid_help)

        self.txt_place_id = QLineEdit()
        self.txt_place_id.setPlaceholderText("Place ID (opcjonalne)")
        form.addRow("Google Place ID:", self.txt_place_id)

        layout.addLayout(form)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.btn_cancel = QPushButton("Anuluj")
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_save = QPushButton("Zapisz")
        self.btn_save.clicked.connect(self.save_project)
        self.btn_save.setDefault(True)

        button_layout.addWidget(self.btn_cancel)
        button_layout.addWidget(self.btn_save)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_project(self):
        """Load project data for editing."""
        project = self.project_model.get(self.project_id)
        if not project:
            QMessageBox.critical(self, "Błąd", "Nie znaleziono projektu")
            self.reject()
            return

        self.txt_name.setText(project['name'])
        self.txt_business_name.setText(project['google_business_name'])
        self.txt_address.setText(project.get('address', ''))
        self.txt_latitude.setValue(project['latitude'])
        self.txt_longitude.setValue(project['longitude'])
        self.spin_radius.setValue(project['radius_km'])
        self.combo_grid.setCurrentText(project['grid_size'])
        self.txt_place_id.setText(project.get('google_place_id', ''))

    def save_project(self):
        """Save the project."""
        # Validate
        if not self.txt_name.text().strip():
            QMessageBox.warning(self, "Uwaga", "Podaj nazwę projektu")
            return

        if not self.txt_business_name.text().strip():
            QMessageBox.warning(self, "Uwaga", "Podaj nazwę firmy")
            return

        try:
            if self.project_id:
                # Update existing project
                self.project_model.update(
                    self.project_id,
                    name=self.txt_name.text().strip(),
                    google_business_name=self.txt_business_name.text().strip(),
                    address=self.txt_address.text().strip() or None,
                    latitude=self.txt_latitude.value(),
                    longitude=self.txt_longitude.value(),
                    radius_km=self.spin_radius.value(),
                    grid_size=self.combo_grid.currentText(),
                    google_place_id=self.txt_place_id.text().strip() or None
                )
            else:
                # Create new project
                self.project_model.create(
                    name=self.txt_name.text().strip(),
                    google_business_name=self.txt_business_name.text().strip(),
                    latitude=self.txt_latitude.value(),
                    longitude=self.txt_longitude.value(),
                    radius_km=self.spin_radius.value(),
                    grid_size=self.combo_grid.currentText(),
                    google_place_id=self.txt_place_id.text().strip() or None,
                    address=self.txt_address.text().strip() or None
                )

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się zapisać projektu:\n{str(e)}")
