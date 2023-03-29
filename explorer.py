import copy

from planet import Planet, Direction
from typing import List, Tuple, Dict


class Point():
    def __init__(self, coordinates: Tuple[int, int]):
        self.coordinates = coordinates
        self.directions = {}
        self.original_perant = None
        self.last_parent = None
        self.cur_direction = None
        self.just_scanned = True
    def __eq__(self, other):
        if not isinstance(other, Point):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.coordinates == other.coordinates

    def add_directions(self, directions):
        for dir in directions:
            self.directions.update({dir: False})
class Explorer():

    def __init__(self, planet):
        self.planet = planet
        self.points = []
        self.cur_point = Point(None)
        self.prev_point = Point(None)



    # check if the coordinate is alreadey visited
    def is_visited(self, point ):
        return self.planet.paths.__contains__(point)
    # check if all the outgoings path of a point is drived, so then is point explored
    def is_explored(self, point: Point):
        for dir in point.directions:
            if not point.directions[dir]:
                return False
        return True
    def is_parent(self, point):
        if (self.prev_point.coordinates == None) :
            return False
        if ((self.prev_point.last_parent.coordinates == self.cur_point.coordinates) ) :
            return  True
        if (self.prev_point.original_perant == None):
            return False
        return (self.prev_point.original_perant.coordinates == self.cur_point.coordinates)
    def add_start_scann(self, coordinates: Tuple[int, int], directions: List[Direction]):
        point = Point(coordinates)
        point.add_directions(directions)
        self.cur_point = point
        self.points.append(point)
    def add_path_to_planet(self):
        self.planet.add_path((self.prev_point.coordinates, self.prev_point.cur_direction), \
                                 (self.cur_point.coordinates, self.cur_point.cur_direction),1)
    def get_point(self,coordinates):
        for p in self.points:
            if p.coordinates == coordinates:
                return p
        return None
    def add_new_scann(self, coordinates: Tuple[int, int], directions: List[Direction], in_diriction):
        weight = 1

        self.prev_point = copy.deepcopy(self.cur_point)
        if (self.cur_point.coordinates == coordinates):
            cur_point_index = self.points.index(self.get_point(coordinates))
            self.points[cur_point_index].directions[in_diriction] = True
            self.cur_point.cur_direction = in_diriction
            self.points[cur_point_index].last_parent = self.prev_point
            self.add_path_to_planet()
            return
        if ( self.is_visited(coordinates)):
            cur_point_index = self.points.index(self.get_point(coordinates))
            self.points[cur_point_index].last_parent = self.prev_point
            self.points[cur_point_index].just_scanned = False
            self.cur_point = self.get_point(coordinates)
            self.cur_point.cur_direction = in_diriction
            self.points[cur_point_index].directions[in_diriction] = True
            if (not self.is_parent(self.cur_point)):
                self.add_path_to_planet()
            else:
                self.cur_point = self.get_point(coordinates)
        else :
            point = Point(coordinates)
            point.original_perant = self.prev_point
            point.last_parent = self.prev_point
            point.add_directions(directions)
            point.directions[in_diriction] = True
            point.cur_direction = in_diriction
            self.cur_point = point
            self.points.append(point)
            self.add_path_to_planet()
    def _are_all_points_visited(self):
        for point in self.points:
            if (not self.is_explored(point)) :
                return False
        return True

    def get_next_direction(self):
        direction = None
        cur_point_index = self.points.index(self.cur_point)
        if (not self.cur_point.just_scanned and not self.is_parent(self.cur_point)):
            self.points[cur_point_index].directions[self.cur_point.cur_direction] = True
            if (self._are_all_points_visited()):
                return None
            direction =  (self.cur_point.coordinates,
            self.planet.get_out_direction(self.cur_point.coordinates, self.prev_point.coordinates))
            self.points[cur_point_index].cur_direction = direction[1]
            return direction
        for dir in self.cur_point.directions:
            if (not self.cur_point.directions[dir]):
                self.points[cur_point_index].directions[dir] = True
                direction = (self.cur_point.coordinates, dir)
                self.points[cur_point_index].cur_direction = direction[1]
                return direction
        if (not self._are_all_points_visited()):
            direction = (self.cur_point.coordinates, self.planet.get_out_direction(self.cur_point.coordinates,
                                                                              self.cur_point.original_perant.coordinates))
            self.points[cur_point_index].cur_direction = direction[1]
            return direction
        return None
