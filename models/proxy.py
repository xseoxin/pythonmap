from datetime import datetime
from typing import Optional, List, Dict, Any
from .database import Database


class Proxy:
    """Model for managing proxy servers."""

    def __init__(self, db: Database):
        self.db = db

    def create(self, host: str, port: int, protocol: str = 'http',
               username: Optional[str] = None, password: Optional[str] = None) -> int:
        """Create a new proxy."""
        self.db.connect()
        cursor = self.db.execute('''
            INSERT INTO proxies
            (host, port, protocol, username, password, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (host, port, protocol, username, password, datetime.now()))
        self.db.commit()
        proxy_id = cursor.lastrowid
        self.db.close()
        return proxy_id

    def get(self, proxy_id: int) -> Optional[Dict[str, Any]]:
        """Get proxy by ID."""
        self.db.connect()
        proxy = self.db.fetch_one(
            'SELECT * FROM proxies WHERE id = ?', (proxy_id,)
        )
        self.db.close()
        return proxy

    def get_all(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all proxies."""
        self.db.connect()
        query = 'SELECT * FROM proxies'
        if active_only:
            query += ' WHERE is_active = 1'
        query += ' ORDER BY created_at DESC'
        proxies = self.db.fetch_all(query)
        self.db.close()
        return proxies

    def get_random_active(self) -> Optional[Dict[str, Any]]:
        """Get a random active proxy."""
        self.db.connect()
        proxy = self.db.fetch_one('''
            SELECT * FROM proxies
            WHERE is_active = 1
            ORDER BY RANDOM()
            LIMIT 1
        ''')
        self.db.close()
        return proxy

    def update(self, proxy_id: int, **kwargs) -> bool:
        """Update proxy."""
        if not kwargs:
            return False

        fields = ', '.join([f'{key} = ?' for key in kwargs.keys()])
        values = tuple(kwargs.values()) + (proxy_id,)

        self.db.connect()
        self.db.execute(f'UPDATE proxies SET {fields} WHERE id = ?', values)
        self.db.commit()
        self.db.close()
        return True

    def mark_used(self, proxy_id: int) -> bool:
        """Mark proxy as recently used."""
        return self.update(proxy_id, last_used=datetime.now())

    def delete(self, proxy_id: int, soft_delete: bool = True) -> bool:
        """Delete proxy (soft or hard delete)."""
        self.db.connect()
        if soft_delete:
            self.db.execute(
                'UPDATE proxies SET is_active = 0 WHERE id = ?', (proxy_id,)
            )
        else:
            self.db.execute('DELETE FROM proxies WHERE id = ?', (proxy_id,))
        self.db.commit()
        self.db.close()
        return True

    def get_proxy_string(self, proxy: Dict[str, Any]) -> str:
        """Format proxy as connection string."""
        protocol = proxy.get('protocol', 'http')
        host = proxy['host']
        port = proxy['port']
        username = proxy.get('username')
        password = proxy.get('password')

        if username and password:
            return f"{protocol}://{username}:{password}@{host}:{port}"
        return f"{protocol}://{host}:{port}"
