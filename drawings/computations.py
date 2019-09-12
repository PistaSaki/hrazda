import numpy as np
from types import SimpleNamespace
#%%
delta = 320
x_corner = 3887
x_lamp = 1452
k = (x_lamp - delta/2 ) // delta
k = int(k)
print("noof steps before lamp", k)
first_step = x_lamp - (k +1/2) * delta
print("distance from first step to WC", first_step)

l = (x_corner - x_lamp - delta/2) // delta
l = int(l)
print("noof steps after the lamp", l)
last_step = (x_corner - x_lamp) - (l + 1/2) * delta
print("distance from last step to corner", last_step)
#%%
print("so the total number of tubes is", k + l + 2)
assert (k + l + 1) * delta + first_step + last_step == x_corner
#%%
x_start = 30
tubes_from_wall = [first_step + i * delta for i in range(k + l + 2)]
tubes_from_wall = np.array([x for x in tubes_from_wall if x > x_start])
print(tubes_from_wall)
print(tubes_from_wall - x_start)
#%%
gap = 10
#middle_i = max(i for i, x in enumerate(tubes_from_wall) if x  < x_corner / 2)
middle_i = len(tubes_from_wall) //2
print("Total number of tubes", len(tubes_from_wall), ". Split:",( middle_i, len(tubes_from_wall) - middle_i))
middle = (tubes_from_wall[middle_i -1] + tubes_from_wall[middle_i]) / 2
print("Middle of gap between the L parts from wall:", middle)
#%%
class Rail:
    def __init__(self, length, start, tubes_from_wall):
        self.length = length
        self.start = start
        self.tubes_from_wall = tubes_from_wall
        self.holes_vertical_from_wall = []
        
    @property
    def tubes_from_start(self):
        return list(np.array(self.tubes_from_wall) - self.start)
    @property
    def holes_vertical_from_start(self):
        return list(np.array(self.holes_vertical_from_wall) - self.start)
        
#%%
L1 = Rail(
    length = middle - x_start - gap/2,
    start = x_start,
    tubes_from_wall= tubes_from_wall[:middle_i]
)
L2 = Rail(
    length = x_corner - middle - gap/2,
    start = middle + gap / 2,
    tubes_from_wall= tubes_from_wall[middle_i: ]
)
assert x_start + L1.length + gap + L2.length == x_corner
#%%
L1.tubes_from_start
L2.tubes_from_start
#%%
for L in L1, L2:
    tw = L.tubes_from_wall 
    L.holes_vertical_from_wall = [
        (tw[0] + tw[1])/2, 
        (tw[-1] + tw[-2])/2
    ]
    
#%%

print("Holes on the wall:", L1.holes_vertical_from_wall + L2.holes_vertical_from_wall)



