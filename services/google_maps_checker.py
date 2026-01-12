import time
import json
import logging
from typing import Optional, Dict, List, Tuple, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

from .grid_calculator import GridCalculator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleMapsChecker:
    """Service for checking business positions in Google Maps search results."""

    def __init__(self, proxy: Optional[str] = None, headless: bool = True):
        self.proxy = proxy
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        self.ua = UserAgent()

    def init_driver(self):
        """Initialize Chrome WebDriver."""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument('--headless=new')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument(f'user-agent={self.ua.random}')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--lang=pl-PL')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        if self.proxy:
            chrome_options.add_argument(f'--proxy-server={self.proxy}')

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise

    def close_driver(self):
        """Close the WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error closing driver: {e}")
            finally:
                self.driver = None

    def search_at_location(self, keyword: str, latitude: float, longitude: float,
                          business_name: str, timeout: int = 15) -> Dict[str, Any]:
        """
        Search for a keyword at specific coordinates and find business position.

        Args:
            keyword: Search phrase
            latitude: Location latitude
            longitude: Location longitude
            business_name: Name of the business to find
            timeout: Maximum wait time in seconds

        Returns:
            Dictionary with search results
        """
        if not self.driver:
            self.init_driver()

        result = {
            'found': False,
            'position': None,
            'total_results': 0,
            'error': None,
            'search_url': None
        }

        try:
            # Build Google Maps search URL with specific location
            search_url = (
                f"https://www.google.com/maps/search/{keyword}/"
                f"@{latitude},{longitude},15z"
            )
            result['search_url'] = search_url

            logger.info(f"Searching: {keyword} at ({latitude}, {longitude})")
            self.driver.get(search_url)

            # Wait for results to load
            time.sleep(3)  # Initial wait for map to load

            # Wait for search results container
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
                )
            except TimeoutException:
                result['error'] = 'Search results did not load'
                return result

            time.sleep(2)  # Additional wait for results to populate

            # Find all business listings
            results = self._extract_business_listings()
            result['total_results'] = len(results)

            if not results:
                result['error'] = 'No results found'
                return result

            # Search for the business in results
            position = self._find_business_position(results, business_name)

            if position is not None:
                result['found'] = True
                result['position'] = position
                logger.info(f"Business found at position {position}")
            else:
                logger.info(f"Business not found in top {len(results)} results")

        except Exception as e:
            logger.error(f"Error during search: {e}")
            result['error'] = str(e)

        return result

    def _extract_business_listings(self) -> List[Dict[str, str]]:
        """Extract business listings from Google Maps search results."""
        businesses = []

        try:
            # Find the results feed
            feed = self.driver.find_element(By.CSS_SELECTOR, "div[role='feed']")

            # Scroll through results to load more
            self._scroll_results(feed)

            # Find all business cards/links
            elements = feed.find_elements(By.CSS_SELECTOR, "a[href*='/maps/place/']")

            for idx, element in enumerate(elements):
                try:
                    # Extract business name from aria-label or text
                    name = element.get_attribute('aria-label')
                    if not name:
                        name = element.text

                    if name and name.strip():
                        businesses.append({
                            'position': idx + 1,
                            'name': name.strip(),
                            'url': element.get_attribute('href')
                        })
                except Exception as e:
                    logger.debug(f"Error extracting business at index {idx}: {e}")
                    continue

        except NoSuchElementException:
            logger.warning("Could not find results feed")

        return businesses

    def _scroll_results(self, feed_element, scroll_times: int = 3):
        """Scroll through results to load more businesses."""
        try:
            for _ in range(scroll_times):
                self.driver.execute_script(
                    "arguments[0].scrollTo(0, arguments[0].scrollHeight);",
                    feed_element
                )
                time.sleep(1.5)
        except Exception as e:
            logger.debug(f"Error scrolling results: {e}")

    def _find_business_position(self, businesses: List[Dict[str, str]],
                                business_name: str) -> Optional[int]:
        """
        Find the position of a business in search results.

        Uses fuzzy matching to handle slight name variations.
        """
        business_name_lower = business_name.lower()
        business_name_clean = self._clean_business_name(business_name_lower)

        for business in businesses:
            result_name_lower = business['name'].lower()
            result_name_clean = self._clean_business_name(result_name_lower)

            # Exact match
            if business_name_lower in result_name_lower or result_name_lower in business_name_lower:
                return business['position']

            # Clean match (without special characters)
            if business_name_clean in result_name_clean or result_name_clean in business_name_clean:
                return business['position']

        return None

    @staticmethod
    def _clean_business_name(name: str) -> str:
        """Remove special characters and extra spaces from business name."""
        import re
        # Remove special characters except spaces
        cleaned = re.sub(r'[^\w\s]', '', name)
        # Remove extra spaces
        cleaned = ' '.join(cleaned.split())
        return cleaned

    def check_project_keywords(self, project: Dict[str, Any],
                               keywords: List[Dict[str, Any]],
                               grid_size: str = '5x5',
                               radius_km: float = 5.0,
                               delay_between_checks: float = 2.0) -> List[Dict[str, Any]]:
        """
        Check all keywords for a project across a grid of locations.

        Args:
            project: Project dictionary with business info
            keywords: List of keyword dictionaries
            grid_size: Grid size (e.g., '5x5')
            radius_km: Radius in kilometers
            delay_between_checks: Delay between checks in seconds

        Returns:
            List of check results
        """
        all_results = []

        # Calculate grid points
        grid_points = GridCalculator.calculate_grid_points(
            project['latitude'],
            project['longitude'],
            radius_km,
            grid_size
        )

        logger.info(f"Checking {len(keywords)} keywords across {len(grid_points)} grid points")

        try:
            # Initialize driver once for all checks
            self.init_driver()

            for keyword in keywords:
                keyword_results = []

                for lat, lon, grid_x, grid_y in grid_points:
                    # Check position at this location
                    result = self.search_at_location(
                        keyword['phrase'],
                        lat,
                        lon,
                        project['google_business_name']
                    )

                    check_result = {
                        'keyword_id': keyword['id'],
                        'grid_x': grid_x,
                        'grid_y': grid_y,
                        'latitude': lat,
                        'longitude': lon,
                        'found': result['found'],
                        'position': result['position'],
                        'response_data': json.dumps(result)
                    }

                    keyword_results.append(check_result)
                    all_results.append(check_result)

                    logger.info(
                        f"Keyword '{keyword['phrase']}' at grid ({grid_x},{grid_y}): "
                        f"{'Found at position ' + str(result['position']) if result['found'] else 'Not found'}"
                    )

                    # Delay between checks to avoid rate limiting
                    time.sleep(delay_between_checks)

        finally:
            self.close_driver()

        return all_results

    def __enter__(self):
        """Context manager entry."""
        self.init_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_driver()
