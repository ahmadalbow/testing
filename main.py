from planet import  Planet,Direction
from explorer import Explorer
planet = Planet()
explorer = Explorer(planet)
explorer.add_start_scan((150, 120), [180,270],180)
explorer.set_choosed_direction(270)
explorer.add_new_scan((149,120),[0,90,270],90,1)
planet.add_path(((148,120),0),((149,121),270),1)
explorer.set_choosed_direction(270)
explorer.add_new_scan((148,120),[0,90],90,1)
planet.add_path(((148,120),0),((148,120),0),-1)
planet.add_path(((149,121),270),((149,121),270),-1)
planet.add_path(((149,121),0),((149,122),180),2)
planet.add_path(((149,122),270),((149,122),270),-1)
planet.add_path(((149,122),90),((150,122),270),2)
explorer.set_choosed_direction(270)
explorer.add_new_scan((149,120),None,270,1)
explorer.set_choosed_direction(0)
explorer.add_new_scan((149,121),[0,90,270,180],180,4)
explorer.set_choosed_direction(90)
explorer.add_new_scan((150,122),[0,270,180],180,4)
explorer.set_choosed_direction(0)
explorer.add_new_scan((150,123),[0,270,180],180,1)
explorer.set_choosed_direction(270)
explorer.add_new_scan((149,123),[270,90],90,1)
explorer.set_choosed_direction(270)
explorer.add_new_scan((149,123),None,270,-1)
print(explorer.get_next_direction())













