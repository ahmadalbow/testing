from planet import Planet, Direction
from typing import List, Tuple, Dict

class Erkunder():


    def __init__(self, planet):
        self.planet = planet
        self.points = {}
        self.cur_point = None
        self.visited = {}
        self._double_visited_direction = None
        self._double_visited = False
        self.is_Parent = False
        self.cur_direction = None

    def add_start_scann(self,point : Tuple[int,int], directions : List[Direction] ):
        self.points[point] = {}
        self.visited[point] = None
        self.cur_point = point
        for dir in directions :
            self.points[point].update({dir : (False)})


    def add_new_scann(self,point : Tuple[int,int], directions : List[Direction], in_diriction ):
        if (self.cur_point == point):
            self.is_Parent = True
            self.points[self.cur_point][in_diriction] = True
            self.planet.add_path((self.cur_point, self.cur_direction), (point, in_diriction),1)
        if (not self.is_Parent):
            self.planet.add_path((self.cur_point, self.cur_direction), (point, in_diriction),1)
        if (self.visited.__contains__(point)) :
            self._double_visited_direction = in_diriction
            self._double_visited = True
            self.cur_point = point
            return
        self._double_visited = False
        self.points[(point, in_diriction)] = {}
        self.visited[point] = in_diriction
        self.cur_point = point
        self.points[point] = {}
        for dir in directions :
            if (dir != in_diriction) :
                self.points[point].update({dir : (False)})

    def _are_all_points_visited(self):
        for point in self.points:
            for dir in self.points[point]:
                if not self.points[point][dir] :
                    return False
        return True


    def get_next_direction(self):
        if ( self._double_visited and not self.is_Parent) :
            self.is_Parent = True
            self.points[self.cur_point][self._double_visited_direction] = True
            if (self._are_all_points_visited()): return None
            return (self.cur_point,self._double_visited_direction)
        self.is_Parent = False
        for dir in self.points[self.cur_point]:
            if (not self.points[self.cur_point][dir]):
                self.points[self.cur_point][dir] = True
                self.cur_direction = dir
                return (self.cur_point,dir)
        if (not self._are_all_points_visited()):
            self.is_Parent = True
            return  (self.cur_point,self.visited[self.cur_point])
        return None