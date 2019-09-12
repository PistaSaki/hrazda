import cadquery as cq

length = 3887.
width = 50.
thickness = 5.

box = cq.Workplane("XY").box(length, width, width)
print(box)
box2 = box.translate(thickness, thickness, 0)

show_object(box)
