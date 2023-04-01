from planet import  Planet,Direction
from explorer import Explorer
planet = Planet()
explorer = Explorer(planet)
explorer.add_start_scan((0, 0), [0,270],0)
print(explorer.get_next_direction())
explorer.set_choosed_direction(270)
explorer.add_new_scan((0,1),[90,270,180],270,999)
explorer.set_choosed_direction(180)
explorer.add_new_scan((0,2),[0,270,90,180],270,15)
planet.add_path(((0,2),0),((0,3),180),7)
planet.add_path(((0,2),270),((0,2),270),-1)
planet.add_path(((0,1),180),((0,1),180),-1)
explorer.set_choosed_direction(270)
print(explorer.get_next_direction())









