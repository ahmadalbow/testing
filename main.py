from planet import  Planet,Direction
from explorer import Explorer
planet = Planet()
explorer = Explorer(planet)
explorer.add_start_scan((0, 0), [90,270],270)
explorer.set_choosed_direction(90,False)
explorer.add_new_scan((0,1),[90,270,180],270,10)
explorer.set_choosed_direction(180,False)
explorer.add_new_scan((1,1),[0],0,1)
print(explorer.get_next_direction())










