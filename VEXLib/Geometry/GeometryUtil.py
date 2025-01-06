"""
Geometry Utility Module.

This module provides various functions for calculating distances, areas, centroids,
and other geometric properties. It also includes functions for handling lines and polygons.
"""

import math

from VEXLib.Geometry.Translation1d import Distance, Translation1d


def hypotenuse(x: float, y: float) -> float:
    """
    Get the hypotenuse length of a right triangle with sides x and y

    Args:
        x: The length of one leg of the triangle
        y: The length of the other leg of the triangle

    Returns:
        The hypotenuse length of a right triangle with side lengths x and y
    """

    return math.sqrt(pow(x, 2) + pow(y, 2))


def distance(point1, point2):
    """Get the Euclidean distance between two points.

    Args:
        point1 (tuple): Coordinates of the first point (x1, y1).
        point2 (tuple): Coordinates of the second point (x2, y2).

    Returns:
        float: The Euclidean distance between the two points.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def area_triangle(point1, point2, point3):
    """Calculate the area of a triangle formed by three points using Heron's formula.

    Args:
        point1 (tuple): Coordinates of the first point (x1, y1).
        point2 (tuple): Coordinates of the second point (x2, y2).
        point3 (tuple): Coordinates of the third point (x3, y3).

    Returns:
        float: The area of the triangle.
    """
    a = distance(point1, point2)
    b = distance(point2, point3)
    c = distance(point3, point1)
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def centroid(points):
    """Calculate the centroid (center of mass) of a list of points.

    Args:
        points (list): List of point coordinates [(x1, y1), (x2, y2), ...].

    Returns:
        tuple[float, float]: Coordinates of the centroid (x, y).
    """
    total_area = 0
    centroid_x = 0
    centroid_y = 0

    for i, point in enumerate(points):
        j = (i + 1) % len(points)
        factor = point[0] * points[j][1] - points[j][0] * point[1]
        total_area += factor
        centroid_x += (point[0] + points[j][0]) * factor
        centroid_y += (point[1] + points[j][1]) * factor

    total_area /= 2
    centroid_x /= (6 * total_area)
    centroid_y /= (6 * total_area)

    return centroid_x, centroid_y


def intersection_point(line1_start, line1_end, line2_start, line2_end):
    """Calculate the intersection point of two lines defined by their endpoints.

    Args:
        line1_start (tuple): Starting point of the first line (x1, y1).
        line1_end (tuple): Ending point of the first line (x2, y2).
        line2_start (tuple): Starting point of the second line (x3, y3).
        line2_end (tuple): Ending point of the second line (x4, y4).

    Returns:
        tuple or None: Coordinates of the intersection point (x, y) if it exists, None otherwise.
    """
    x1, y1 = line1_start
    x2, y2 = line1_end
    x3, y3 = line2_start
    x4, y4 = line2_end

    det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if det == 0:
        return None  # Lines are parallel

    intersection_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
    intersection_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

    # Check if the intersection point is within the line segments
    if (min(x1, x2) <= intersection_x <= max(x1, x2) and
            min(y1, y2) <= intersection_y <= max(y1, y2) and
            min(x3, x4) <= intersection_x <= max(x3, x4) and
            min(y3, y4) <= intersection_y <= max(y3, y4)):
        return intersection_x, intersection_y
    return None


def is_point_inside_polygon(point, polygon):
    """Check if a point is inside a polygon.

    Args:
        point (tuple): Coordinates of the point (x, y).
        polygon (list): List of polygon vertices [(x1, y1), (x2, y2), ...].

    Returns:
        bool: True if the point is inside the polygon, False otherwise.
    """
    num_vertices = len(polygon)
    intersection_count = 0

    for i in range(num_vertices):
        j = (i + 1) % num_vertices
        if ((polygon[i][1] > point[1]) != (polygon[j][1] > point[1]) and
                point[0] < (polygon[j][0] - polygon[i][0]) * (point[1] - polygon[i][1]) /
                (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
            intersection_count += 1

    return intersection_count % 2 == 1


def polygon_area(polygon):
    """Calculate the area of a polygon defined by its vertices using the shoelace formula.

    Args:
        polygon (list): List of polygon vertices [(x1, y1), (x2, y2), ...].

    Returns:
        float: The area of the polygon.
    """
    num_vertices = len(polygon)
    area = 0

    for i in range(num_vertices):
        j = (i + 1) % num_vertices
        area += (polygon[i][0] * polygon[j][1]) - (polygon[j][0] * polygon[i][1])

    return abs(area) / 2


def circle_area(radius):
    """Calculate the area of a circle given its radius.

    Args:
        radius (float): The radius of the circle.

    Returns:
        float: The area of the circle.
    """
    return math.pi * radius ** 2


def circle_circumference(radius):
    """Calculate the circumference of a circle given its radius.

    Args:
        radius (float | Distance): The radius of the circle.

    Returns:
        float | Distance: The circumference of the circle.
    """
    return 2 * math.pi * radius


def rectangle_area(width, height):
    """Calculate the area of a rectangle given its width and height.

    Args:
        width (float): The width of the rectangle.
        height (float): The height of the rectangle.

    Returns:
        float: The area of the rectangle.
    """
    return width * height


def rectangle_perimeter(width, height):
    """Calculate the perimeter of a rectangle given its width and height.

    Args:
        width (float): The width of the rectangle.
        height (float): The height of the rectangle.

    Returns:
        float: The perimeter of the rectangle.
    """
    return 2 * (width + height)


def closest_point_on_line(point, line_start, line_end):
    """
    Find the closest point on a line to a given point.

    Args:
        point (tuple): Coordinates of the point (x, y).
        line_start (tuple): Starting point of the line (x1, y1).
        line_end (tuple): Ending point of the line (x2, y2).

    Returns:
        tuple: Coordinates of the closest point on the line (x, y).
    """
    x1, y1 = line_start
    x2, y2 = line_end
    x0, y0 = point

    dx, dy = x2 - x1, y2 - y1
    if dx == dy == 0:
        return line_start  # Start and end are the same point

    t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))  # Clamp to segment

    x_closest = x1 + t * dx
    y_closest = y1 + t * dy

    return x_closest, y_closest


def arc_length_from_rotation(circle_circumference: Distance, rotation) -> Translation1d:
    """
    Calculate the arc length traveled by a circle given its circumference and a rotation value.

    Args:
        circle_circumference (Distance): The circumference of the circle.
        rotation: The rotation value (in revolutions).

    Returns:
        float: The arc length traveled by the circle.
    """
    return circle_circumference * rotation.to_revolutions()
