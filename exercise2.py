import math


class Canvas(list[str, ...]):
    def __init__(self, canvas_width, canvas_height):
        super().__init__([" " * canvas_width for _ in range(canvas_height)])
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def print(self: list[str, ...]):  # Print the canvas to see the result
        """
        Prints the given canvas adding the column and row numbers' ones place on top, at the bottom and on both sides. It
        makes use of an inner function, create_row_headers, to create the headers.
        :param canvas: The canvas to print
        """

        def create_row_headers(length: int):
            """A helper function to create the headers when printing the canvas"""
            return "".join([str(i % 10) for i in range(length)])

        header = " " + create_row_headers(len(canvas[0]))
        print(header)
        for idx, row in enumerate(canvas):
            print(idx % 10, row, idx % 10, sep="")
        print(header)

    def draw_polygon(self: list[str, ...], *points: tuple[int, int], closed: bool = True, line_char: str = "*"):
        """
        Draws a polygon by drawing the line segments the polygon consists of. If the polygon is closed, the last point is
        connected with the first, e.g., a line segment between the two is drawn.
        This function is implemented using an inner function, namely draw_line_segment. Function draw_line_segment is
        used to draw the individual line segments that make up the polygon.
        :param canvas: The canvas to draw the polygon on
        :param points: The points the polygon consists of
        :param closed: Whether the polygon is closed, e.g., the last point is connected to the first point
        :param line_char: The character to draw the polygon with
        """

        def draw_line_segment(canvas: list[str, ...], start: tuple[int, int], end: tuple[int, int], line_char: str = "*"):
            """
            Draws a line segment using Bresenham's line algorithm (https://en.wikipedia.org/wiki/Bresenham's_line_algorithm)
            It uses the inner function replace_at_index, which is responsible for replacing a character in a string, which
            represents the process of painting a character on the given canvas.
            :param canvas: The canvas to draw the line on
            :param start: The start point of the line to draw, a tuple with the x and y coordinates of the point
            :param end: The end point of the line to draw
            :param line_char: The character to draw the line with, defaults to "*"
            """

            def replace_at_index(s: str, r: str, idx: int) -> str:
                """A helper function to replace a string r at a given index idx in a string s. Used to paint a character
                on the canvas in this context."""
                return s[:idx] + r + s[idx + len(r):]

            x1, y1 = start
            x2, y2 = end

            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            error = dx - dy

            while x1 != x2 or y1 != y2:
                canvas[y1] = replace_at_index(canvas[y1], line_char, x1)

                double_error = error * 2
                if double_error > -dy:
                    error -= dy
                    x1 += sx

                if double_error < dx:
                    error += dx
                    y1 += sy

            canvas[y2] = replace_at_index(canvas[y2], line_char, x2)

        # Determine the start and end points of the open polygon
        start_points = points[:-1]
        end_points = points[1:]
        # If closed, add the start and end points of the line segment that connects the last and the first point
        if closed:
            start_points += (points[-1],)  # The awkward notation with the comma at the end indicates that the object is a
            # tuple. Omiting the comma and writing (points[1]) would be treated as just the
            # value points[-1], not as a tuple.
            end_points += (points[0],)

        # Draw each segment in turn. zip is used to build tuples each consisting of a start and an end point
        for start_point, end_point in zip(start_points, end_points):
            draw_line_segment(canvas, start_point, end_point, line_char)

    def draw_line(self: list[str, ...], start: tuple[int, int], end: tuple[int, int], line_char: str = "*"):
        """Uses the draw_polygon function to draw a line from the given start to the given end point."""
        canvas.draw_polygon(start, end, closed=False, line_char=line_char)

    def draw_rectangle(self: list[str, ...], upper_left: tuple[int, int], lower_right: tuple[int, int],
                       line_char: str = "*"):
        """Uses the draw_polygon function to draw a rectangle from the given upper-left to the given lower-right corner."""
        x1, y1 = upper_left
        x2, y2 = lower_right

        canvas.draw_polygon(upper_left, (x2, y1), lower_right, (x1, y2), line_char=line_char)

    def draw_n_gon(self: list[str, ...], center: tuple[int, int], radius: int, number_of_points: int, rotation: int = 0,
                   line_char: str = "*"):
        """
        Draws an n-gon, that is, a polygon with n points. The n-gon is centered around the given center point
        :param canvas: The canvas to draw on
        :param center: The center of the n-gon to draw
        :param radius: The radius of the n-gon to draw
        :param number_of_points: The number of points to distribute
        :param rotation: A optional start rotation in degrees. If not given, 0 is used
        :param line_char: An optional character to use when drawing
        """
        # Distribute the points evenly around a circle
        angles = range(rotation, 360 + rotation, 360 // number_of_points)

        points = []
        for angle in angles:
            # Convert the angle of the point to radians
            angle_in_radians = math.radians(angle)
            # Calculate the x and y positions of the point
            x = center[0] + radius * math.cos(angle_in_radians)
            y = center[1] + radius * math.sin(angle_in_radians)
            # Add the point to the list of points as a tuple
            points.append((round(x), round(y)))

        # Use the draw_polygon function to draw all the lines of the n-gon
        canvas.draw_polygon(*points, line_char=line_char)


'''
# Example usage:
#canvas_width = 100
#canvas_height = 40
#canvas = [" " * canvas_width for _ in range(canvas_height)]
'''

canvas = Canvas(100, 40)

# A simple line
canvas.draw_line((10, 4), (92, 19), "+")
# A polygon with five points, the last point will be connected to the first one
canvas.draw_polygon((7, 12), (24, 29), (42, 15), (37, 32), (15, 35))
# A rectangle from the upper-left corner to the lower-right corner
canvas.draw_rectangle((45, 2), (80, 27), line_char='#')
# An n-gon with a high number of points will appear like a circle
canvas.draw_n_gon((72, 25), 12, 20, 80, "-")

# Print what we have painted
canvas.print()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):  # used to print a single object
        return f"({self.x}/{self.y})"

    def __repr__(self):  # used to print a collection of objects
        return self.__str__()

    def distance_from_origin(self) -> float:
        distance = math.sqrt(self.x ** 2 + self.y ** 2)
        return distance


p1 = Point(2.3, 43.14)
p2 = Point(5.53, 2.5)
p3 = Point(12.2, 28.7)

print(p1)
print([p1, p2, p3])

p1 = Point(1, 1)
p2 = Point(5, 5)
p3 = Point(10, 10)
print(p1.distance_from_origin())
print(p2.distance_from_origin())
print(p3.distance_from_origin())


class Shape(list[Point, ...]):
    def __init__(self, *points):
        super().__init__(points)

    def centroid(self) -> Point:

        x_total = sum(point.x for point in self)
        y_total = sum(point.y for point in self)
        num_points = len(self)

        centroid_x = x_total / num_points
        centroid_y = y_total / num_points

        return Point(centroid_x, centroid_y)

    def __eq__(self, other):
        return self.centroid().distance_from_origin() == other.centroid().distance_from_origin()

    def __lt__(self, other):
        return self.centroid().distance_from_origin() < other.centroid().distance_from_origin()


s1 = Shape(p1, p2, p3)
s2 = Shape(p2)
s3 = Shape()

print(s1)
print(s2)
print(s3)

s1 = Shape(Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0))
s2 = Shape(Point(0, 0.5), Point(0.5, 1), Point(1, 0.5), Point(0.5, 0))
s3 = Shape(Point(0.25, 0.25), Point(0.25, 0.75), Point(0.75, 0.75), Point(0.75, 0.25))
print(s1.centroid())
print(s2.centroid())
print(s3.centroid())

s1 = Shape(Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0))
s2 = Shape(Point(0, 0.5), Point(0.5, 1), Point(1, 0.5), Point(0.5, 0))
print(s1 == s2) # Equal because the two have the same centroid
s2 = Shape(Point(5, 5), Point(5, 6), Point(6, 6), Point(6, 5))
print(s1 < s2) # s1 is smaller than s2 because its centroid is closer to the origin

s3 = Shape(Point(10, 10), Point(10, 11), Point(11, 11), Point(11, 10))
shapes = [s3, s1, s2]
print(shapes)
print(sorted(shapes)) # sorted by their distance from the origin
