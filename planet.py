#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
from enum import IntEnum, unique
from typing import Optional, List, Tuple, Dict

@unique
class Direction(IntEnum):
    """ Directions in shortcut """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


Weight = int
"""
Weight of a given path (received from the server)

Value:  -1 if blocked path
        >0 for all other paths
        never 0
"""


class Planet:
    """
    Contains the representation of the map and provides certain functions to manipulate or extend
    it according to the specifications
    """

    def __init__(self):
        """ Initializes the data structure """
        self.paths = {}
        self.explorer = None

    def add_path(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction],
                 weight: int):

        # if the start or the target is not a point then the path will not be added
        if (start[0] == (None,None) or target[0] == (None,None)) : return

        # Check if the point already was add in the paths if not a dictionery will be assigned to its value
        if (self.paths.keys().__contains__(start[0])):
            self.paths[start[0]][start[1]] = (target[0], target[1], weight)
        else:
            self.paths[start[0]] = {start[1]: (target[0], target[1], weight)}
        if (self.paths.keys().__contains__(target[0])):
            self.paths[target[0]][target[1]] = (start[0], start[1], weight)
        else:
            self.paths[target[0]] = {target[1]: (start[0], start[1], weight)}
        self.explorer.add_path(start,target)
        if (weight == -1):
            self.explorer.block(start[0],target[0])

    def get_paths(self) -> Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]:
        return  self.paths

    # get all the points in the map
    def get_vertices(self):
        return self.paths.keys()

    # get the neigbours of a specific point
    def get_neigbours(self, point: Tuple[int, int]):
        neigbours = []
        outgoings = self.paths[point]
        for x in outgoings:
            neigbours.append((outgoings[x][0], x, outgoings[x][2]))
        return neigbours
    # get the direction from the target point to the start point
    def get_in_direction(self, start :Tuple[int,int], target: Tuple[int,int]):
        start_directions = self.get_paths()[start]
        for dir in start_directions:
            if (start_directions[dir][0] == target):
                return start_directions[dir][1]
        return None

    # get the direction from the start point to the target point
    def get_out_direction(self, start: Tuple[int,int], target: Tuple[int,int]):
        start_directions = self.paths[start]
        for dir in start_directions:
            if (start_directions[dir][0] == target):
                return dir
        return None
    def block_path(self,start:Tuple[int, int],end : Tuple[int, int]):
        self.paths[start][self.get_out_direction(start,end)][2] = -1
        self.paths[end][self.get_in_direction(start, end)][2] = -1
        self.explorer.block(start, end)
    def un_block_path(self,start:Tuple[int, int],end : Tuple[int, int],weight : Weight):
        self.paths[start][self.get_out_direction(start, end)][2] = weight
        self.paths[end][self.get_in_direction(start, end)][2] = weight
        self.explorer.unblock(start,end)
    def path_length(self,paths):
        lenght = 0
        if paths == None:
            return  float("inf")
        for path in paths :
            lenght += self.paths[path[0]][path[1]][2]
        return lenght
    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[Tuple[int, int], Direction]]]:

        # Dijkstra algorithm to find the shortest path

        # set the distances to all the other points to infinity
        distances = {v: float("inf") for v in self.get_vertices()}
        # save the previous vertices in the form (vertices, Direction)
        prev_v = {v: None for v in self.get_vertices()}
        if (not prev_v.__contains__(start)) : prev_v[start] = None
        if (not prev_v.__contains__(target)): prev_v[target] = None
        # set the distances of the start point to zero
        distances[start] = 0

        #make a copy of the original vertices
        vertices = list(self.get_vertices())[:]

        #applying the dijkstra algorithm to find the shortest way
        while len(vertices) > 0:

            v = min(vertices, key=lambda a: distances[a])
            vertices.remove(v)
            if (distances[v] == float("inf")):
                break
            for neighbour, dict, weight in self.get_neigbours(v):
               # don't change the distance to the point if the path is blocked and keep it by infinity
                if (weight == -1):
                    continue
                else:
                    path_weight = distances[v] + weight
                    if path_weight < distances[neighbour]:
                        distances[neighbour] = path_weight
                        prev_v[neighbour] = (v, dict)
        path = []
        curr_v = target
        while prev_v[curr_v] is not None:
            path.insert(0, prev_v[curr_v])
            curr_v = prev_v[curr_v][0]
        if (start != target) & (path == []): return None
        return path
