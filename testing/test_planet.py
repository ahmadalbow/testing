#!/usr/bin/env python3

import unittest

from planet  import Direction, Planet

class ExampleTestPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        +--+
        |  |
        +-0,3------+
           |       |
          0,2-----2,2 (target)
           |      /
        +-0,1    /
        |  |    /
        +-0,0-1,0
           |
        (start)

        """
        # Initialize your data structure here
        self.planet = Planet()
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 1), Direction.WEST), ((0, 0), Direction.WEST), 1)

    @unittest.skip('Example test, should not count in final test results')
    def test_target_not_reachable_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target not reachable nearby

        Result: Target is not reachable
        """
        self.assertIsNone(self.planet.shortest_path((0, 0), (1, 2)))


class TestRoboLabPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        MODEL YOUR TEST PLANET HERE (if you'd like):

        """
        # Initialize your data structure here
        self.planet = Planet()

        #Mehl Planet
        self.planet.add_path(((3, 4), Direction.WEST), ((2, 4), Direction.EAST), 1)
        self.planet.add_path(((2, 4), Direction.WEST), ((1, 5), Direction.SOUTH), 1)
        self.planet.add_path(((1, 5), Direction.EAST), ((3, 5), Direction.WEST), 1)
        self.planet.add_path(((3, 5), Direction.EAST), ((3, 7), Direction.EAST), 3)
        self.planet.add_path(((3, 7), Direction.SOUTH), ((2, 6), Direction.EAST), -1)
        self.planet.add_path(((3, 7), Direction.NORTH), ((2, 8), Direction.EAST), 4)
        self.planet.add_path(((2, 8), Direction.SOUTH), ((2, 6), Direction.NORTH), 5)
        self.planet.add_path(((2, 8), Direction.WEST), ((1, 6), Direction.NORTH), 2)
        self.planet.add_path(((1, 6), Direction.EAST), ((2, 6), Direction.WEST), 2)
        #unreachable path
        self.planet.add_path(((1, 9), Direction.EAST), ((2, 9), Direction.WEST), 2)
        # Same Length Path
        self.planet.add_path(((3, 4), Direction.NORTH), ((3, 5), Direction.SOUTH), 3)
        #Loop Path
        self.planet.add_path(((1, 6), Direction.WEST), ((1, 6), Direction.SOUTH), 1)

        #Empty Planet
        self.empty_planet = Planet()

    def test_integrity(self):
        """
        This test should check that the dictionary returned by "planet.get_paths()" matches the expected structure
        """
        expected_paths = {
            (3, 4): {
                        Direction.WEST: ((2, 4), Direction.EAST, 1),
                        Direction.NORTH: ((3, 5), Direction.SOUTH, 3)},
            (2, 4): {
                        Direction.EAST: ((3, 4), Direction.WEST, 1),
                        Direction.WEST: ((1, 5), Direction.SOUTH, 1)},
            (1, 5): {
                        Direction.SOUTH: ((2, 4), Direction.WEST, 1),
                        Direction.EAST: ((3, 5), Direction.WEST, 1)},
            (3, 5): {
                        Direction.WEST: ((1, 5), Direction.EAST, 1),
                        Direction.EAST: ((3, 7), Direction.EAST, 3),
                        Direction.SOUTH: ((3, 4), Direction.NORTH, 3)},
            (3, 7): {
                        Direction.EAST: ((3, 5), Direction.EAST, 3),
                        Direction.SOUTH: ((2, 6), Direction.EAST, -1),
                        Direction.NORTH: ((2, 8), Direction.EAST, 4)},
            (2, 6): {
                        Direction.EAST:((3, 7), Direction.SOUTH, -1),
                        Direction.NORTH:((2, 8), Direction.SOUTH, 5),
                        Direction.WEST: ((1, 6), Direction.EAST, 2)},
            (2, 8): {
                        Direction.EAST: ((3, 7), Direction.NORTH, 4),
                        Direction.SOUTH: ((2, 6), Direction.NORTH, 5),
                        Direction.WEST: ((1, 6), Direction.NORTH, 2)},
            (1, 6): {
                        Direction.NORTH: ((2, 8), Direction.WEST, 2),
                        Direction.EAST: ((2, 6), Direction.WEST, 2),
                        Direction.WEST: ((1, 6), Direction.SOUTH, 1),
                        Direction.SOUTH: ((1, 6), Direction.WEST, 1)},
            (1, 9): {
            Direction.EAST: ((2, 9), Direction.WEST, 2)},
            (2, 9): {
                Direction.WEST: ((1, 9), Direction.EAST, 2)}
        }

        self.assertEqual(expected_paths,self.planet.get_paths())

    def test_empty_planet(self):
        """
        This test should check that an empty planet really is empty
        """
        paths = {}
        self.assertEqual(paths,self.empty_planet.get_paths())

    def test_target(self):
        """
        This test should check that the shortest-path algorithm implemented works.

        Requirement: Minimum distance is three nodes (two paths in list returned)
        """
        shortest_path = [((3,7),Direction.NORTH),((2,8),Direction.WEST),((1,6),Direction.EAST)]
        self.assertEqual(shortest_path, self.planet.shortest_path((3,7),(2,6)))

    def test_target_not_reachable(self):
        """
        This test should check that a target outside the map or at an unexplored node is not reachable
        """
        # test if the shortest path between (3,4) and (1,9) is None
        self.assertIsNone(self.planet.shortest_path((3,4),(1,9)))

    def test_same_length(self):
        """
        This test should check that the shortest-path algorithm implemented returns a shortest path even if there
        are multiple shortest paths with the same length.

        Requirement: Minimum of two paths with same cost exists, only one is returned by the logic implemented
        """

        """
         the length of the path [((3,4),Direction.NORTH)] is equal to the length of the path
         [((3,4),Direction.WEST),((2,4),Direction.WEST),((1,5),Direction.EAST)] 
        """

        shortest_path = [((3,4),Direction.NORTH)]
        self.assertEqual(self.planet.shortest_path((3,4),(3,5)),shortest_path)

    def test_target_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target nearby

        Result: Target is reachable
        """
        self.assertIsNotNone(self.planet.shortest_path((2,8),(2,6)))

    def test_target_not_reachable_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target not reachable nearby

        Result: Target is not reachable
        """
        self.assertIsNone(self.planet.shortest_path((2, 10), (1, 6)))


if __name__ == "__main__":
    unittest.main()
