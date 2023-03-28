import unittest
from planet import Planet
class ExampleTestPlanet(unittest.TestCase):
    def setUp(self) :
        self.planet = Planet()
    def test_add(self):
        self.assertEqual(15,self.planet.add(10,5))


if __name__ == '__main__':
    unittest.main()
