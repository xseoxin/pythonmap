import math
from typing import List, Tuple


class GridCalculator:
    """Calculate grid points around a central location."""

    EARTH_RADIUS_KM = 6371.0

    @staticmethod
    def parse_grid_size(grid_size: str) -> Tuple[int, int]:
        """Parse grid size string (e.g., '5x5') to tuple."""
        parts = grid_size.lower().split('x')
        if len(parts) != 2:
            raise ValueError(f"Invalid grid size format: {grid_size}")
        return int(parts[0]), int(parts[1])

    @staticmethod
    def calculate_grid_points(center_lat: float, center_lon: float,
                              radius_km: float, grid_size: str) -> List[Tuple[float, float, int, int]]:
        """
        Calculate grid points around a center location.

        Args:
            center_lat: Center latitude
            center_lon: Center longitude
            radius_km: Radius in kilometers
            grid_size: Grid size as string (e.g., '5x5', '7x7')

        Returns:
            List of tuples: (latitude, longitude, grid_x, grid_y)
        """
        rows, cols = GridCalculator.parse_grid_size(grid_size)
        points = []

        # Calculate step size in kilometers
        step_km = (2 * radius_km) / (max(rows, cols) - 1) if max(rows, cols) > 1 else 0

        # Calculate offset from center
        offset_lat = (rows - 1) / 2
        offset_lon = (cols - 1) / 2

        for row in range(rows):
            for col in range(cols):
                # Calculate distance from center in grid units
                lat_steps = row - offset_lat
                lon_steps = col - offset_lon

                # Convert to kilometers
                lat_km = lat_steps * step_km
                lon_km = lon_steps * step_km

                # Calculate new coordinates
                new_lat, new_lon = GridCalculator.offset_coordinates(
                    center_lat, center_lon, lat_km, lon_km
                )

                points.append((new_lat, new_lon, col, row))

        return points

    @staticmethod
    def offset_coordinates(lat: float, lon: float,
                          offset_lat_km: float, offset_lon_km: float) -> Tuple[float, float]:
        """
        Offset coordinates by distance in kilometers.

        Args:
            lat: Original latitude
            lon: Original longitude
            offset_lat_km: Offset in kilometers (north/south)
            offset_lon_km: Offset in kilometers (east/west)

        Returns:
            Tuple of (new_latitude, new_longitude)
        """
        # Latitude offset (1 degree ≈ 111.32 km)
        new_lat = lat + (offset_lat_km / 111.32)

        # Longitude offset (varies with latitude)
        lon_km_per_degree = 111.32 * math.cos(math.radians(lat))
        new_lon = lon + (offset_lon_km / lon_km_per_degree) if lon_km_per_degree != 0 else lon

        return new_lat, new_lon

    @staticmethod
    def calculate_distance(lat1: float, lon1: float,
                          lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula.

        Returns:
            Distance in kilometers
        """
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return GridCalculator.EARTH_RADIUS_KM * c

    @staticmethod
    def get_grid_center_index(grid_size: str) -> Tuple[int, int]:
        """Get the index of the center point in the grid."""
        rows, cols = GridCalculator.parse_grid_size(grid_size)
        return cols // 2, rows // 2
