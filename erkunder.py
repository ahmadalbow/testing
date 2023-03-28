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


    def add_start_scann(self,point : Tuple[int,int], directions : List[Direction] ):
        self.points[point] = {}
        self.visited[point] = None
        self.cur_point = point
        for dir in directions :
            self.points[point].update({dir : (False)})


    def add_new_scann(self,point : Tuple[int,int], directions : List[Direction], in_diriction ):
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



    def get_new_direction(self):
        if ( self._double_visited and not self.is_Parent) :
            self.is_Parent = True
            self.points[self.cur_point][self._double_visited_direction] = True
            return self._double_visited_direction
        self.is_Parent = False
        for dir in self.points[self.cur_point]:
            if (not self.points[self.cur_point][dir]):
                self.points[self.cur_point][dir] = True
                return dir
        if (not self._are_all_points_visited()):
            self.is_Parent = True
            return  self.visited[self.cur_point]
        return None
