from datetime import datetime
from typing import Optional, List, Dict, Any
from .database import Database


class CheckResult:
    """Model for managing check results."""

    def __init__(self, db: Database):
        self.db = db

    def create(self, keyword_id: int, position: Optional[int],
               grid_x: int, grid_y: int, latitude: float, longitude: float,
               found: bool = False, response_data: Optional[str] = None) -> int:
        """Create a new check result."""
        self.db.connect()
        cursor = self.db.execute('''
            INSERT INTO check_results
            (keyword_id, position, grid_x, grid_y, latitude, longitude,
             found, response_data, checked_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (keyword_id, position, grid_x, grid_y, latitude, longitude,
              1 if found else 0, response_data, datetime.now()))
        self.db.commit()
        result_id = cursor.lastrowid
        self.db.close()
        return result_id

    def get_by_keyword(self, keyword_id: int, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get check results for a keyword."""
        self.db.connect()
        query = '''
            SELECT * FROM check_results
            WHERE keyword_id = ?
            ORDER BY checked_at DESC
        '''
        if limit:
            query += f' LIMIT {limit}'
        results = self.db.fetch_all(query, (keyword_id,))
        self.db.close()
        return results

    def get_latest_by_keyword(self, keyword_id: int) -> List[Dict[str, Any]]:
        """Get latest check results for a keyword (one per grid point)."""
        self.db.connect()
        results = self.db.fetch_all('''
            SELECT cr1.*
            FROM check_results cr1
            INNER JOIN (
                SELECT grid_x, grid_y, MAX(checked_at) as max_date
                FROM check_results
                WHERE keyword_id = ?
                GROUP BY grid_x, grid_y
            ) cr2 ON cr1.grid_x = cr2.grid_x
                  AND cr1.grid_y = cr2.grid_y
                  AND cr1.checked_at = cr2.max_date
            WHERE cr1.keyword_id = ?
            ORDER BY cr1.grid_x, cr1.grid_y
        ''', (keyword_id, keyword_id))
        self.db.close()
        return results

    def get_by_project(self, project_id: int) -> List[Dict[str, Any]]:
        """Get all check results for a project."""
        self.db.connect()
        results = self.db.fetch_all('''
            SELECT cr.*, k.phrase, k.project_id
            FROM check_results cr
            INNER JOIN keywords k ON cr.keyword_id = k.id
            WHERE k.project_id = ?
            ORDER BY cr.checked_at DESC
        ''', (project_id,))
        self.db.close()
        return results

    def get_statistics(self, keyword_id: int) -> Dict[str, Any]:
        """Get statistics for a keyword."""
        self.db.connect()
        stats = self.db.fetch_one('''
            SELECT
                COUNT(*) as total_checks,
                SUM(found) as times_found,
                AVG(CASE WHEN found = 1 THEN position END) as avg_position,
                MIN(CASE WHEN found = 1 THEN position END) as best_position,
                MAX(checked_at) as last_check
            FROM check_results
            WHERE keyword_id = ?
        ''', (keyword_id,))
        self.db.close()
        return stats or {}

    def delete_old_results(self, days: int = 90) -> int:
        """Delete check results older than specified days."""
        self.db.connect()
        cursor = self.db.execute('''
            DELETE FROM check_results
            WHERE checked_at < datetime('now', '-' || ? || ' days')
        ''', (days,))
        deleted_count = cursor.rowcount
        self.db.commit()
        self.db.close()
        return deleted_count

    def bulk_create(self, results: List[Dict[str, Any]]) -> List[int]:
        """Create multiple check results at once."""
        self.db.connect()
        result_ids = []
        for result in results:
            cursor = self.db.execute('''
                INSERT INTO check_results
                (keyword_id, position, grid_x, grid_y, latitude, longitude,
                 found, response_data, checked_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result['keyword_id'],
                result.get('position'),
                result['grid_x'],
                result['grid_y'],
                result['latitude'],
                result['longitude'],
                1 if result.get('found', False) else 0,
                result.get('response_data'),
                datetime.now()
            ))
            result_ids.append(cursor.lastrowid)
        self.db.commit()
        self.db.close()
        return result_ids
