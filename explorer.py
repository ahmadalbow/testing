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
            return NotImplemented
        return self.coordinates == other.coordinates

    def add_directions(self, directions):
        for dir in directions:
            self.directions.update({dir: False})
class Explorer():

    def __init__(self, planet):
        self.planet = planet
        self.planet.explorer = self
        self.points = []
        self.cur_point = Point(None)
        self.prev_point = Point(None)



    # check if the coordinate is alreadey visited
    def is_visited(self, point ):
        return self.points.__contains__(Point(point))
    # check if all the outgoings path of a point is drived, so then is point explored
    def is_explored(self, point: Point):
        for dir in point.directions:
            if not point.directions[dir]:
                return False
        return True
    def is_parent(self, point):
        if (self.prev_point == None or self.prev_point.last_parent == None):
            return False
        if (self.prev_point.coordinates == None) :
            return False
        if ((self.prev_point.last_parent.coordinates == self.cur_point.coordinates) ) :
            return  True
        if (self.prev_point.original_perant == None):
            return False
        return (self.prev_point.original_perant.coordinates == self.cur_point.coordinates)
    def add_start_scan(self, coordinates: Tuple[int, int], directions: List[Direction],in_direction):
        point = Point(coordinates)
        point.add_directions(directions)
        point.directions[in_direction] = True
        self.cur_point = point
        self.points.append(point)
    def add_path_to_planet(self,weight):
        self.planet.add_path((self.prev_point.coordinates, self.prev_point.cur_direction), \
                                 (self.cur_point.coordinates, self.cur_point.cur_direction),weight)
    def get_point(self,coordinates):
        for p in self.points:
            if p.coordinates == coordinates:
                return p
        return None
    def unblock(self,start, end):
        self.get_point(start).directions[self.planet.get_out_direction(start,end)] = False
        self.get_point(end).directions[self.planet.get_out_direction(end, start)] = False
    def block(self,start, end):
        self.get_point(start).directions[self.planet.get_out_direction(start,end)] = True
        self.get_point(end).directions[self.planet.get_out_direction(end, start)] = True



    def add_new_scan(self, coordinates: Tuple[int, int], directions: List[Direction], in_diriction,weight):
        if (not directions.__contains__(in_diriction)):
            directions.append(in_diriction)
        self.prev_point = copy.deepcopy(self.cur_point)
        if (self.cur_point.coordinates == coordinates):

            cur_point_index = self.points.index(self.get_point(coordinates))
            self.points[cur_point_index].directions[in_diriction] = True
            self.cur_point.cur_direction = in_diriction
            self.points[cur_point_index].last_parent = self.prev_point
            if(self.prev_point.cur_direction == self.cur_point.cur_direction):
                self.add_path_to_planet(-1)
                return
            self.add_path_to_planet(weight)
            return
        if ( self.is_visited(coordinates)):
            dirs = self.get_point(coordinates).directions.copy()
            if (directions != None):
                for dir in dirs:
                    if (not directions.__contains__(dir)):
                        del self.get_point(coordinates).directions[dir]
            cur_point_index = self.points.index(self.get_point(coordinates))
            self.points[cur_point_index].last_parent = self.prev_point
            self.points[cur_point_index].just_scanned = False
            self.cur_point = self.get_point(coordinates)
            self.cur_point.cur_direction = in_diriction
            self.points[cur_point_index].directions[in_diriction] = True
            if (not self.is_parent(self.cur_point)):
                self.add_path_to_planet(weight)
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
            self.add_path_to_planet(weight)

    def _are_all_points_visited(self):
        for point in self.points:
            if (not self.is_explored(point)) :
                return False
        return True
    def add_path(self,start,end):
        start_point = start[0]
        start_direction = start[1]
        end_point = end[0]
        end_direction = end[1]
        if (self.points.__contains__(Point(start_point))):
            self.get_point(start_point).directions[start_direction] = True
        else :
            point = Point(start_point)
            point.directions = {Direction.NORTH:False,Direction.WEST:False,Direction.SOUTH:False,Direction.EAST:False}
            point.directions[start_direction] = True
            self.points.append(point)
        if (self.points.__contains__(Point(end_point))):
            self.get_point(end_point).directions[end_direction] = True
        else :
            point = Point(end_point)
            point.directions = {Direction.NORTH:False,Direction.WEST:False,Direction.SOUTH:False,Direction.EAST:False}
            point.directions[end_direction] = True
            self.points.append(point)



    def get_next_direction(self):
        direction = None
        cur_point_index = self.points.index(self.cur_point)
        for dir in self.cur_point.directions:
            if (not self.cur_point.directions[dir]):
                try:
                    direction = (self.cur_point.coordinates, dir.value)
                except:
                    direction = (self.cur_point.coordinates, dir)

                return direction
        if (not self._are_all_points_visited()):
            un_exp_p = {}
            for p in self.points:
                if (not self.is_explored(p)):
                    path_len = self.planet.path_length(self.planet.shortest_path(self.cur_point.coordinates,p.coordinates))
                    un_exp_p[p.coordinates] = path_len
            p = min(un_exp_p, key=lambda a: un_exp_p[a])
            if(self.planet.shortest_path(self.cur_point.coordinates,p) == None ) :
                return  None
            direction = self.planet.shortest_path(self.cur_point.coordinates,p)[0]
            try:
                return (direction[0],direction[1].value)
            except:
                direction
        return None
    def  set_choosed_direction(self,direction):
        if (direction == None):
            return
        cur_point_index = self.points.index(self.cur_point)
        self.points[cur_point_index].cur_direction = direction
        self.points[cur_point_index].directions[direction] = True