import logging
from typing import Optional, Dict, Any
from models import Database, Proxy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProxyManager:
    """Service for managing proxy servers."""

    def __init__(self, db: Database):
        self.db = db
        self.proxy_model = Proxy(db)

    def get_proxy_for_check(self) -> Optional[str]:
        """
        Get a proxy for checking (random selection from active proxies).

        Returns:
            Proxy connection string or None if no proxies available
        """
        proxy = self.proxy_model.get_random_active()

        if proxy:
            # Mark as used
            self.proxy_model.mark_used(proxy['id'])

            # Format as connection string
            proxy_string = self.proxy_model.get_proxy_string(proxy)
            logger.info(f"Using proxy: {proxy['host']}:{proxy['port']}")
            return proxy_string

        logger.info("No active proxies available, checking without proxy")
        return None

    def test_proxy(self, proxy_id: int, timeout: int = 10) -> bool:
        """
        Test if a proxy is working.

        Args:
            proxy_id: Proxy ID to test
            timeout: Request timeout in seconds

        Returns:
            True if proxy works, False otherwise
        """
        import requests

        proxy = self.proxy_model.get(proxy_id)
        if not proxy:
            return False

        proxy_string = self.proxy_model.get_proxy_string(proxy)
        proxies = {
            'http': proxy_string,
            'https': proxy_string
        }

        try:
            response = requests.get(
                'https://www.google.com',
                proxies=proxies,
                timeout=timeout
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Proxy test failed for {proxy['host']}:{proxy['port']}: {e}")
            return False

    def add_proxy_from_string(self, proxy_string: str) -> Optional[int]:
        """
        Add a proxy from a connection string.

        Formats supported:
        - host:port
        - protocol://host:port
        - protocol://username:password@host:port

        Args:
            proxy_string: Proxy connection string

        Returns:
            Proxy ID if created successfully, None otherwise
        """
        try:
            # Remove protocol if present
            protocol = 'http'
            if '://' in proxy_string:
                protocol, proxy_string = proxy_string.split('://', 1)

            # Check for authentication
            username = None
            password = None
            if '@' in proxy_string:
                auth, proxy_string = proxy_string.split('@', 1)
                if ':' in auth:
                    username, password = auth.split(':', 1)

            # Parse host and port
            if ':' not in proxy_string:
                raise ValueError("Invalid proxy format: missing port")

            host, port = proxy_string.rsplit(':', 1)
            port = int(port)

            # Create proxy
            proxy_id = self.proxy_model.create(
                host=host,
                port=port,
                protocol=protocol,
                username=username,
                password=password
            )

            logger.info(f"Added proxy: {host}:{port}")
            return proxy_id

        except Exception as e:
            logger.error(f"Failed to parse proxy string: {e}")
            return None

    def bulk_add_proxies(self, proxy_strings: list) -> Dict[str, Any]:
        """
        Add multiple proxies from a list of connection strings.

        Args:
            proxy_strings: List of proxy connection strings

        Returns:
            Dictionary with success count and failed items
        """
        results = {
            'added': 0,
            'failed': 0,
            'proxy_ids': []
        }

        for proxy_string in proxy_strings:
            proxy_id = self.add_proxy_from_string(proxy_string.strip())
            if proxy_id:
                results['added'] += 1
                results['proxy_ids'].append(proxy_id)
            else:
                results['failed'] += 1

        return results

    def remove_inactive_proxies(self) -> int:
        """
        Remove all inactive proxies (hard delete).

        Returns:
            Number of proxies deleted
        """
        proxies = self.proxy_model.get_all(active_only=False)
        deleted = 0

        for proxy in proxies:
            if not proxy['is_active']:
                self.proxy_model.delete(proxy['id'], soft_delete=False)
                deleted += 1

        return deleted
