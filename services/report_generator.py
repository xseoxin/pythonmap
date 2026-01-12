import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import logging

from models import Database, Project, Keyword, CheckResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """Service for generating reports."""

    def __init__(self, db: Database):
        self.db = db
        self.project_model = Project(db)
        self.keyword_model = Keyword(db)
        self.result_model = CheckResult(db)
        self.reports_dir = 'reports'
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_excel_report(self, project_id: int) -> str:
        """
        Generate Excel report for a project.

        Args:
            project_id: Project ID

        Returns:
            Path to generated report file
        """
        project = self.project_model.get(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        keywords = self.keyword_model.get_by_project(project_id)

        # Prepare data for Excel
        report_data = []

        for keyword in keywords:
            # Get latest results for this keyword
            results = self.result_model.get_latest_by_keyword(keyword['id'])

            if not results:
                report_data.append({
                    'Fraza': keyword['phrase'],
                    'Status': 'Brak danych',
                    'Pozycja (średnia)': '-',
                    'Znaleziono w punktach': '0/0',
                    'Najlepsza pozycja': '-'
                })
                continue

            # Calculate statistics
            found_count = sum(1 for r in results if r['found'])
            total_count = len(results)
            positions = [r['position'] for r in results if r['found'] and r['position']]
            avg_position = round(sum(positions) / len(positions), 1) if positions else None
            best_position = min(positions) if positions else None

            report_data.append({
                'Fraza': keyword['phrase'],
                'Status': 'Znaleziono' if found_count > 0 else 'Nie znaleziono',
                'Pozycja (średnia)': avg_position if avg_position else '-',
                'Znaleziono w punktach': f"{found_count}/{total_count}",
                'Najlepsza pozycja': best_position if best_position else '-'
            })

        # Create DataFrame
        df = pd.DataFrame(report_data)

        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.reports_dir}/raport_{project['name']}_{timestamp}.xlsx"
        filename = filename.replace(' ', '_')

        # Write to Excel with formatting
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Summary sheet
            df.to_excel(writer, sheet_name='Podsumowanie', index=False)

            # Detailed results for each keyword
            for keyword in keywords:
                results = self.result_model.get_latest_by_keyword(keyword['id'])
                if results:
                    detail_data = [{
                        'Punkt (X,Y)': f"({r['grid_x']},{r['grid_y']})",
                        'Szerokość geo.': round(r['latitude'], 6),
                        'Długość geo.': round(r['longitude'], 6),
                        'Znaleziono': 'Tak' if r['found'] else 'Nie',
                        'Pozycja': r['position'] if r['found'] else '-',
                        'Data sprawdzenia': r['checked_at']
                    } for r in results]

                    detail_df = pd.DataFrame(detail_data)
                    sheet_name = keyword['phrase'][:31]  # Excel sheet name limit
                    detail_df.to_excel(writer, sheet_name=sheet_name, index=False)

        logger.info(f"Excel report generated: {filename}")
        return filename

    def generate_pdf_report(self, project_id: int) -> str:
        """
        Generate PDF report for a project.

        Args:
            project_id: Project ID

        Returns:
            Path to generated report file
        """
        project = self.project_model.get(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        keywords = self.keyword_model.get_by_project(project_id)

        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.reports_dir}/raport_{project['name']}_{timestamp}.pdf"
        filename = filename.replace(' ', '_')

        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=12
        )

        # Title
        title = Paragraph(f"Raport pozycji w Google Maps<br/>{project['name']}", title_style)
        story.append(title)
        story.append(Spacer(1, 0.2 * inch))

        # Project info
        story.append(Paragraph("Informacje o projekcie", heading_style))
        project_info = [
            ['Nazwa firmy:', project['google_business_name']],
            ['Adres:', project.get('address', '-')],
            ['Promień sprawdzania:', f"{project['radius_km']} km"],
            ['Siatka:', project['grid_size']],
            ['Data raportu:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]

        project_table = Table(project_info, colWidths=[2 * inch, 4 * inch])
        project_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(project_table)
        story.append(Spacer(1, 0.3 * inch))

        # Keywords summary
        story.append(Paragraph("Podsumowanie fraz", heading_style))

        summary_data = [['Fraza', 'Status', 'Śr. pozycja', 'Najlepsza', 'Punkty']]

        for keyword in keywords:
            results = self.result_model.get_latest_by_keyword(keyword['id'])

            if not results:
                summary_data.append([
                    keyword['phrase'],
                    'Brak danych',
                    '-',
                    '-',
                    '0/0'
                ])
                continue

            found_count = sum(1 for r in results if r['found'])
            total_count = len(results)
            positions = [r['position'] for r in results if r['found'] and r['position']]
            avg_position = round(sum(positions) / len(positions), 1) if positions else '-'
            best_position = min(positions) if positions else '-'

            summary_data.append([
                keyword['phrase'],
                'Znaleziono' if found_count > 0 else 'Nie znaleziono',
                str(avg_position),
                str(best_position),
                f"{found_count}/{total_count}"
            ])

        summary_table = Table(summary_data, colWidths=[2 * inch, 1.3 * inch, 1 * inch, 1 * inch, 0.9 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.white])
        ]))
        story.append(summary_table)

        # Build PDF
        doc.build(story)

        logger.info(f"PDF report generated: {filename}")
        return filename

    def generate_comparison_report(self, project_id: int,
                                  start_date: Optional[str] = None,
                                  end_date: Optional[str] = None) -> str:
        """
        Generate a comparison report showing position changes over time.

        Args:
            project_id: Project ID
            start_date: Start date for comparison (ISO format)
            end_date: End date for comparison (ISO format)

        Returns:
            Path to generated Excel report
        """
        project = self.project_model.get(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.reports_dir}/porownanie_{project['name']}_{timestamp}.xlsx"
        filename = filename.replace(' ', '_')

        # TODO: Implement time-based comparison logic
        # This would require querying historical check_results with date filters

        logger.info(f"Comparison report generated: {filename}")
        return filename
