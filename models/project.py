from datetime import datetime
from typing import Optional, List, Dict, Any
from .database import Database


class Project:
    """Model for managing projects."""

    def __init__(self, db: Database):
        self.db = db

    def create(self, name: str, google_business_name: str, latitude: float,
               longitude: float, radius_km: int = 5, grid_size: str = '5x5',
               google_place_id: Optional[str] = None, address: Optional[str] = None) -> int:
        """Create a new project."""
        self.db.connect()
        cursor = self.db.execute('''
            INSERT INTO projects
            (name, google_business_name, latitude, longitude, radius_km,
             grid_size, google_place_id, address, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, google_business_name, latitude, longitude, radius_km,
              grid_size, google_place_id, address, datetime.now(), datetime.now()))
        self.db.commit()
        project_id = cursor.lastrowid
        self.db.close()
        return project_id

    def get(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get project by ID."""
        self.db.connect()
        project = self.db.fetch_one(
            'SELECT * FROM projects WHERE id = ?', (project_id,)
        )
        self.db.close()
        return project

    def get_all(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all projects."""
        self.db.connect()
        query = 'SELECT * FROM projects'
        if active_only:
            query += ' WHERE is_active = 1'
        query += ' ORDER BY created_at DESC'
        projects = self.db.fetch_all(query)
        self.db.close()
        return projects

    def update(self, project_id: int, **kwargs) -> bool:
        """Update project."""
        if not kwargs:
            return False

        kwargs['updated_at'] = datetime.now()
        fields = ', '.join([f'{key} = ?' for key in kwargs.keys()])
        values = tuple(kwargs.values()) + (project_id,)

        self.db.connect()
        self.db.execute(f'UPDATE projects SET {fields} WHERE id = ?', values)
        self.db.commit()
        self.db.close()
        return True

    def delete(self, project_id: int, soft_delete: bool = True) -> bool:
        """Delete project (soft or hard delete)."""
        self.db.connect()
        if soft_delete:
            self.db.execute(
                'UPDATE projects SET is_active = 0 WHERE id = ?', (project_id,)
            )
        else:
            self.db.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        self.db.commit()
        self.db.close()
        return True

    def get_with_keywords(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get project with its keywords."""
        self.db.connect()
        project = self.db.fetch_one(
            'SELECT * FROM projects WHERE id = ?', (project_id,)
        )
        if project:
            keywords = self.db.fetch_all(
                'SELECT * FROM keywords WHERE project_id = ? AND is_active = 1',
                (project_id,)
            )
            project['keywords'] = keywords
        self.db.close()
        return project
