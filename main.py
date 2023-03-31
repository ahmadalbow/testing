from planet import  Planet,Direction
from explorer import Explorer
planet = Planet()
explorer = Explorer(planet)
explorer.add_start_scann((68, 421), [Direction.NORTH])
print(explorer.get_next_direction())
explorer.set_choosed_direction(explorer.get_next_direction()[1])
explorer.add_new_scann((68, 422), [Direction.EAST, Direction.NORTH, Direction.SOUTH], Direction.SOUTH,1)
print(explorer.get_next_direction())
explorer.set_choosed_direction(Direction.NORTH)
explorer.add_new_scann((69, 423), [Direction.WEST, Direction.NORTH], Direction.WEST,1)
print(explorer.get_next_direction())
explorer.set_choosed_direction(Direction.NORTH)
explorer.add_new_scann((70, 424), [Direction.WEST], Direction.WEST,1)
print(explorer.get_next_direction())
explorer.set_choosed_direction(Direction.WEST)






