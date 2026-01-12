from datetime import datetime
from typing import Optional, List, Dict, Any
from .database import Database


class Keyword:
    """Model for managing keywords/phrases."""

    def __init__(self, db: Database):
        self.db = db

    def create(self, project_id: int, phrase: str) -> int:
        """Create a new keyword."""
        self.db.connect()
        cursor = self.db.execute('''
            INSERT INTO keywords (project_id, phrase, created_at)
            VALUES (?, ?, ?)
        ''', (project_id, phrase, datetime.now()))
        self.db.commit()
        keyword_id = cursor.lastrowid
        self.db.close()
        return keyword_id

    def get(self, keyword_id: int) -> Optional[Dict[str, Any]]:
        """Get keyword by ID."""
        self.db.connect()
        keyword = self.db.fetch_one(
            'SELECT * FROM keywords WHERE id = ?', (keyword_id,)
        )
        self.db.close()
        return keyword

    def get_by_project(self, project_id: int, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all keywords for a project."""
        self.db.connect()
        query = 'SELECT * FROM keywords WHERE project_id = ?'
        params = [project_id]
        if active_only:
            query += ' AND is_active = 1'
        query += ' ORDER BY created_at DESC'
        keywords = self.db.fetch_all(query, tuple(params))
        self.db.close()
        return keywords

    def update(self, keyword_id: int, **kwargs) -> bool:
        """Update keyword."""
        if not kwargs:
            return False

        fields = ', '.join([f'{key} = ?' for key in kwargs.keys()])
        values = tuple(kwargs.values()) + (keyword_id,)

        self.db.connect()
        self.db.execute(f'UPDATE keywords SET {fields} WHERE id = ?', values)
        self.db.commit()
        self.db.close()
        return True

    def delete(self, keyword_id: int, soft_delete: bool = True) -> bool:
        """Delete keyword (soft or hard delete)."""
        self.db.connect()
        if soft_delete:
            self.db.execute(
                'UPDATE keywords SET is_active = 0 WHERE id = ?', (keyword_id,)
            )
        else:
            self.db.execute('DELETE FROM keywords WHERE id = ?', (keyword_id,))
        self.db.commit()
        self.db.close()
        return True

    def bulk_create(self, project_id: int, phrases: List[str]) -> List[int]:
        """Create multiple keywords at once."""
        self.db.connect()
        keyword_ids = []
        for phrase in phrases:
            cursor = self.db.execute('''
                INSERT INTO keywords (project_id, phrase, created_at)
                VALUES (?, ?, ?)
            ''', (project_id, phrase, datetime.now()))
            keyword_ids.append(cursor.lastrowid)
        self.db.commit()
        self.db.close()
        return keyword_ids
