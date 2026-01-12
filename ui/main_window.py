from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QLabel, QProgressBar, QStatusBar, QTabWidget, QSplitter,
    QGroupBox, QMenu, QAction
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
import logging
from typing import Optional, List, Dict, Any

from models import Database, Project, Keyword, CheckResult, Proxy
from services import GoogleMapsChecker, ProxyManager, ReportGenerator
from utils import CheckScheduler
from config import Settings

logger = logging.getLogger(__name__)


class CheckWorker(QThread):
    """Worker thread for running checks."""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, project_id: int, db: Database):
        super().__init__()
        self.project_id = project_id
        self.db = db
        self.project_model = Project(db)
        self.keyword_model = Keyword(db)
        self.result_model = CheckResult(db)
        self.proxy_manager = ProxyManager(db)

    def run(self):
        """Run the check."""
        try:
            # Get project and keywords
            project = self.project_model.get(self.project_id)
            keywords = self.keyword_model.get_by_project(self.project_id)

            if not keywords:
                self.finished.emit(False, "Brak fraz do sprawdzenia")
                return

            self.progress.emit(f"Rozpoczynam sprawdzanie {len(keywords)} fraz...")

            # Get proxy if available
            proxy = self.proxy_manager.get_proxy_for_check()

            # Create checker
            checker = GoogleMapsChecker(
                proxy=proxy,
                headless=Settings.HEADLESS_BROWSER
            )

            # Run checks
            results = checker.check_project_keywords(
                project,
                keywords,
                project['grid_size'],
                project['radius_km'],
                Settings.DELAY_BETWEEN_CHECKS_SECONDS
            )

            # Save results
            self.progress.emit("Zapisywanie wyników...")
            self.result_model.bulk_create(results)

            found_count = sum(1 for r in results if r['found'])
            total_count = len(results)

            self.finished.emit(
                True,
                f"Sprawdzono {len(keywords)} fraz w {total_count} punktach. "
                f"Znaleziono w {found_count} lokalizacjach."
            )

        except Exception as e:
            logger.error(f"Check failed: {e}")
            self.finished.emit(False, f"Błąd: {str(e)}")


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.db = Database(Settings.DATABASE_PATH)
        self.project_model = Project(self.db)
        self.keyword_model = Keyword(self.db)
        self.result_model = CheckResult(self.db)
        self.proxy_model = Proxy(self.db)
        self.report_generator = ReportGenerator(self.db)
        self.scheduler = CheckScheduler()

        self.current_project_id: Optional[int] = None
        self.check_worker: Optional[CheckWorker] = None

        self.init_ui()
        self.load_projects()

        # Start scheduler
        self.scheduler.start()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(Settings.WINDOW_TITLE)
        self.setGeometry(100, 100, Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Top button bar
        button_layout = QHBoxLayout()

        self.btn_new_project = QPushButton("➕ Nowy Projekt")
        self.btn_new_project.clicked.connect(self.add_project)

        self.btn_edit_project = QPushButton("✏️ Edytuj Projekt")
        self.btn_edit_project.clicked.connect(self.edit_project)
        self.btn_edit_project.setEnabled(False)

        self.btn_delete_project = QPushButton("🗑️ Usuń Projekt")
        self.btn_delete_project.clicked.connect(self.delete_project)
        self.btn_delete_project.setEnabled(False)

        self.btn_manage_proxies = QPushButton("🔒 Proxy")
        self.btn_manage_proxies.clicked.connect(self.manage_proxies)

        button_layout.addWidget(self.btn_new_project)
        button_layout.addWidget(self.btn_edit_project)
        button_layout.addWidget(self.btn_delete_project)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_manage_proxies)

        main_layout.addLayout(button_layout)

        # Splitter for projects and details
        splitter = QSplitter(Qt.Horizontal)

        # Left: Projects list
        projects_group = QGroupBox("Projekty")
        projects_layout = QVBoxLayout()

        self.projects_table = QTableWidget()
        self.projects_table.setColumnCount(5)
        self.projects_table.setHorizontalHeaderLabels([
            'Nazwa', 'Firma', 'Promień (km)', 'Siatka', 'Status'
        ])
        self.projects_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.projects_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.projects_table.setSelectionMode(QTableWidget.SingleSelection)
        self.projects_table.itemSelectionChanged.connect(self.on_project_selected)
        self.projects_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.projects_table.customContextMenuRequested.connect(self.show_project_context_menu)

        projects_layout.addWidget(self.projects_table)
        projects_group.setLayout(projects_layout)

        # Right: Project details
        details_group = QGroupBox("Szczegóły Projektu")
        details_layout = QVBoxLayout()

        # Project info
        self.lbl_project_info = QLabel("Wybierz projekt, aby zobaczyć szczegóły")
        self.lbl_project_info.setWordWrap(True)
        details_layout.addWidget(self.lbl_project_info)

        # Action buttons
        action_layout = QHBoxLayout()

        self.btn_check = QPushButton("▶️ Sprawdź Pozycje")
        self.btn_check.clicked.connect(self.run_check)
        self.btn_check.setEnabled(False)
        self.btn_check.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 8px; font-weight: bold; }")

        self.btn_keywords = QPushButton("📝 Zarządzaj Frazami")
        self.btn_keywords.clicked.connect(self.manage_keywords)
        self.btn_keywords.setEnabled(False)

        self.btn_view_map = QPushButton("🗺️ Pokaż Mapę")
        self.btn_view_map.clicked.connect(self.view_map)
        self.btn_view_map.setEnabled(False)

        self.btn_generate_report = QPushButton("📄 Generuj Raport")
        self.btn_generate_report.clicked.connect(self.generate_report)
        self.btn_generate_report.setEnabled(False)

        action_layout.addWidget(self.btn_check)
        action_layout.addWidget(self.btn_keywords)
        action_layout.addWidget(self.btn_view_map)
        action_layout.addWidget(self.btn_generate_report)

        details_layout.addLayout(action_layout)

        # Keywords table
        self.keywords_table = QTableWidget()
        self.keywords_table.setColumnCount(3)
        self.keywords_table.setHorizontalHeaderLabels(['Fraza', 'Status', 'Ostatnie sprawdzenie'])
        self.keywords_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        details_layout.addWidget(QLabel("Frazy:"))
        details_layout.addWidget(self.keywords_table)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        details_layout.addWidget(self.progress_bar)

        details_group.setLayout(details_layout)

        # Add to splitter
        splitter.addWidget(projects_group)
        splitter.addWidget(details_group)
        splitter.setSizes([400, 800])

        main_layout.addWidget(splitter)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Gotowe")

    def load_projects(self):
        """Load projects into the table."""
        self.projects_table.setRowCount(0)
        projects = self.project_model.get_all()

        for project in projects:
            row = self.projects_table.rowCount()
            self.projects_table.insertRow(row)

            self.projects_table.setItem(row, 0, QTableWidgetItem(project['name']))
            self.projects_table.setItem(row, 1, QTableWidgetItem(project['google_business_name']))
            self.projects_table.setItem(row, 2, QTableWidgetItem(str(project['radius_km'])))
            self.projects_table.setItem(row, 3, QTableWidgetItem(project['grid_size']))

            status = "✓ Aktywny" if project['is_active'] else "✗ Nieaktywny"
            self.projects_table.setItem(row, 4, QTableWidgetItem(status))

            # Store project ID
            self.projects_table.item(row, 0).setData(Qt.UserRole, project['id'])

    def on_project_selected(self):
        """Handle project selection."""
        selected = self.projects_table.selectedItems()
        if not selected:
            self.current_project_id = None
            self.btn_edit_project.setEnabled(False)
            self.btn_delete_project.setEnabled(False)
            self.btn_check.setEnabled(False)
            self.btn_keywords.setEnabled(False)
            self.btn_view_map.setEnabled(False)
            self.btn_generate_report.setEnabled(False)
            self.lbl_project_info.setText("Wybierz projekt, aby zobaczyć szczegóły")
            self.keywords_table.setRowCount(0)
            return

        row = selected[0].row()
        self.current_project_id = self.projects_table.item(row, 0).data(Qt.UserRole)

        # Enable buttons
        self.btn_edit_project.setEnabled(True)
        self.btn_delete_project.setEnabled(True)
        self.btn_check.setEnabled(True)
        self.btn_keywords.setEnabled(True)
        self.btn_view_map.setEnabled(True)
        self.btn_generate_report.setEnabled(True)

        # Load project details
        self.load_project_details()

    def load_project_details(self):
        """Load details for the selected project."""
        if not self.current_project_id:
            return

        project = self.project_model.get(self.current_project_id)
        if not project:
            return

        # Update info label
        info_text = f"""
        <b>Nazwa projektu:</b> {project['name']}<br>
        <b>Firma:</b> {project['google_business_name']}<br>
        <b>Adres:</b> {project.get('address', 'Nie podano')}<br>
        <b>Współrzędne:</b> {project['latitude']}, {project['longitude']}<br>
        <b>Promień:</b> {project['radius_km']} km<br>
        <b>Siatka:</b> {project['grid_size']}<br>
        <b>Utworzono:</b> {project['created_at']}
        """
        self.lbl_project_info.setText(info_text)

        # Load keywords
        self.load_keywords()

    def load_keywords(self):
        """Load keywords for the selected project."""
        self.keywords_table.setRowCount(0)

        if not self.current_project_id:
            return

        keywords = self.keyword_model.get_by_project(self.current_project_id)

        for keyword in keywords:
            row = self.keywords_table.rowCount()
            self.keywords_table.insertRow(row)

            self.keywords_table.setItem(row, 0, QTableWidgetItem(keyword['phrase']))

            # Get latest results
            results = self.result_model.get_latest_by_keyword(keyword['id'])
            if results:
                found_count = sum(1 for r in results if r['found'])
                status = f"Znaleziono w {found_count}/{len(results)} punktach"
                last_check = results[0]['checked_at'] if results else 'Nigdy'
            else:
                status = "Nie sprawdzono"
                last_check = "Nigdy"

            self.keywords_table.setItem(row, 1, QTableWidgetItem(status))
            self.keywords_table.setItem(row, 2, QTableWidgetItem(last_check))

    def add_project(self):
        """Add a new project."""
        from .project_dialog import ProjectDialog
        dialog = ProjectDialog(self, self.db)
        if dialog.exec_():
            self.load_projects()
            self.status_bar.showMessage("Projekt został dodany", 3000)

    def edit_project(self):
        """Edit the selected project."""
        if not self.current_project_id:
            return

        from .project_dialog import ProjectDialog
        dialog = ProjectDialog(self, self.db, self.current_project_id)
        if dialog.exec_():
            self.load_projects()
            self.load_project_details()
            self.status_bar.showMessage("Projekt został zaktualizowany", 3000)

    def delete_project(self):
        """Delete the selected project."""
        if not self.current_project_id:
            return

        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Czy na pewno chcesz usunąć ten projekt?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.project_model.delete(self.current_project_id)
            self.current_project_id = None
            self.load_projects()
            self.status_bar.showMessage("Projekt został usunięty", 3000)

    def manage_keywords(self):
        """Manage keywords for the selected project."""
        if not self.current_project_id:
            return

        from .keyword_dialog import KeywordDialog
        dialog = KeywordDialog(self, self.db, self.current_project_id)
        if dialog.exec_():
            self.load_keywords()
            self.status_bar.showMessage("Frazy zostały zaktualizowane", 3000)

    def manage_proxies(self):
        """Manage proxy servers."""
        from .proxy_dialog import ProxyDialog
        dialog = ProxyDialog(self, self.db)
        dialog.exec_()

    def run_check(self):
        """Run position check for the selected project."""
        if not self.current_project_id:
            return

        if self.check_worker and self.check_worker.isRunning():
            QMessageBox.warning(self, "Uwaga", "Sprawdzanie już trwa")
            return

        # Confirm check
        reply = QMessageBox.question(
            self,
            "Potwierdzenie",
            "Rozpocząć sprawdzanie pozycji? Może to potrwać kilka minut.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # Disable buttons
        self.btn_check.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate

        # Start worker
        self.check_worker = CheckWorker(self.current_project_id, self.db)
        self.check_worker.progress.connect(self.on_check_progress)
        self.check_worker.finished.connect(self.on_check_finished)
        self.check_worker.start()

    def on_check_progress(self, message: str):
        """Handle check progress updates."""
        self.status_bar.showMessage(message)

    def on_check_finished(self, success: bool, message: str):
        """Handle check completion."""
        self.btn_check.setEnabled(True)
        self.progress_bar.setVisible(False)

        if success:
            QMessageBox.information(self, "Sukces", message)
            self.load_keywords()
        else:
            QMessageBox.warning(self, "Błąd", message)

        self.status_bar.showMessage("Gotowe", 3000)

    def view_map(self):
        """View the map with position markers."""
        if not self.current_project_id:
            return

        from .map_view import MapView
        dialog = MapView(self, self.db, self.current_project_id)
        dialog.exec_()

    def generate_report(self):
        """Generate a report for the selected project."""
        if not self.current_project_id:
            return

        # Ask for report type
        reply = QMessageBox.question(
            self,
            "Typ raportu",
            "Wybierz format raportu:\n\nYes = Excel\nNo = PDF",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )

        if reply == QMessageBox.Cancel:
            return

        try:
            if reply == QMessageBox.Yes:
                filepath = self.report_generator.generate_excel_report(self.current_project_id)
            else:
                filepath = self.report_generator.generate_pdf_report(self.current_project_id)

            QMessageBox.information(
                self,
                "Sukces",
                f"Raport został wygenerowany:\n{filepath}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wygenerować raportu:\n{str(e)}")

    def show_project_context_menu(self, position):
        """Show context menu for project."""
        menu = QMenu()

        check_action = QAction("Sprawdź pozycje", self)
        check_action.triggered.connect(self.run_check)

        keywords_action = QAction("Zarządzaj frazami", self)
        keywords_action.triggered.connect(self.manage_keywords)

        edit_action = QAction("Edytuj", self)
        edit_action.triggered.connect(self.edit_project)

        delete_action = QAction("Usuń", self)
        delete_action.triggered.connect(self.delete_project)

        menu.addAction(check_action)
        menu.addAction(keywords_action)
        menu.addSeparator()
        menu.addAction(edit_action)
        menu.addAction(delete_action)

        menu.exec_(self.projects_table.viewport().mapToGlobal(position))

    def closeEvent(self, event):
        """Handle window close event."""
        self.scheduler.stop()
        event.accept()
