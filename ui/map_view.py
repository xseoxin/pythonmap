from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QLabel, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import folium
from folium import plugins
import tempfile
import os
from typing import Dict, List

from models import Database, Project, Keyword, CheckResult
from services import GridCalculator


class MapView(QDialog):
    """Dialog for viewing map with position markers."""

    def __init__(self, parent, db: Database, project_id: int):
        super().__init__(parent)
        self.db = db
        self.project_id = project_id
        self.project_model = Project(db)
        self.keyword_model = Keyword(db)
        self.result_model = CheckResult(db)

        self.project = None
        self.keywords = []
        self.current_keyword_id = None

        self.init_ui()
        self.load_data()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Mapa Pozycji")
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout()

        # Top controls
        controls_layout = QHBoxLayout()

        controls_layout.addWidget(QLabel("Wybierz frazę:"))

        self.combo_keywords = QComboBox()
        self.combo_keywords.currentIndexChanged.connect(self.on_keyword_changed)
        controls_layout.addWidget(self.combo_keywords)

        btn_refresh = QPushButton("Odśwież mapę")
        btn_refresh.clicked.connect(self.refresh_map)
        controls_layout.addWidget(btn_refresh)

        controls_layout.addStretch()

        layout.addLayout(controls_layout)

        # Legend
        legend_label = QLabel(
            "🔵 = Znaleziono | ⚪ = Nie znaleziono | 🔴 = Lokalizacja firmy | 🟩 = Punkt centralny"
        )
        layout.addWidget(legend_label)

        # Web view for map
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        btn_close = QPushButton("Zamknij")
        btn_close.clicked.connect(self.accept)

        button_layout.addWidget(btn_close)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_data(self):
        """Load project and keywords data."""
        self.project = self.project_model.get(self.project_id)
        if not self.project:
            QMessageBox.critical(self, "Błąd", "Nie znaleziono projektu")
            self.reject()
            return

        self.keywords = self.keyword_model.get_by_project(self.project_id)

        if not self.keywords:
            QMessageBox.warning(self, "Uwaga", "Brak fraz dla tego projektu")
            return

        # Populate combo box
        for keyword in self.keywords:
            self.combo_keywords.addItem(keyword['phrase'], keyword['id'])

        # Show first keyword
        if self.keywords:
            self.current_keyword_id = self.keywords[0]['id']
            self.refresh_map()

    def on_keyword_changed(self, index):
        """Handle keyword selection change."""
        if index >= 0:
            self.current_keyword_id = self.combo_keywords.itemData(index)
            self.refresh_map()

    def refresh_map(self):
        """Refresh the map with current keyword data."""
        if not self.current_keyword_id or not self.project:
            return

        try:
            # Create map centered on business location
            m = folium.Map(
                location=[self.project['latitude'], self.project['longitude']],
                zoom_start=13,
                tiles='OpenStreetMap'
            )

            # Add business location marker (red)
            folium.Marker(
                location=[self.project['latitude'], self.project['longitude']],
                popup=f"<b>{self.project['google_business_name']}</b><br>{self.project.get('address', '')}",
                tooltip=self.project['google_business_name'],
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

            # Calculate grid points
            grid_points = GridCalculator.calculate_grid_points(
                self.project['latitude'],
                self.project['longitude'],
                self.project['radius_km'],
                self.project['grid_size']
            )

            # Get latest results for this keyword
            results = self.result_model.get_latest_by_keyword(self.current_keyword_id)

            # Create a dict for quick lookup
            results_dict = {
                (r['grid_x'], r['grid_y']): r
                for r in results
            }

            # Get grid center
            center_x, center_y = GridCalculator.get_grid_center_index(self.project['grid_size'])

            # Add markers for each grid point
            for lat, lon, grid_x, grid_y in grid_points:
                result = results_dict.get((grid_x, grid_y))

                # Determine marker color and info
                if grid_x == center_x and grid_y == center_y:
                    color = 'green'
                    icon = 'star'
                    popup_text = f"Punkt centralny ({grid_x},{grid_y})"
                elif result and result['found']:
                    color = 'blue'
                    icon = 'ok-sign'
                    position = result['position']
                    popup_text = f"Pozycja: {position}<br>Punkt: ({grid_x},{grid_y})"
                else:
                    color = 'lightgray'
                    icon = 'remove-sign'
                    popup_text = f"Nie znaleziono<br>Punkt: ({grid_x},{grid_y})"

                folium.Marker(
                    location=[lat, lon],
                    popup=popup_text,
                    tooltip=f"({grid_x},{grid_y})",
                    icon=folium.Icon(color=color, icon=icon)
                ).add_to(m)

            # Add circle to show radius
            folium.Circle(
                location=[self.project['latitude'], self.project['longitude']],
                radius=self.project['radius_km'] * 1000,  # Convert to meters
                color='blue',
                fill=True,
                fillOpacity=0.1,
                popup=f"Promień: {self.project['radius_km']} km"
            ).add_to(m)

            # Add grid lines for better visualization
            self._add_grid_lines(m, grid_points, self.project['grid_size'])

            # Save to temp file and load in web view
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                m.save(f.name)
                self.web_view.setUrl(QUrl.fromLocalFile(f.name))

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wygenerować mapy:\n{str(e)}")

    def _add_grid_lines(self, map_obj, grid_points: List, grid_size: str):
        """Add grid lines to the map for better visualization."""
        rows, cols = GridCalculator.parse_grid_size(grid_size)

        # Group points by row and column
        points_by_row = {}
        points_by_col = {}

        for lat, lon, grid_x, grid_y in grid_points:
            if grid_y not in points_by_row:
                points_by_row[grid_y] = []
            points_by_row[grid_y].append((lat, lon))

            if grid_x not in points_by_col:
                points_by_col[grid_x] = []
            points_by_col[grid_x].append((lat, lon))

        # Draw horizontal lines
        for row_points in points_by_row.values():
            if len(row_points) > 1:
                row_points.sort(key=lambda p: p[1])  # Sort by longitude
                folium.PolyLine(
                    locations=row_points,
                    color='gray',
                    weight=1,
                    opacity=0.3
                ).add_to(map_obj)

        # Draw vertical lines
        for col_points in points_by_col.values():
            if len(col_points) > 1:
                col_points.sort(key=lambda p: p[0])  # Sort by latitude
                folium.PolyLine(
                    locations=col_points,
                    color='gray',
                    weight=1,
                    opacity=0.3
                ).add_to(map_obj)
