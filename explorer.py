from planet import Planet, Direction
from typing import List, Tuple, Dict


class Point():
    def __init__(self, coordinates: Tuple[int, int]):
        self.coordinates = coordinates
        self.directions = {}
        self.original_perant = None
        self.last_parent = None

    def add_directions(self, directions):
        for dir in directions:
            self.directions.update({dir: False})
class Explorer():

    def __init__(self, planet):
        self.planet = planet
        self.points = []
        self.cur_point = None
        self.prev_point = None
        self.visited = {}
        self._double_visited_direction = None
        self._double_visited = False
        self.back_to_parent = False
        self.cur_direction = None

    # check if the coordinate is alreadey visited
    def is_visited(self, coordinates: Tuple[int, int]):
        for point in self.points:
            if (point.coordinates == coordinates):
                return True
        return False

    # check if all the outgoings path of a point is drived, so then is point explored
    def is_explored(self, point: Point):
        for dir in point.directions:
            if not point.directions[dir]:
                return False
        return True


    def add_start_scann(self, coordinates: Tuple[int, int], directions: List[Direction]):
        point = Point(coordinates)
        point.add_directions(directions)
        self.cur_point = point
        self.points.append(point)

    def add_new_scann(self, coordinates: Tuple[int, int], directions: List[Direction], in_diriction):
        point = Point(coordinates)
        point.last_parent = self.cur_point
        self.prev_point = self.cur_point
        self.cur_point = point
        if (self.cur_point == point.last_parent):
            self.back_to_parent = True
            self.points[self.cur_point][in_diriction] = True
            self.planet.add_path((self.cur_point, self.cur_direction), (coordinates, in_diriction), 1)
        if (not self.back_to_parent):
            self.planet.add_path((self.cur_point, self.cur_direction), (coordinates, in_diriction), 1)
        if (self.is_visited(point)):
            self._double_visited_direction = in_diriction
            self._double_visited = True
            self.cur_point = coordinates
            return

        self._double_visited = False
        self.points[(coordinates, in_diriction)] = {}
        self.visited[coordinates] = in_diriction

        self.points[coordinates] = {}
        for dir in directions:
            if (dir != in_diriction):
                self.points[coordinates].update({dir: (False)})

    def _are_all_points_visited(self):
        for point in self.points:
            for dir in self.points[point]:
                if not self.points[point][dir]:
                    return False
        return True

    def get_next_direction(self):
        if (self._double_visited and not self.back_to_parent):
            self.back_to_parent = True
            self.points[self.cur_point][self._double_visited_direction] = True
            if (self._are_all_points_visited()): return None
            return (self.cur_point, self._double_visited_direction)
        self.back_to_parent = False
        for dir in self.points[self.cur_point]:
            if (not self.points[self.cur_point][dir]):
                self.points[self.cur_point][dir] = True
                self.cur_direction = dir
                return (self.cur_point, dir)
        if (not self._are_all_points_visited()):
            self.back_to_parent = True
            return (self.cur_point, self.visited[self.cur_point])
        return None
